# Heat Scoring — 热度评分算法

> 本文件定义 multi-agent-trend-ai 的热度评分公式、归一化方法、梯队阈值与生命周期判定逻辑。
> 最后更新: 2026-06-19

---

## 1. 评分公式

```
heat_score = 0.30 * norm(search_index)
          + 0.30 * norm(mention_count)
          + 0.20 * norm(article_count)
          + 0.20 * norm(engagement_rate)
```

输出范围: 0-100，保留 1 位小数。

### 1.1 权重分配理由

| 信号 | 权重 | 理由 |
|------|------|------|
| search_index | 0.30 | 反映用户主动搜索意愿，是最直接的"需求信号" |
| mention_count | 0.30 | 反映跨平台讨论度，覆盖公众号+视频号+技术社区 |
| article_count | 0.20 | 反映内容供给侧热度，但可能滞后 |
| engagement_rate | 0.20 | 反映用户参与深度（点赞/在看/评论比） |

### 1.2 归一化方法

对每个信号使用 **min-max 归一化**：
```
norm(x) = (x - min) / (max - min) * 100
```

- `min`, `max` 来自当次采集的全体关键词集合
- 不使用全局 min/max（避免冷启动偏差）
- 缺失信号按 0 处理，但 `confidence` 降级

---

## 2. 梯队阈值

| 梯队 | 范围 | 含义 | 颜色 |
|------|------|------|------|
| S | ≥ 85 | 核心热点（双爆） | #534AB7 紫 |
| A | 70-84.9 | 高潜热点（技术社区高热） | #185FA5 蓝 |
| B | 55-69.9 | 稳定增长（应用上升） | #3B6D11 绿 |
| C | < 55 | 长尾观察（新兴潜力） | #854F0B 橙 |

> **边界包含**: heat_score=85.0 → S，heat_score=70.0 → A（TC-06 验证）

---

## 3. 生命周期判定

基于 4 周滚动增长率 (g):

```
g = (current_week_score - 4_weeks_ago_score) / 4_weeks_ago_score
```

| g 范围 | 生命周期 |
|--------|---------|
| > 50% | introduction（引入期） |
| 10% ~ 50% | growth（成长期） |
| -10% ~ 10% | maturity（成熟期） |
| < -10% | decline（衰退期） |

### 3.1 判定用途
- **introduction** 词：标注为"新兴潜力"，建议创作者抢先布局
- **growth** 词：标注为"上升期"，建议尽快产出内容
- **maturity** 词：标注为"稳定流量"，适合做深度内容
- **decline** 词：标注为"热度下行"，建议替换选题

---

## 4. Confidence 计算

基于"证据源数 × 一致性"：

```
confidence = base × consistency

base:
  - 1 source: 0.5
  - 2 sources: 0.75
  - 3+ sources: 1.0

consistency:
  - 所有源评分在同一梯队: 1.0
  - 跨 1 梯队: 0.8
  - 跨 2 梯队: 0.5
  - 跨 ≥ 3 梯队: 0.3
```

| confidence | 输出标记 |
|------------|---------|
| ≥ 0.75 | high |
| 0.5-0.74 | medium |
| < 0.5 | low（移入"待观察"区） |

---

## 5. 评分更新机制

### 5.1 触发条件
- **定时**: 每周日 03:00 自动重算（cron）
- **手动**: 用户在对话中说"刷新关键词库" → `refresh_keyword_lib=true`
- **异常**: 单源失败 >3 次连续 → 触发临时重算

### 5.2 重算流程
1. 重新执行 Step 2 数据采集
2. 按公式计算新 heat_score
3. 与旧分数对比，计算增长率 g
4. 更新 `last_updated` 时间戳
5. 写入 `archive/keyword-pool-{YYYYMMDD}.md`
6. 触发 Tier 迁移检测

### 5.3 Tier 迁移检测
若词条从某梯队迁移到另一梯队（如 A → S），输出：
```
[tier-migration] MCP协议: A → S (2026-06-19)
```
并写入 `references/tier-migration.log`，供后续复盘。

---

## 6. 异常处理

| 异常 | 处理 |
|------|------|
| 信号缺失 | 该项按 0 分，但 confidence 降级 |
| 公式除零 | 使用上一周期分数 + 标记 `stale` |
| 跨源评分极差 (>50) | 标记 `inconsistent`，降一档 confidence |
| 新词无历史 | 跳过 lifecycle 判定，lifecycle=null |
| 评分公式异常 | 自动回退到默认权重 0.25/0.25/0.25/0.25 |

---

## 7. 算法局限性

- ⚠️ search_index 数据可能受 SEO 影响，需结合 mention_count 校准
- ⚠️ 视频号公开数据有限，engagement_rate 主要来自公众号代理
- ⚠️ 冷启动阶段（< 10 词）归一化不稳定，建议手动初始化种子词库
- ⚠️ 中英文混合查询时，跨语言归一化未做（v1.1 优化）
