# 技能设计规格书 — multi-agent-trend-ai

> 输出时间: 2026-06-19  
> 设计角色: 设计师 Agent  
> 上游输入: `drafts/researcher-report.md`  
> 输出: 本规格书将作为 SKILL.md 与 references/ 的施工蓝图

---

## 1. Skill 元数据设计

```yaml
---
name: multi-agent-trend-ai
version: 1.0.0
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
  bilingual keyword coverage and refreshable heat scores.
metadata:
  hermes:
    domain: trend-research
    language: zh-CN
    output_format: markdown
    refresh_cycle: weekly
    data_sources:
      - wechat-search
      - wechat-mp
      - wechat-video
      - 36kr
      - paicoding-aihot
      - tencent-cloud-dev
      - zhihu-zhuanlan
    tier_colors:
      S: "#534AB7"
      A: "#185FA5"
      B: "#3B6D11"
      C: "#854F0B"
    dependencies:
      - tavily-mcp
      - python>=3.10
    safety:
      pii: none-collected
      secrets: env-only
---
```

---

## 2. 触发词设计

### 主触发词（4 个）
- 微信 AI 热门 / 公众号 AI 热门
- AI Agent 关键词调研
- 公众号 AI 选题
- 热度梯队 / AI 热词梯队

### 副触发词（10 个）
- 视频号 AI 趋势
- 小程序 AI 选题
- 搜一搜 AI 关键词
- 微信生态 AI 报告
- AI Agent 周报 / 月报
- WeChat AI keyword research
- AI Agent trend tier
- 公众号 选题建议
- AI 内容方向
- 智能体 关键词

### 否定触发词
- 抖音 / 小红书 / B 站趋势
- 海外 Twitter / Reddit trend
- 非 AI 领域（美妆/美食）趋势
- "什么是 AI Agent" 类概念问题
- 单纯润色 / 翻译请求

### 触发示例
- "帮我看看最近微信上有哪些 AI 热门词"
- "做一份 AI Agent 关键词调研报告"
- "我想做公众号 AI 内容，给我一些选题建议"
- "把这些 AI 词按热度梯队分一下"

---

## 3. 工作流设计

### 流程图
```
用户输入解析
    ↓
数据采集 (4 路并发)
    ↓
去重 / 标准化
    ↓
热度评分 (HeatScore 0-100)
    ↓
梯队分类 (S/A/B/C)
    ↓
可视化渲染 (条形图 + 标签云)
    ↓
选题生成 (2-3 条)
    ↓
失败日志写入 (如有)
```

### 节点规格

| 节点 | 工具 | 输入 | 输出 | 错误处理 |
|------|------|------|------|----------|
| 数据采集 | WebSearch + WebFetch | keyword_groups, time_range | RawHit[] | 单源失败 → 降级标记 |
| 去重标准化 | 内部逻辑 | RawHit[] | NormalizedTerm[] | 保留原词 |
| 热度评分 | 公式 | NormalizedTerm[] | ScoredTerm[] | 公式异常 → 用上周期分数 |
| 梯队分类 | 阈值规则 | ScoredTerm[] | TierBucket[] | 数量异常 → 强制等分 |
| 可视化渲染 | matplotlib + wordcloud | ScoredTerm[] | PNG + HTML | 不可用 → Markdown 表格 |
| 选题生成 | LLM + 模板 | TierBucket + user_background | TopicSuggestion[] | 模板缺失 → 基础 prompt |
| 失败日志 | Write append | 异常堆栈 | 追加 failure_case_log.md | 写失败 → 控制台告警 |

---

## 4. 输入输出契约

### 用户输入 Schema
```json
{
  "query": "string",
  "time_range": "7d | 30d | 90d | custom",
  "scope": ["mp", "video", "mini", "search"],
  "limit": 50,
  "tier_focus": ["S", "A", "B", "C"] | null,
  "language": "zh-CN | en-US"
}
```

### KeywordEntry (YAML)
```yaml
- id: mcp-protocol
  name_zh: MCP协议
  name_en: Model Context Protocol
  aliases: [MCP, Model Context Protocol]
  category: concept
  lifecycle: growth
  heat_score: 92
  tier: S
  signals:
    search_index: 18500
    mention_count: 12000
    article_count: 450
    engagement_rate: 0.082
  last_updated: 2026-06-19T00:00:00Z
  source_refs:
    - https://aihot.paicoding.com/
    - https://36kr.com/
```

### 最终输出 (Markdown)
```markdown
# 微信生态 AI Agent 热门关键词报告 (YYYY-MM-DD)

## 概览
- 总词数 / 覆盖时间 / 数据源

## 梯队分布表

## S 梯队（核心热点）— 详细词条
## A 梯队（高潜热点）
## B 梯队（稳定增长）
## C 梯队（长尾观察）

## 选题清单（2-3 条）
## 可视化
- 条形图 + 标签云
## 数据源声明
## 失败记录（如有）
```

---

## 5. 视觉规范

| 梯队 | 颜色 | 含义 |
|------|------|------|
| S | `#534AB7` | 核心热点（紫色） |
| A | `#185FA5` | 高潜热点（蓝色） |
| B | `#3B6D11` | 稳定增长（绿色） |
| C | `#854F0B` | 长尾观察（棕色） |

### 备用方案
- 降级 1: Markdown 表格 + ANSI 着色
- 降级 2: 纯文本 + `[S][A][B][C]` 前缀
- 降级 3: Mermaid 流程图

---

## 6. 关键词库结构

### 四层分类
| 层级 | 定义 | 示例 |
|------|------|------|
| concept | 基础理论与范式 | RAG、Agent、Prompt |
| framework | 工程框架与平台 | LangChain、CrewAI、Dify |
| application | 落地应用与场景 | AI 客服、智能助手 |
| emerging | 前沿探索方向 | MCP、A2A、Multi-Agent |

### 评分公式
```
heat_score = 0.30 * norm(search_index)
          + 0.30 * norm(mention_count)
          + 0.20 * norm(article_count)
          + 0.20 * norm(engagement_rate)
```

### 梯队阈值
- S ≥ 85
- 70 ≤ A < 85
- 55 ≤ B < 70
- C < 55

### 生命周期判定（4 周滚动增长率）
- introduction: > 50%
- growth: 10% ~ 50%
- maturity: -10% ~ 10%
- decline: < -10%

---

## 7. references/ 目录设计

| 文件 | 用途 |
|------|------|
| `data-sources.md` | 数据源配置 + 降级顺序 + 鉴权 |
| `keyword-pool.md` | 关键词库 YAML（按四层分类） |
| `heat-scoring.md` | 评分公式推导 + 归一化方法 |
| `topic-template.md` | 选题生成 prompt 模板 |
| `failure_case_log.md` | 失败案例日志（自我迭代） |
| `self-review-template.md` | 自我复盘模板（自我迭代） |
| `test_pool.md` | 测试用例池（≥ 8 个） |

---

## 8. 错误处理与降级

### 数据源降级顺序
```
1. wechat-search → 2. wechat-mp → 3. wechat-video
        ↓ 失败
4. paicoding-aihot / 36kr / tencent-cloud / zhihu
        ↓ 失败
5. keyword-pool.md 本地缓存（标注"可能过期"）
        ↓ 失败
6. 返回空结果 + 错误提示
```

### 关键词库过期
- `last_updated` 距今 > 14 天 → 标 `stale=true`
- 输出追加 `⚠️ 关键词库已过期 N 天`

### 可视化工具不可用
| 主方案 | 降级 1 | 降级 2 | 降级 3 |
|--------|--------|--------|--------|
| matplotlib 条形图 | Markdown + ANSI | 纯文本列表 | Mermaid |

---

## 9. 测试用例池（8 个）

### 基础功能（3）
- TC-01 完整调研流程
- TC-02 单梯队查询
- TC-03 中英双语输出

### 边界场景（3）
- TC-04 空查询
- TC-05 关键词库全空
- TC-06 阈值边界（85.0 → S）

### 错误恢复（2）
- TC-07 数据源全失败
- TC-08 可视化工具不可用

---

## 10. SKILL.md 章节映射

| 规格书章节 | SKILL.md 章节 |
|------------|---------------|
| 1. 元数据 | frontmatter |
| 2. 触发词 | When to Use |
| 3. 工作流 | Workflow |
| 4. 输入输出 | Inputs / Outputs |
| 5. 视觉规范 | Visualization |
| 6. 关键词库 | Keyword Pool |
| 8. 错误处理 | Error Handling |
| 7+9. references | References |
| 自我迭代 | Self-Iteration |

**SKILL.md 章节结构**:
```
# multi-agent-trend-ai
## When to Use
## Quick Start
## Workflow
## Inputs
## Outputs
## Visualization
## Keyword Pool
## Error Handling
## Self-Iteration
## References
```

---

**规格书完。** 已覆盖 hermes-agent-skill-authoring 全部 6 条标准。
