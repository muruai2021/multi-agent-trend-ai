---
name: multi-agent-trend-ai
description: "调研微信公众号和视频号等微信生态中 AI Agent 领域的热门关键词、内容趋势与流量词。触发场景包括用户询问 AI Agent 热门话题、公众号热度关键词、视频号 AI 流量词、AI Agent 选题方向，或需要生成相关公众号或视频号内容选题报告。本技能整合多源热点数据，按热度梯队输出关键词分析、可视化图表及内容选题建议。"
agent_created: true
version: 1.0.0
---

# Multi-Agent-Trend-AI

调研微信生态（公众号 + 视频号）AI Agent 热门关键词与内容趋势，输出热度分级、关键词解读及内容选题建议。

## 核心数据源

| 来源 | 链接 | 用途 |
|------|------|------|
| PaiCoding AI热点雷达 | https://aihot.paicoding.com/ | 每日跨平台热点聚合 |
| 36氪 AI专题 | https://36kr.com/ | 行业趋势与资本动向 |
| 花叔AI自媒体趋势 | https://www.huasheng.ai/insights/ai-content-trends-2025-2026/ | 自媒体内容方向参考 |
| 腾讯云开发者社区 | https://cloud.tencent.com.cn/developer/ | 视频号和微信生态动态 |
| 知乎专栏 AI Agent合集 | https://zhuanlan.zhihu.com/ | 技术深度文章 |

## 标准调研流程

### Step 1：多源搜索关键词

用 WebSearch 并发搜索以下方向（每组最多5个关键词）：

组1：AI agent 公众号 热门 2026
组2：视频号 AI智能体 热搜词
组3：MCP A2A Multi-Agent 公众号热度
组4：AI Agent 爆款选题 公众号

### Step 2：抓取高价值页面

重点抓取以下类型的页面：
- AI 热点雷达（每日更新，直接可用）
- 36氪 AI Agent 专题文章（趋势判断）
- 技术栈和掘金等垂直社区（开发者热度）
- 腾讯云开发者社区（视频号和微信生态独家）

用 WebFetch 提取页面核心内容。

### Step 3：整理热度梯队

按以下标准将关键词分为四层：

| 梯队 | 标准 | 典型来源 |
|------|------|---------|
| 第一梯队 | 公众号和视频号双爆，搜索指数极高 | MCP协议、Multi-Agent、Vibe Coding |
| 第二梯队 | 技术社区高热，持续稳定 | CrewAI、LangGraph、Dify |
| 第三梯队 | 应用场景快速上升 | AI客服Agent、微信内置AI |
| 第四梯队 | 新兴潜力方向 | Agent Swarm、端侧Agent、具身智能 |

### Step 4：生成可视化输出

使用 show_widget 工具生成热度条形图加标签云双视图：
- 热度条形图：横向条形，每条标注关键词名称加热度百分比
- 标签云：按梯队配色（紫等于第一梯队，蓝等于第二梯队，绿等于第三梯队，橙等于第四梯队）

参考配色（固定四色）：
第一梯队: #534AB7 (紫)
第二梯队: #185FA5 (蓝)
第三梯队: #3B6D11 (绿)
第四梯队: #854F0B (橙)

### Step 5：内容选题建议

结合用户背景（多Agent协作系统开发、公众号写作者），给出2到3条高命中选题组合：
- 组合关键词1：MCP 加上 多Agent协作流水线实战
- 组合关键词2：Vibe Coding 加上 企业级Agent落地案例
- 组合关键词3：微信内置AI Agent 加上 电商客服场景

## 关键词库（持续更新）

核心关键词池（调研时优先检查是否仍处热度上升期）：

**概念层**
- MCP协议 / Model Context Protocol
- A2A协议 / Agent-to-Agent
- AG-UI / Agent User Interface
- Multi-Agent 多智能体协作
- Agent Workflow / 工作流编排

**框架层**
- CrewAI / LangChain / LangGraph
- Dify / Coze 平台
- AutoGPT 2.0
- Claude Code / Cursor / Codex

**应用层**
- AI 客服 Agent
- 内容生成 Pipeline
- 微信内置 AI Agent（2026年6月新增热点）
- Agent 落地 / 企业级应用

**新兴层**
- Agent Swarm（蜂群）
- 具身智能 / 物理 AI
- 端侧 Agent / 本地模型
- Context Engineering
- Agent 记忆管理

## 输出格式规范

每次调研输出包含：
1. 热度分级表（四梯队，Markdown 表格）
2. 可视化热度图（show_widget，热度条形图加标签云）
3. 内容选题建议（2到3 条组合，供公众号和视频号创作者参考）
4. 数据来源注释（附注本次使用的数据源列表）
