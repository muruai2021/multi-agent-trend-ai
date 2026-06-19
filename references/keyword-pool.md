# Keyword Pool — 关键词库

> 本文件维护 multi-agent-trend-ai 的核心关键词库，按四层分类（concept/framework/application/emerging）。
> 最后更新: 2026-06-19
> 维护周期: 每周日凌晨 03:00 自动重算 heat_score

---

## 库结构 (YAML)

```yaml
- id: <slug>
  name_zh: <中文名>
  name_en: <English Name>
  aliases: [<同义词列表>]
  category: concept | framework | application | emerging
  lifecycle: introduction | growth | maturity | decline
  heat_score: 0-100
  tier: S | A | B | C
  signals:
    search_index: <int>
    mention_count: <int>
    article_count: <int>
    engagement_rate: <float 0-1>
  last_updated: <ISO8601>
  source_refs:
    - <evidence URL 1>
    - <evidence URL 2>
```

---

## 当前词库

### 概念层 (concept)

```yaml
- id: mcp-protocol
  name_zh: MCP协议
  name_en: Model Context Protocol
  aliases: [MCP, Model Context Protocol, 上下文协议]
  category: concept
  lifecycle: growth
  heat_score: 92
  tier: S
  signals:
    search_index: 18500
    mention_count: 12000
    article_count: 450
    engagement_rate: 0.082
  last_updated: 2026-06-19T03:00:00Z
  source_refs:
    - https://aihot.paicoding.com/
    - https://36kr.com/information/AI

- id: a2a-protocol
  name_zh: A2A协议
  name_en: Agent-to-Agent
  aliases: [A2A, Agent-to-Agent, 智能体间通信]
  category: concept
  lifecycle: growth
  heat_score: 78
  tier: A
  signals:
    search_index: 9200
    mention_count: 6100
    article_count: 220
    engagement_rate: 0.065
  last_updated: 2026-06-19T03:00:00Z
  source_refs:
    - https://36kr.com/
    - https://cloud.tencent.com.cn/developer/

- id: ag-ui
  name_zh: AG-UI
  name_en: Agent User Interface
  aliases: [AG-UI, Agent UI, 智能体界面]
  category: concept
  lifecycle: introduction
  heat_score: 58
  tier: B
  signals:
    search_index: 3200
    mention_count: 2100
    article_count: 78
    engagement_rate: 0.041
  last_updated: 2026-06-19T03:00:00Z
  source_refs:
    - https://zhuanlan.zhihu.com/

- id: multi-agent
  name_zh: Multi-Agent 多智能体协作
  name_en: Multi-Agent Collaboration
  aliases: [多智能体, Multi-Agent, 多 Agent 协作]
  category: concept
  lifecycle: growth
  heat_score: 88
  tier: S
  signals:
    search_index: 15600
    mention_count: 10800
    article_count: 380
    engagement_rate: 0.075
  last_updated: 2026-06-19T03:00:00Z
  source_refs:
    - https://aihot.paicoding.com/
    - https://36kr.com/

- id: agent-workflow
  name_zh: Agent Workflow 工作流编排
  name_en: Agent Workflow Orchestration
  aliases: [Agent工作流, 智能体编排, Workflow编排]
  category: concept
  lifecycle: growth
  heat_score: 72
  tier: A
  signals:
    search_index: 7800
    mention_count: 5200
    article_count: 180
    engagement_rate: 0.058
  last_updated: 2026-06-19T03:00:00Z
  source_refs:
    - https://cloud.tencent.com.cn/developer/
```

### 框架层 (framework)

```yaml
- id: crewai
  name_zh: CrewAI
  name_en: CrewAI
  aliases: [CrewAI, Crew AI]
  category: framework
  lifecycle: growth
  heat_score: 75
  tier: A
  signals:
    search_index: 8400
    mention_count: 5600
    article_count: 210
    engagement_rate: 0.062
  last_updated: 2026-06-19T03:00:00Z
  source_refs:
    - https://github.com/joaomdmoura/crewAI
    - https://36kr.com/

- id: langchain
  name_zh: LangChain
  name_en: LangChain
  aliases: [LangChain, Lang Chain]
  category: framework
  lifecycle: maturity
  heat_score: 80
  tier: A
  signals:
    search_index: 11200
    mention_count: 7800
    article_count: 320
    engagement_rate: 0.068
  last_updated: 2026-06-19T03:00:00Z
  source_refs:
    - https://github.com/langchain-ai/langchain
    - https://36kr.com/

- id: langgraph
  name_zh: LangGraph
  name_en: LangGraph
  aliases: [LangGraph, Lang Graph]
  category: framework
  lifecycle: growth
  heat_score: 73
  tier: A
  signals:
    search_index: 7600
    mention_count: 5100
    article_count: 190
    engagement_rate: 0.060
  last_updated: 2026-06-19T03:00:00Z
  source_refs:
    - https://github.com/langchain-ai/langgraph
    - https://cloud.tencent.com.cn/developer/

- id: dify
  name_zh: Dify
  name_en: Dify
  aliases: [Dify, Dify.AI]
  category: framework
  lifecycle: growth
  heat_score: 71
  tier: A
  signals:
    search_index: 6800
    mention_count: 4500
    article_count: 165
    engagement_rate: 0.055
  last_updated: 2026-06-19T03:00:00Z
  source_refs:
    - https://github.com/langgenius/dify
    - https://36kr.com/

- id: coze
  name_zh: Coze 平台
  name_en: Coze Platform
  aliases: [Coze, 扣子, 字节 Coze]
  category: framework
  lifecycle: growth
  heat_score: 70
  tier: A
  signals:
    search_index: 6500
    mention_count: 4200
    article_count: 155
    engagement_rate: 0.053
  last_updated: 2026-06-19T03:00:00Z
  source_refs:
    - https://www.coze.cn/
    - https://36kr.com/

- id: autogpt-v2
  name_zh: AutoGPT 2.0
  name_en: AutoGPT 2.0
  aliases: [AutoGPT, Auto GPT 2.0, Auto-GPT]
  category: framework
  lifecycle: maturity
  heat_score: 62
  tier: B
  signals:
    search_index: 4800
    mention_count: 3200
    article_count: 110
    engagement_rate: 0.048
  last_updated: 2026-06-19T03:00:00Z
  source_refs:
    - https://github.com/Significant-Gravitas/AutoGPT
    - https://zhuanlan.zhihu.com/

- id: claude-code
  name_zh: Claude Code
  name_en: Claude Code
  aliases: [Claude Code, Anthropic Claude Code]
  category: framework
  lifecycle: growth
  heat_score: 82
  tier: A
  signals:
    search_index: 12800
    mention_count: 8400
    article_count: 280
    engagement_rate: 0.072
  last_updated: 2026-06-19T03:00:00Z
  source_refs:
    - https://docs.claude.com/claude-code
    - https://36kr.com/

- id: cursor
  name_zh: Cursor
  name_en: Cursor IDE
  aliases: [Cursor, Cursor Editor, Cursor AI]
  category: framework
  lifecycle: growth
  heat_score: 78
  tier: A
  signals:
    search_index: 9800
    mention_count: 6500
    article_count: 230
    engagement_rate: 0.064
  last_updated: 2026-06-19T03:00:00Z
  source_refs:
    - https://cursor.com/
    - https://36kr.com/

- id: codex
  name_zh: Codex
  name_en: OpenAI Codex
  aliases: [Codex, OpenAI Codex, GPT Codex]
  category: framework
  lifecycle: maturity
  heat_score: 65
  tier: B
  signals:
    search_index: 5200
    mention_count: 3500
    article_count: 120
    engagement_rate: 0.050
  last_updated: 2026-06-19T03:00:00Z
  source_refs:
    - https://openai.com/index/openai-codex/
    - https://36kr.com/
```

### 应用层 (application)

```yaml
- id: ai-customer-service
  name_zh: AI 客服 Agent
  name_en: AI Customer Service Agent
  aliases: [AI客服, 智能客服, AI 客服 Agent]
  category: application
  lifecycle: growth
  heat_score: 67
  tier: B
  signals:
    search_index: 6100
    mention_count: 4200
    article_count: 165
    engagement_rate: 0.052
  last_updated: 2026-06-19T03:00:00Z
  source_refs:
    - https://36kr.com/
    - https://cloud.tencent.com.cn/developer/

- id: content-pipeline
  name_zh: 内容生成 Pipeline
  name_en: Content Generation Pipeline
  aliases: [内容生成, Content Pipeline, AI 写作流水线]
  category: application
  lifecycle: growth
  heat_score: 64
  tier: B
  signals:
    search_index: 5300
    mention_count: 3600
    article_count: 130
    engagement_rate: 0.049
  last_updated: 2026-06-19T03:00:00Z
  source_refs:
    - https://huasheng.ai/insights/ai-content-trends-2025-2026/
    - https://36kr.com/

- id: wechat-builtin-ai
  name_zh: 微信内置 AI Agent
  name_en: WeChat Built-in AI Agent
  aliases: [微信AI, 微信智能体, WeChat AI]
  category: application
  lifecycle: introduction
  heat_score: 70
  tier: A
  signals:
    search_index: 7200
    mention_count: 4800
    article_count: 175
    engagement_rate: 0.061
  last_updated: 2026-06-19T03:00:00Z
  source_refs:
    - https://cloud.tencent.com.cn/developer/
    - https://36kr.com/
  # 注: 2026年6月新增热点

- id: enterprise-agent
  name_zh: Agent 落地 / 企业级应用
  name_en: Enterprise Agent Adoption
  aliases: [企业级Agent, Agent落地, Enterprise Agent]
  category: application
  lifecycle: growth
  heat_score: 68
  tier: B
  signals:
    search_index: 6300
    mention_count: 4300
    article_count: 160
    engagement_rate: 0.054
  last_updated: 2026-06-19T03:00:00Z
  source_refs:
    - https://36kr.com/
```

### 新兴层 (emerging)

```yaml
- id: agent-swarm
  name_zh: Agent Swarm 蜂群
  name_en: Agent Swarm
  aliases: [Agent Swarm, 智能体蜂群, Swarm Agent]
  category: emerging
  lifecycle: introduction
  heat_score: 48
  tier: C
  signals:
    search_index: 2100
    mention_count: 1400
    article_count: 52
    engagement_rate: 0.035
  last_updated: 2026-06-19T03:00:00Z
  source_refs:
    - https://zhuanlan.zhihu.com/

- id: embodied-ai
  name_zh: 具身智能 / 物理 AI
  name_en: Embodied AI
  aliases: [具身智能, 物理AI, Embodied AI, Physical AI]
  category: emerging
  lifecycle: growth
  heat_score: 52
  tier: C
  signals:
    search_index: 2800
    mention_count: 1900
    article_count: 68
    engagement_rate: 0.038
  last_updated: 2026-06-19T03:00:00Z
  source_refs:
    - https://36kr.com/

- id: on-device-agent
  name_zh: 端侧 Agent / 本地模型
  name_en: On-Device Agent
  aliases: [端侧Agent, 本地模型, On-Device AI, Edge Agent]
  category: emerging
  lifecycle: introduction
  heat_score: 45
  tier: C
  signals:
    search_index: 1900
    mention_count: 1300
    article_count: 45
    engagement_rate: 0.032
  last_updated: 2026-06-19T03:00:00Z
  source_refs:
    - https://cloud.tencent.com.cn/developer/

- id: context-engineering
  name_zh: Context Engineering
  name_en: Context Engineering
  aliases: [Context Engineering, 上下文工程, Prompt Engineering 2.0]
  category: emerging
  lifecycle: introduction
  heat_score: 50
  tier: C
  signals:
    search_index: 2400
    mention_count: 1600
    article_count: 58
    engagement_rate: 0.036
  last_updated: 2026-06-19T03:00:00Z
  source_refs:
    - https://zhuanlan.zhihu.com/

- id: agent-memory
  name_zh: Agent 记忆管理
  name_en: Agent Memory Management
  aliases: [Agent记忆, 智能体记忆, Memory Management]
  category: emerging
  lifecycle: introduction
  heat_score: 42
  tier: C
  signals:
    search_index: 1600
    mention_count: 1100
    article_count: 38
    engagement_rate: 0.028
  last_updated: 2026-06-19T03:00:00Z
  source_refs:
    - https://zhuanlan.zhihu.com/

- id: vibe-coding
  name_zh: Vibe Coding
  name_en: Vibe Coding
  aliases: [Vibe Coding, 氛围编程, 凭感觉编程]
  category: emerging
  lifecycle: growth
  heat_score: 86
  tier: S
  signals:
    search_index: 14200
    mention_count: 9600
    article_count: 340
    engagement_rate: 0.078
  last_updated: 2026-06-19T03:00:00Z
  source_refs:
    - https://aihot.paicoding.com/
    - https://36kr.com/
```

---

## 维护规则

1. **新增词条**: heat_score ≥ 40 且有 ≥ 2 个 source_refs 才能入库
2. **淘汰词条**: 连续 4 周 heat_score < 30 → 移入 `archive/`
3. **合并规则**: aliases 重叠时合并为同一 entry，保留更高 heat_score
4. **版本号**: 每次更新追加 `last_updated` 时间戳
5. **快照**: 每周日 03:30 自动备份到 `archive/keyword-pool-{YYYYMMDD}.md`
