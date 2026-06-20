# Data Sources — 数据源配置

> 本文件定义 multi-agent-trend-ai 的所有数据源、接入方式、降级顺序与信号含义。
> 最后更新: 2026-06-20
> 架构版本: v1.1.1（4 个公众号生态官方源提升为主信号通道）

---

## 1. 数据源分层架构

```
┌─────────────────────────────────────────────────────────┐
│ Tier 1 · 主信号通道（公众号生态官方源）                   │
│   1. 微信搜一搜热词榜                                    │
│   2. 视频号创作者中心                                    │
│   3. 新榜公众号指数                                      │
│   4. 清博公众号数据                                      │
└─────────────────────┬───────────────────────────────────┘
                      ↓ (间接推论 / 降级)
┌─────────────────────────────────────────────────────────┐
│ Tier 2 · 跨平台信号源（公众号相关二级源）                 │
│   5. wechat.sogou.com (微信搜一搜网页版)                │
│   6. mp.weixin.qq.com  (公众号平台)                     │
│   7. channels.weixin.qq.com (视频号平台)                │
│   8. aihot.paicoding.com (跨平台 AI 聚合)              │
│   9. cloud.tencent.com.cn/developer/ (腾讯云)          │
│  10. zhuanlan.zhihu.com (知乎专栏)                      │
└─────────────────────┬───────────────────────────────────┘
                      ↓ (执行)
┌─────────────────────────────────────────────────────────┐
│ Tier 3 · 采集执行层                                      │
│  11. mmx search query (跨平台搜索)                       │
│  12. references/keyword-pool.md (本地历史库)             │
└─────────────────────────────────────────────────────────┘
```

> **关键设计**：Tier 1 是**信号语义定义**（代表"我们关心的公众号生态信号"），不一定是直接 API 接入；Tier 3 是**实际执行**（mmx + 本地库）。Tier 2 起到 Tier 1 与 Tier 3 之间的桥接作用。

---

## 2. Tier 1 · 主信号通道（公众号生态官方源）

| # | 信号通道 | URL / 接入点 | 抓取方式 | 信号含义 |
|---|---------|------------|---------|---------|
| 1 | **微信搜一搜热词榜** | weixin.sogou.com / 搜一搜 web 端 | WebFetch 热词面板 | 公众号搜索热度（用户主动查询行为） |
| 2 | **视频号创作者中心** | channels.weixin.qq.com 创作者端 | 创作者登录后控制台 | 视频号选题热度、爆款选题数据 |
| 3 | **新榜公众号指数** | newrank.cn / newrank.cn/publication | 公开榜单 + 商业 API | 公众号阅读 / 在看 / 点赞 / 10w+ 检测 |
| 4 | **清博公众号数据** | gsdata.cn / data.gsdata.cn | 公开榜单 + 商业 API | 公众号传播分析、WCI 指数 |

### 2.1 微信搜一搜热词榜

- **优先级**: 1
- **数据格式**: 热词列表 + 趋势指数
- **接入方式**:
  - 公开搜索：`https://weixin.sogou.com/weixin?type=2&query=AI%20Agent`
  - 抓取 `weixin.sogou.com` 的搜索建议下拉（用户输入框 focus 时显示）
- **降级路径**: 失败 → `mmx search query --q "weixin 搜一搜 热词 AI Agent"`
- **信号权重**: 0.30（最高，代表主动搜索需求）
- **更新频率**: 实时
- **API 可用性**: 无公开 API，需通过 WebFetch 抓页面或搜索建议

### 2.2 视频号创作者中心

- **优先级**: 2
- **数据格式**: 创作者后台的"热门选题" / "爆款视频"列表
- **接入方式**:
  - 创作者端：登录后访问 `channels.weixin.qq.com` 创作者中心
  - 公开替代：抓 `搜一搜视频号 tab` 的热门推荐
  - 第三方：`新榜视频号榜` / `清博视频号榜`
- **降级路径**: 失败 → `mmx search query --q "视频号 热门 AI Agent"`
- **信号权重**: 0.25
- **更新频率**: 日
- **API 可用性**: 创作者中心无公开 API；第三方榜单可抓

### 2.3 新榜公众号指数

- **优先级**: 3
- **数据格式**: 公众号文章阅读数、在看、点赞、10w+ 标记
- **接入方式**:
  - 公开榜单：`https://www.newrank.cn/publication/rank` (公开 Top 榜)
  - 商业 API：需 `NEWRANK_API_KEY`（付费，按调用计费）
- **降级路径**:
  - 无 API Key → 抓公开榜单的 top 50
  - 失败 → `mmx search query --q "新榜 公众号 AI Agent 10w+"`
- **信号权重**: 0.20
- **更新频率**: 日 / 实时（API 模式）
- **环境变量**: `NEWRANK_API_KEY`（可选）

### 2.4 清博公众号数据

- **优先级**: 4
- **数据格式**: 公众号传播指数（WCI）、阅读 / 在看 / 转发数据
- **接入方式**:
  - 公开榜单：`https://www.gsdata.cn/custom/wxRank`
  - 商业 API：需 `GSDATA_API_KEY`（付费，按月订阅）
- **降级路径**:
  - 无 API Key → 抓 WCI 公开榜
  - 失败 → `mmx search query --q "清博 公众号 AI Agent 传播"`
- **信号权重**: 0.15
- **更新频率**: 日
- **环境变量**: `GSDATA_API_KEY`（可选）

---

## 3. Tier 2 · 跨平台信号源

| # | 信号源 | URL | 类型 | 角色 |
|---|--------|-----|------|------|
| 5 | weixin.sogou.com | https://weixin.sogou.com/ | 微信内容搜索 | 公众号文章全文搜索（与 Tier 1.1 互补）|
| 6 | mp.weixin.qq.com | https://mp.weixin.qq.com/ | 公众号平台 | 创作者端，订阅 / 推送数据 |
| 7 | channels.weixin.qq.com | https://channels.weixin.qq.com/ | 视频号平台 | 视频号内容平台 |
| 8 | aihot.paicoding.com | https://aihot.paicoding.com/ | 跨平台 AI 聚合 | 每日跨平台 AI 热点（包含公众号文章）|
| 9 | cloud.tencent.com.cn/developer | https://cloud.tencent.com.cn/developer/ | 腾讯云开发者 | 视频号 / 微信生态技术动态 |
| 10 | zhuanlan.zhihu.com | https://zhuanlan.zhihu.com/ | 知乎专栏 | UGC 深度技术文章（公众号文章的镜像）|

> Tier 2 是 Tier 1 信号通道的**间接代理**。当 Tier 1 不可达时，通过 Tier 2 推论公众号生态热度。

---

## 4. Tier 3 · 采集执行层

### 4.1 mmx search query

- **实际执行**: 跨平台搜索，4 路并发
- **覆盖**: 公众号文章 / 视频号 / 知乎 / CSDN / 36kr 等
- **在数据流中的角色**: Tier 1 不可达时的**统一兜底**

### 4.2 references/keyword-pool.md

- **实际执行**: 本地历史关键词库（30 词，4 层分类）
- **覆盖**: 公众号热词的基线
- **在数据流中的角色**: 历史趋势的**对照基准**

---

## 5. 完整降级顺序

```
[Tier 1] 微信搜一搜热词榜
        ↓ 失败 (无 API Key / 抓取超时)
[Tier 1] 视频号创作者中心
        ↓ 失败
[Tier 1] 新榜公众号指数
        ↓ 失败
[Tier 1] 清博公众号数据
        ↓ 全部失败
[Tier 2] 跨平台聚合源 (Sogou / 36kr / 腾讯云 / 知乎 / aihot)
        ↓ 失败
[Tier 3] mmx search query (4 路并发)
        ↓ 失败
[Tier 3] references/keyword-pool.md (本地库，标 "可能过期")
        ↓ 失败
[END] 返回空结果 + 引导用户提供素材（不编造数据）
```

降级触发条件：
- Tier 1 全部 4 个源不可达 → 标记 `degraded_mode`，报告中明示"公众号生态官方源未直接接入，依赖跨平台推论"
- Tier 1 至少 1 个源可达 → 报告中标注具体接入情况

---

## 6. 鉴权与速率限制

### 6.1 公众号生态官方源

| 源 | 鉴权 | 速率限制 | 备注 |
|----|------|---------|------|
| 微信搜一搜热词榜 | 无 | 建议 ≤ 30 req/min | 公开页面抓取 |
| 视频号创作者中心 | 需创作者登录 | 严格限制 | 公开替代：搜一搜视频号 tab |
| 新榜公众号指数 | 公开榜单无；商业 API 需 Key | 公开：60 req/min | API：按调用计费 |
| 清博公众号数据 | 公开榜单无；商业 API 需 Key | 公开：30 req/min | API：按月订阅 |

### 6.2 环境变量（避免硬编码）

```bash
# .env (本地)
NEWRANK_API_KEY=your_key_here     # 新榜商业 API（可选）
GSDATA_API_KEY=your_key_here      # 清博商业 API（可选）
WECHAT_USER_AGENT="Mozilla/5.0 ..."  # 微信生态抓取 UA
WECHAT_REFERER="https://wx.qq.com/"  # 微信生态 Referer
```

> **安全声明**: 本 Skill 不收集任何 PII，密钥仅通过环境变量注入。

---

## 7. 抓取合规

- ✅ 仅做热度聚合与关键词提取
- ❌ 不存储公众号 / 视频号原文
- ❌ 不绕过登录墙（视频号创作者中心需登录，跳过）
- ✅ 遵守 robots.txt（默认）
- ❌ 不进行高频抓取（>5 req/s 触发熔断）
- ✅ 商业 API 优先于爬虫（避免侵权）

---

## 8. 数据源健康检查

每 24h 自动 ping 一次所有 Tier 1 + Tier 2 源，更新状态表：

| 源 | 上次成功 | 状态 | 备注 |
|----|---------|------|------|
| 微信搜一搜热词榜 | 2026-06-20 12:00 | ⏳ 待接入 | 需 WebFetch 实施 |
| 视频号创作者中心 | — | ⏳ 待接入 | 公开榜单替代 |
| 新榜公众号指数 | — | ⏳ 待接入 | 公开榜单可立即接入 |
| 清博公众号数据 | — | ⏳ 待接入 | 公开榜单可立即接入 |
| weixin.sogou.com | 2026-06-19 12:00 | ✅ healthy | - |
| aihot.paicoding.com | 2026-06-19 12:02 | ✅ healthy | - |
| mmx search | 2026-06-20 18:30 | ✅ healthy | 4 路并发 |

健康检查结果写入 `references/data-source-health.log`。

---

## 9. 接入路线图

### Phase 1 · 立即可接入（公开榜单）
- 新榜公开 Top 榜：抓 `newrank.cn/publication/rank` 的 top 50 公众号
- 清博 WCI 公开榜：抓 `gsdata.cn/custom/wxRank` 的 top 50 公众号
- 微信搜一搜热词下拉：抓 `weixin.sogou.com` 搜索建议

### Phase 2 · 第三方辅助
- 替代视频号创作者中心：抓搜一搜视频号 tab + 第三方视频号榜单
- 公众号全文检索：weixin.sogou.com 高级搜索

### Phase 3 · 商业 API
- 新榜 API（按调用计费）
- 清博 API（按月订阅）
- 西瓜助手（视频号专业数据）
