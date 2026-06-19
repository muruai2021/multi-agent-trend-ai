---
name: multi-agent-trend-ai
version: 1.1.0
author: multi-agent-skills-factory
license: Apache-2.0
platforms:
  - claude-code
  - hermes-agent
description: |
  Use when the user needs to research trending AI Agent keywords within the
  WeChat ecosystem (公众号 / 视频号 / 小程序 / 搜一搜), classify them into four
  heat tiers (S/A/B/C), and produce topic suggestions for content creators.
  Triggers on requests like "微信 AI 热门关键词", "公众号 AI 选题",
  "WeChat AI Agent 趋势", "AI Agent 热度梯队", "视频号 AI 内容方向",
  "小程序 AI 选题建议". Supports Chinese content strategy workflows with
  bilingual keyword coverage and refreshable heat scores. Default output is
  a self-contained HTML report saved to the current working directory, with
  strict content-quality constraints (no first-person in topics, real evidence
  only, every topic must have explicit selection logic).
metadata:
  hermes:
    domain: trend-research
    language: zh-CN
    output_format: html
    output_path: current-directory
    refresh_cycle: weekly
    data_sources:
      - wechat-search
      - wechat-mp
      - wechat-video
      - 36kr
      - paicoding-aihot
      - tencent-cloud-dev
      - zhihu-zhuanlan
      - mmx-search
    tier_colors:
      S: "#534AB7"
      A: "#185FA5"
      B: "#3B6D11"
      C: "#854F0B"
    dependencies:
      - mmx-cli
      - python>=3.10
    content_constraints:
      no_first_person_in_topics: true
      evidence_required: true
      topic_logic_required: true
    safety:
      pii: none-collected
      secrets: env-only
---

# multi-agent-trend-ai

> 调研微信生态（公众号 + 视频号 + 小程序 + 搜一搜）AI Agent 热门关键词与内容趋势，按 S/A/B/C 四梯队输出热度分级、关键词解读、可视化图表及内容选题建议。

## When to Use

### ✅ 主触发词
- 微信 AI 热门 / 公众号 AI 热门
- AI Agent 关键词调研
- 公众号 AI 选题
- 热度梯队 / AI 热词梯队

### ✅ 副触发词
- 视频号 AI 趋势
- 小程序 AI 选题
- 搜一搜 AI 关键词
- 微信生态 AI 报告
- AI Agent 周报 / 月报
- WeChat AI keyword research
- AI Agent trend tier
- AI 智能体 关键词
- 公众号 选题建议
- AI 内容方向

### ❌ 不触发
- 抖音 / 小红书 / B 站 / Twitter 趋势
- 非 AI 领域（美妆、美食等）趋势
- "什么是 AI Agent" 概念问题
- 单纯润色 / 翻译请求

### 触发示例
- "帮我看看最近微信上有哪些 AI 热门词"
- "做一份 AI Agent 关键词调研报告，时间范围 30 天"
- "我想做公众号 AI 内容，给我一些选题建议"
- "把这些 AI 词按热度梯队分一下"
- "WeChat AI Agent trend report, 7 days"

---

## Quick Start

```
用户: "做一份 AI Agent 关键词调研报告，30 天范围，公众号+视频号"
        ↓
主编调度 7 步流水线
        ↓
输出: trend-report-YYYY-MM-DD.html (自包含 HTML，存到当前目录)
```

典型执行时长: 30-60 秒（含 4 路并发搜索）

### 内容质量约束（强制）

1. **不编造案例** — 每个 evidence URL 必须来自当次 mmx search query 返回的 organic 结果，或 keyword-pool.md 的 source_refs
2. **选题不用第一人称** — 标题与大纲中不出现"我"、"我们"；改为客观描述（"14 天复盘"而非"我用 Claude Code 的 14 天"）
3. **选题逻辑必须有依据** — 每条选题必须显式列出：组合的热度分数、生命周期互补性、数据信号、受众/事件锚点
4. **反共识选题要有原文支撑** — 不可凭空"逆向"，必须从 mmx 搜索结果中找到原文事实作为反共识支点

---

## Workflow

```
┌─────────────────────────────────────┐
│ Step 1 · 用户输入解析                │
│ - 提取: topic, time_range, scope     │
│ - 加载: keyword-pool.md (本地库)     │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│ Step 2 · 多源数据采集（4 路并发）     │
│ - WebSearch: 4 组关键词并行          │
│ - WebFetch: 抓取高价值页面           │
│ - 降级顺序见 Error Handling          │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│ Step 3 · 去重 + 标准化               │
│ - 同义词合并（按 aliases）           │
│ - 中英双语归一                       │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│ Step 4 · 热度评分 (HeatScore 0-100)  │
│ - 公式: 0.30·search + 0.30·mention  │
│        + 0.20·article + 0.20·engage  │
│ - 详见 references/heat-scoring.md    │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│ Step 5 · 梯队分类 (S/A/B/C)          │
│ - S ≥ 85, 70 ≤ A < 85               │
│ - 55 ≤ B < 70, C < 55               │
│ - evidence URL 强制 ≥ 1             │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│ Step 6 · 可视化 + 选题生成（并行）   │
│ - 横向条形图 + 标签云（4 色）        │
│ - 选题 2-3 条（结合用户背景）        │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│ Step 7 · 失败日志写入（如有）        │
│ - 追加到 references/failure_case_log │
└─────────────────────────────────────┘
```

### 步骤详解

#### Step 1 · 用户输入解析
- 必需参数: `topic`（默认 `AI Agent`）, `time_window`（7d/30d/90d/custom）, `target_platform`（公众号/视频号/两者）
- 可选参数: `user_background`, `exclude_keywords`, `focus_vertical`, `top_n`, `deliverable_format`
- 加载本地关键词库 `references/keyword-pool.md` 作为 baseline

#### Step 2 · 多源数据采集

**4 组并发 WebSearch 关键词**（每组最多 5 个）：

| 组 | 关键词 | 用途 |
|----|--------|------|
| 1 | AI agent 公众号 热门 2026 / 智能体 公众号 趋势 / AI Agent 微信生态 / 公众号 AI 选题 / 微信 AI 内容 | 通用趋势 |
| 2 | 视频号 AI智能体 热搜词 / 视频号 AI Agent 流量 / 视频号 智能体 爆款 / 视频号 AI 教程 / 视频号 AI 实战 | 视频号专项 |
| 3 | MCP A2A Multi-Agent 公众号热度 / MCP协议 公众号 / Agent-to-Agent 视频号 / Vibe Coding 公众号 / AG-UI 趋势 | 技术热点 |
| 4 | AI Agent 爆款选题 公众号 / AI 选题 视频号 / AI Agent 流量词 / 公众号 10w+ AI / 视频号 AI 涨粉 | 创作者视角 |

**WebFetch 高价值页面**：
1. AI 热点雷达 (https://aihot.paicoding.com/) — 每日跨平台聚合
2. 36 氪 AI 专题 (https://36kr.com/) — 行业趋势 + 资本动向
3. 花叔 AI 自媒体趋势 (https://www.huasheng.ai/insights/ai-content-trends-2025-2026/) — 自媒体内容方向
4. 腾讯云开发者社区 (https://cloud.tencent.com.cn/developer/) — 视频号 / 微信生态动态
5. 知乎专栏 AI Agent 合集 (https://zhuanlan.zhihu.com/) — 技术深度文章

#### Step 3 · 去重 + 标准化
- aliases 重叠词条合并
- 中英别名统一为 id（如 `mcp-protocol`）
- 同义词归并（"MCP协议" = "Model Context Protocol" = "MCP"）

#### Step 4 · 热度评分
详见 `references/heat-scoring.md`：
```
heat_score = 0.30 * norm(search_index)
          + 0.30 * norm(mention_count)
          + 0.20 * norm(article_count)
          + 0.20 * norm(engagement_rate)
```

#### Step 5 · 梯队分类
| 梯队 | 标准 | 典型来源 | 颜色 |
|------|------|---------|------|
| S | 公众号+视频号双爆，搜索指数极高 | MCP协议、Multi-Agent、Vibe Coding | #534AB7 紫 |
| A | 技术社区高热，持续稳定 | CrewAI、LangGraph、Dify、Claude Code | #185FA5 蓝 |
| B | 应用场景快速上升 | AI客服Agent、微信内置AI、AutoGPT 2.0 | #3B6D11 绿 |
| C | 新兴潜力方向 | Agent Swarm、端侧Agent、具身智能、Context Engineering | #854F0B 橙 |

**强制约束**：每条梯队词必须挂 ≥ 1 个 evidence URL，否则移入"待观察"区。

#### Step 6 · 可视化 + 选题生成

**可视化方案**：
- **主视图**: 横向条形图（X = heat_score, Y = keywords 分组）+ 标签云（字号 ∝ heat_score, 颜色 = 梯队色）
- **降级 1**: Markdown 表格 + ANSI 着色
- **降级 2**: 纯文本列表 + `[S][A][B][C]` 前缀
- **降级 3**: Mermaid 横向流程图

**选题生成**（详见 `references/topic-template.md`）：

| # | 关键词组合 | 目标平台 | 内容形态 |
|---|-----------|---------|---------|
| 1 | MCP + 多 Agent 协作流水线实战 | 公众号 | 深度长文 + 代码示例 |
| 2 | Vibe Coding + 企业级 Agent 落地案例 | 公众号 + 视频号 | 案例拆解 + 实拍演示 |
| 3 | 微信内置 AI Agent + 电商客服场景 | 视频号 | 30s 短视频 + 脚本 |

---

## Inputs

### 必需参数
| 字段 | 类型 | 说明 | 默认 |
|------|------|------|------|
| `topic` | string | 调研主题 | `AI Agent` |
| `target_platform` | enum | `公众号` / `视频号` / `两者` | `两者` |
| `time_window` | enum | `当日` / `本周` / `本月` / `本季` | `本周` |

### 可选参数
| 字段 | 类型 | 默认 | 说明 |
|------|------|------|------|
| `user_background` | string | `通用` | 用户身份（开发者/写作者/运营/PM） |
| `exclude_keywords` | list | `[]` | 排除词 |
| `focus_vertical` | string | - | 垂直领域（电商/教育/客服/医疗） |
| `deliverable_format` | enum | `html` | `md` / `json` / `html` |
| `top_n` | int | 20 | 返回词数上限 |
| `refresh_keyword_lib` | bool | `false` | 是否同步刷新关键词库 |

---

## Outputs

### 默认输出：自包含 HTML（当前目录）

文件名: `trend-report-YYYY-MM-DD.html`
保存位置: **当前工作目录**（不是 `outputs/` 子目录）
特性: 嵌入 CSS，无外部依赖；CSS 横向条形图（matplotlib 不可用时降级 1）；梯队配色 #534AB7 / #185FA5 / #3B6D11 / #854F0B

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <style>...tier colors + CSS bar chart...</style>
</head>
<body>
  <header>微信生态 AI Agent 热门关键词报告 · 2026-06-20</header>
  <section>概览（4 个统计卡）</section>
  <section>横向条形图（28 词）</section>
  <section>S / A / B / C 梯队详情</section>
  <section>选题清单（4 条，每条含 evidence + 选题逻辑）</section>
  <section>数据源 + 失败记录</section>
  <section>发布建议 + 选题分发节奏</section>
</body>
</html>
```

### 选题清单内容契约

每条选题必须包含以下 5 个字段：
1. **关键词组合** — 列出所用梯队词 + 分数
2. **选题逻辑** — 4 个 bullet：热度支撑 / 生命周期互补 / 数据信号 / 受众基础
3. **大纲** — 5 个章节
4. **Evidence** — ≥ 2 个真实 URL（来自当次 mmx search 的 organic 结果或 keyword-pool.md source_refs）
5. **预估热度** — 基于 S/A/B 分数加权的明确数字

### 可选输出
- `json`: 完整结构化数据（存到 `outputs/trend-data-YYYY-MM-DD.json`）
- `md`: 纯文本备用（存到 `outputs/trend-report-YYYY-MM-DD.md`）
- `html`: 单文件可视化报告

---

## Visualization

### 配色规范（强制沿用）

| 梯队 | 颜色 | 含义 |
|------|------|------|
| S | `#534AB7` | 核心热点（紫色） |
| A | `#185FA5` | 高潜热点（蓝色） |
| B | `#3B6D11` | 稳定增长（绿色） |
| C | `#854F0B` | 长尾观察（棕色） |

### 主视图: 双视图
1. **横向条形图** (matplotlib)
   - X 轴: 热度评分 (0-100)
   - Y 轴: 关键词（按梯队分组）
   - 颜色: 梯队上色
2. **标签云** (wordcloud)
   - 字号 ∝ heat_score
   - 颜色 = 梯队配色
   - 中英双语同图

### 降级路径
| 工具状态 | 降级 1 | 降级 2 | 降级 3 |
|---------|--------|--------|--------|
| matplotlib 不可用 | Markdown 表格 + ANSI | 纯文本列表 | Mermaid 流程图 |
| wordcloud 不可用 | HTML `<span>` 字号 | 纯文本 | 跳过 |

---

## Keyword Pool

详细字段定义与维护策略见 `references/keyword-pool.md` 与 `references/heat-scoring.md`。

### 四层分类
| 层级 | 定义 | 当前代表词 |
|------|------|-----------|
| concept (概念) | 基础理论与范式 | MCP协议、A2A协议、AG-UI、Multi-Agent、Agent Workflow |
| framework (框架) | 工程框架与平台 | CrewAI、LangChain、LangGraph、Dify、Coze、Claude Code、Cursor |
| application (应用) | 落地应用与场景 | AI 客服 Agent、内容生成 Pipeline、微信内置 AI Agent、企业级 Agent |
| emerging (新兴) | 前沿探索方向 | Agent Swarm、具身智能、端侧 Agent、Context Engineering、Agent 记忆管理 |

### 维护策略
- **更新周期**: 每周日凌晨 03:00 自动重算 heat_score
- **梯队阈值**: S≥85, 70≤A<85, 55≤B<70, C<55
- **生命周期**: introduction (>50% 4 周增长率), growth (10-50%), maturity (-10~10%), decline (<-10%)

---

## Error Handling

### 数据源降级顺序
```
1. wechat-search (主)
        ↓ 失败
2. wechat-mp (公众号热门)
        ↓ 失败
3. wechat-video (视频号热门)
        ↓ 失败
4. paicoding-aihot / 36kr / tencent-cloud / zhihu (跨平台聚合)
        ↓ 失败
5. references/keyword-pool.md 本地缓存（标注"可能过期"）
        ↓ 失败
6. 返回空结果 + 引导用户提供素材
```

### 错误处理矩阵

| 错误类型 | 触发条件 | 行为 |
|---------|---------|------|
| 关键词热度衰减 | 核心词搜索结果数环比下滑 >50% | 标"热度下行"，从词库替补 |
| 数据源全部不可达 | 5 个源 WebFetch 全部失败 | 立即停止，不编造数据 |
| 视频号数据缺失 | 视频号无公开热度 API | 仅基于公众号 + 间接信号估算，标注"推论值" |
| 跨梯队冲突 | 词同时出现在多个梯队 | 保留最高梯队，加注 cross-tier |
| 垂直领域冷门 | focus_vertical 长尾 | 降级到通用版 + 提示 |
| 选题建议雷同 | 多轮产出相同 2-3 条 | 引入 1 条逆向选题 |
| 可视化工具不可用 | matplotlib 导入失败 | 降级到 Markdown + ANSI |
| 关键词库脱节 | 库中 >40% 词不在 Top 100 | 实时数据为准，词库进队列 |
| LLM 幻觉 | 词条缺 evidence URL | 移入"待观察"区 |
| 平台政策变化 | 微信封锁抓取 / 站点改版 | 剔除失效源，重平衡权重 |

### 关键词库过期
- `last_updated` 距今 > 14 天 → 标 `stale=true`
- 输出追加 `⚠️ 关键词库已过期 N 天，建议刷新`

---

## Self-Iteration

本 Skill 内置自我迭代机制，由 `references/failure_case_log.md` 和 `references/self-review-template.md` 驱动。

### 错误案例日志

每次使用出现错误时，记录到 `references/failure_case_log.md`：

| 字段 | 说明 |
|------|------|
| 日期 | YYYY-MM-DD |
| 触发词 | 用户原始 query |
| 错误类型 | 搜索失败 / 抓取超时 / 可视化失败 / 评分异常 / 幻觉 |
| 错误输出 | 实际产出 |
| 正确预期 | 应有产出 |
| 根因分析 | 一句话定位 |
| 修复状态 | 待修复 / 已修复 / 已转回归 |
| 修复人/版本 | - |

### 触发条件
- 未修复 ≥ 5 条 → 自动触发复盘迭代
- 同一触发词出现 ≥ 3 次 → 判定为复发性错误（立即修复）

### 自我复盘流程
1. 运行 `python scripts/analyze_failures.py . --auto` 检测触发条件
2. 按优先级生成改进建议（P0/P1/P2）
3. 更新 SKILL.md
4. 回归测试验证（`test_pool.md`）

### 加分项（评审时）
- 有错误日志且 ≥ 3 条记录: +3
- 有自我复盘报告且有改进措施: +3
- 已修复案例进入回归测试池: +2
- 最近 30 天无新增错误: +2

---

## References

| 文件 | 用途 |
|------|------|
| [references/data-sources.md](references/data-sources.md) | 数据源配置 + 降级顺序 + 鉴权 |
| [references/keyword-pool.md](references/keyword-pool.md) | 关键词库 YAML（按四层分类） |
| [references/heat-scoring.md](references/heat-scoring.md) | 评分公式推导 + 归一化方法 |
| [references/topic-template.md](references/topic-template.md) | 选题生成 prompt 模板 |
| [references/failure_case_log.md](references/failure_case_log.md) | 失败案例日志（自我迭代） |
| [references/self-review-template.md](references/self-review-template.md) | 自我复盘模板（自我迭代） |
| [references/test_pool.md](references/test_pool.md) | 测试用例池（≥ 8 个） |

### 设计文档（追溯）
- [drafts/sop-draft-v0.md](drafts/sop-draft-v0.md) — 原始 SOP 草稿
- [drafts/researcher-report.md](drafts/researcher-report.md) — 研究员分析报告
- [drafts/design-spec-v1.md](drafts/design-spec-v1.md) — 设计师规格书

---

## Validation Checklist

运行 `python scripts/validate_skill.py .` 自动验证（推荐）或手动检查：

- [x] description 以 "Use when" 开头
- [x] frontmatter 含 name/description/version/author/license/platforms/metadata.hermes
- [x] description ≤ 1024 字符
- [x] references/ 目录存在（正文 > 8KB）
- [x] test_pool.md 命名正确
- [x] 无硬编码敏感信息
- [x] 覆盖 6 个工作流节点（输入解析/采集/标准化/评分/分类/可视化/选题）
- [x] 自我迭代机制完整（failure_case_log + self-review-template）
