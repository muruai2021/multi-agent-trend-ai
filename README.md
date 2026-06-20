# multi-agent-trend-ai

> 调研微信生态（公众号 + 视频号 + 小程序 + 搜一搜）AI Agent 热门关键词与内容趋势，按 S/A/B/C 四梯队输出热度分级、关键词解读、可视化图表及内容选题建议。

[![version](https://img.shields.io/badge/version-1.1.0-blue)](SKILL.md)
[![license](https://img.shields.io/badge/license-Apache--2.0-green)](LICENSE)
[![platforms](https://img.shields.io/badge/platforms-claude--code%20%7C%20hermes--agent-lightgrey)](SKILL.md)

## 这是什么

一个 Claude Code / Hermes Agent 的 Skill，用于：

1. **采集** 微信生态（公众号 + 视频号）中 AI Agent 相关关键词的多源信号
2. **评分** 按 0.30·search + 0.30·mention + 0.20·article + 0.20·engage 公式计算 heat_score
3. **分类** 按 S ≥ 85 / A 70-84.9 / B 55-69.9 / C < 55 四梯队分级
4. **生成** 自包含 HTML 报告（含 28 词横向条形图 + 4 条选题 + 公众号生态信号源）

## 快速开始

```bash
# 在对话中调用
/multi-agent-trend-ai

# 或带参数
/multi-agent-trend-ai 30d both AI Agent
```

输出会落在 **当前工作目录** 的 `trend-report-YYYY-MM-DD.html`（自包含、无外部依赖）。

## 目录结构

```
multi-agent-trend-ai/
├── README.md                       ← 本文件
├── SKILL.md                        ← Skill 规范（v1.1.0，YAML frontmatter + 工作流）
├── LICENSE                         ← Apache-2.0
├── .gitignore                      ← 排除 trend-report-*.html 与 outputs/
│
├── references/                     ← 知识库
│   ├── keyword-pool.md             ← 30 个 AI Agent 关键词（按 concept/framework/application/emerging 四层）
│   ├── heat-scoring.md             ← 评分公式推导 + 归一化方法
│   ├── topic-template.md           ← 选题生成 prompt 模板
│   ├── data-sources.md             ← 数据源配置 + 降级顺序
│   ├── failure_case_log.md         ← 失败案例日志（自我迭代）
│   ├── self-review-template.md     ← 自我复盘模板
│   └── test_pool.md                ← 测试用例池
│
├── templates/                      ← 输出模板
│   └── report.html                 ← 标准 HTML 报告模板（参数化）
│
├── scripts/                        ← 工具脚本
│   ├── validate_skill.py           ← Skill 规范验证
│   └── analyze_failures.py         ← 失败日志分析
│
└── drafts/                         ← 设计文档（追溯）
    ├── sop-draft-v0.md
    ├── researcher-report.md
    ├── design-spec-v1.md
    └── review-report-v1.md
```

## 工作流（7 步）

```
Step 1 · 用户输入解析（topic / time_window / target_platform）
  ↓
Step 2 · 多源数据采集（4 路并发 mmx search query）
  ↓
Step 3 · 去重 + 标准化（中英别名归一）
  ↓
Step 4 · 热度评分（HeatScore 0-100）
  ↓
Step 5 · 梯队分类 (S/A/B/C)
  ↓
Step 6 · 可视化 + 选题生成（CSS 横向条形图 + 4 条选题）
  ↓
Step 7 · 失败日志写入（如有）
```

## 输出示例

报告包含 10 个章节：

1. **梯队分布** — 4 个统计卡（SVG 图标 + 数字 + 标签）
2. **热度分布** — 28 词横向条形图（按梯队上色）
3. **S 梯队核心热点** — 详细卡片（数据信号 + Evidence）
4. **A 梯队高潜热点** — 表格（关键词 + 分数 + 层级 + 生命周期 + 信号）
5. **B 梯队稳定增长** — 表格
6. **C 梯队长尾观察** — 表格
7. **选题清单** — 4 条（3 条常规 + 1 条反共识），每条含：
   - 关键词组合
   - 选题逻辑（4 个 bullet：热度支撑 / 生命周期互补 / 数据信号 / 受众基础）
   - 大纲
   - Evidence（≥ 2 个真实 URL）
   - 预估热度
8. **公众号生态信号源** — 信号源表（直接采集 / 待接入 / 降级 / 失败）
9. **失败记录** — step / status / description
10. **发布节奏** — 10 天节奏表（公众号 + 视频号）

查看 [templates/report.html](templates/report.html) 了解完整结构。

## 内容质量约束（v1.1.0+ 强制）

1. **不编造案例** — 每个 evidence URL 必须来自当次 mmx search organic 结果
2. **选题不用第一人称** — 避免"我"、"我们"，改为客观描述
3. **选题逻辑必须有依据** — 每条选题显式列出热度分数、生命周期、数据信号
4. **反共识选题有原文支撑** — 必须从 mmx 搜索结果中找到事实支点

## 数据源

主源：mmx search query（4 路并发，跨平台覆盖公众号 / 视频号 / 知乎）

公众号生态间接源（待接入）：
- 微信搜一搜热词榜
- 视频号创作者中心
- 新榜公众号指数
- 清博公众号数据

## 自我迭代

- 每次失败自动记录到 `references/failure_case_log.md`
- 未修复 ≥ 5 条 → 触发复盘迭代
- 同一触发词 ≥ 3 次 → 立即修复

## 贡献

修改流程：
1. Fork & 拉分支
2. 修改 `SKILL.md` 或 `references/`
3. 在 `references/failure_case_log.md` 记录变更
4. 提交 PR

## 许可

Apache-2.0

## 链接

- [Skill 规范](SKILL.md)
- [报告模板](templates/report.html)
- [关键词库](references/keyword-pool.md)
- [评分公式](references/heat-scoring.md)
- [选题模板](references/topic-template.md)
