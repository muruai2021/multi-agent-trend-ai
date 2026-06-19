# 研究员 SOP 分析报告 — multi-agent-trend-ai

> 输出时间: 2026-06-19  
> 分析对象: `drafts/sop-draft-v0.md`  
> 分析角色: 研究员 Agent

---

## 1. SOP 业务理解

### 1.1 业务目标
1. **热度发现**：识别微信生态（公众号 + 视频号）当下 AI Agent 领域的热门关键词与流量词，按四梯队量化热度。
2. **趋势研判**：结合跨平台信号（技术社区、36氪、自媒体趋势站），判断 AI Agent 内容的上升 / 平稳 / 衰退态势。
3. **结构化输出**：以 Markdown 表格 + 可视化图表 + 选题建议的三段式交付物。
4. **创作辅助**：为公众号作者、视频号创作者提供 2-3 条高命中选题组合。
5. **持续追踪**：维护一份动态关键词库（概念层 / 框架层 / 应用层 / 新兴层）。

### 1.2 目标用户
- 主要：微信公众号作者、视频号 AI 创作者、AI 自媒体运营
- 次要：AI Agent 产品经理、内容策略师、创业团队内容负责人
- 核心痛点：信息分散，缺乏"微信生态专属"热度评估；技术热度≠内容热度，错失流量窗口

### 1.3 核心价值主张
> 把全网 AI Agent 噪音，蒸馏成微信生态创作者可直接落地的"热度梯队 + 选题配方"。

---

## 2. 关键节点拆解

| Step | 节点 | 输入 | 处理逻辑 | 输出 | 失败兜底 |
|------|------|------|----------|------|----------|
| 1 | 多源搜索关键词 | 调研主题 | 4 组并行 WebSearch | URL+标题+摘要 | 回退到预置关键词库 |
| 2 | 抓取高价值页面 | Step 1 URL 列表 | WebFetch 4 类页面 | 结构化摘要 | 单页失败跳过；>60% 失败终止 |
| 3 | 整理热度梯队 | Step 2 摘要 | 按四档归类 + evidence | 梯队表 | 证据不足标"待观察" |
| 4 | 可视化输出 | 梯队表 | show_widget 双视图 | bar + tag_cloud | 回退 ASCII + Markdown |
| 5 | 选题建议 | 梯队 + 用户背景 | 组合 2-3 条 | 选题清单 | 背景缺失→通用版 |

节点依赖: `Step 1 → 2 → 3 → 4/5`，Step 4 与 Step 5 可并行。

---

## 3. 输入输出契约

### 3.1 必需输入
- `topic` (string, 默认 `AI Agent`)
- `target_platform` (enum: 公众号 / 视频号 / 两者)
- `time_window` (enum: 当日 / 本周 / 本月 / 本季)

### 3.2 可选输入
- `user_background` (string)
- `exclude_keywords` (list)
- `focus_vertical` (string, 垂直领域)
- `deliverable_format` (enum: md / json / html / md+chart)
- `top_n` (int, 默认 20)
- `refresh_keyword_lib` (bool)

### 3.3 输出物
- `tier_table` (object: tier1~4, 含 keywords[]、evidence[])
- `visualization` (object: bar_chart, tag_cloud)
- `topic_suggestions` (array: 2-3 条选题)
- `data_sources` (array: URL 列表)
- `confidence` (enum: high/medium/low)
- `timestamp` (ISO8601)
- `keyword_lib_diff` (object: 新增/退出)

---

## 4. 边界场景（10 项）

| # | 场景 | 降级策略 |
|---|------|----------|
| 1 | 关键词热度衰减 | 从词库替补同梯队新词 |
| 2 | 数据源全部不可达 | 引导用户提供素材，不编造 |
| 3 | 视频号数据缺失 | 标注"推论值" |
| 4 | 跨梯队冲突 | 保留最高梯队，加注 cross-tier |
| 5 | 垂直领域冷门 | 降级到通用版 + 提示 |
| 6 | 选题建议雷同 | 引入"反共识"逆向选题 |
| 7 | 可视化工具不可用 | ASCII 条形图 + 文字标签云 |
| 8 | 关键词库与现实脱节 (>40%) | 实时数据为准，词库进队列 |
| 9 | LLM 幻觉污染 | 每条梯队词至少 1 个 evidence URL |
| 10 | 平台政策变化 | 剔除失效源，重平衡权重 |

---

## 5. 数据源评估

| 数据源 | 可靠性 | 更新频率 | 风险 |
|--------|--------|----------|------|
| PaiCoding AI热点雷达 | 中 | 日 | 个人维护，可能停更 |
| 36氪 AI专题 | 高 | 日 | 偏 B 端，缺微信创作者视角 |
| 花叔AI自媒体趋势 | 中 | 月/季 | 更新慢，覆盖 2025-2026 |
| 腾讯云开发者社区 | 高 | 日 | 偏开发者视角 |
| 知乎专栏 AI Agent | 中 | 日 | 噪声大，需筛选 |

**核心缺口**: 仅腾讯云覆盖"视频号/微信生态"原生信号。

**建议补充**:
1. 新榜 / 清博 / 西瓜助手 — 微信生态真实阅读量
2. 微信指数 — 官方热度金本位
3. 微博/抖音/小红书热搜 — 全网共振度校验
4. 百度指数 / Google Trends — 时序对比
5. GitHub Trending + Hugging Face — 框架层开发者热度
6. AI 公众号 Top 100 榜单 — 同行在写什么

---

## 6. 风险与依赖

| 维度 | 风险 | 缓解 |
|------|------|------|
| WebSearch | API 限流 | 多组并行 + 失败回退 |
| WebFetch | 反爬/robots | 多源冗余 + 超时熔断 |
| show_widget | 未上线 | ASCII 回退 |
| 时效性 | 词热度半衰期 < 7 天 | 7 天后自动标"建议复检" |
| 标准化 | 多源指标无法直接相加 | 内部 HeatScore 0-100 + 公开换算 |
| 合规 | 抓公众号可能违 ToS | 仅做热度聚合，不存原文 |
| 幻觉 | LLM 把旧知识当今日热度 | evidence URL 强制约束 |

---

## 7. 可拆分性评估

**强烈建议拆分**为 5 个子 Skill:

```
trend-keyword-lib (数据底座)
        ▲
        │
trend-keyword-scraper ──► trend-keyword-tierer ──► trend-keyword-visualizer
                                              │
                                              ▼
                                   trend-topic-suggester
```

| 子 Skill | 职责 | 可复用给 |
|---------|------|---------|
| trend-keyword-scraper | Step 1+2 多源搜索抓取 | 任意趋势调研 |
| trend-keyword-tierer | Step 3 四梯队归类 | 跨主题复盘 |
| trend-keyword-visualizer | Step 4 可视化 | 任意热度图 |
| trend-topic-suggester | Step 5 选题生成 | 内容生产类 |
| trend-keyword-lib | 关键词库 CRUD | 上游 4 个 Skill |

> **v0.1 决策**: 因当前 SOP 边界尚不固定，先用单 Skill 内多阶段实现，待使用 ≥ 3 次后按节点拆分为子 Skill。

---

## 8. 草案关键缺口（v0.1 须补齐）

1. 梯队归类规则缺可操作判定标准
2. 数据源权重未定义
3. evidence 强制约束缺失
4. 可视化降级路径未明示
5. confidence 计算未公式化
6. 关键词库版本号缺失

---

**报告结论**: SOP 业务价值清晰、流程闭环完整；主要短板在标准化、证据约束、视觉降级和子能力可复用性。
