# Failure Case Log — 失败案例日志

> 本文件记录 multi-agent-trend-ai 每次使用出现的错误案例。
> 触发条件: 未修复 ≥ 5 条 → 自动触发复盘迭代；同一触发词出现 ≥ 3 次 → 立即修复
> 最后更新: 2026-06-19

---

## 记录格式

每条记录使用如下结构（实际案例请从下方 `## 当前记录` 起追加）：

```
#CASE: <case_id>
  date: <YYYY-MM-DD>
  trigger_word: <user_query>
  stage: Step 1/2/3/4/5/6/7
  error_type: search_fail / fetch_timeout / viz_fail / scoring_anomaly / hallucination
  actual_output: <实际输出>
  expected_output: <应有输出>
  root_cause: <根因分析>
  fix_status: pending / fixed / regression_passed
  fix_version: <version>
```

---

## 当前记录

```
#CASE: 2026-06-20-001
  date: 2026-06-20
  trigger_word: multi-agent-trend-ai (默认参数，本周 7d)
  stage: Step 2
  error_type: search_fail
  actual_output: Tavily MCP 返回 "Client network socket disconnected before secure TLS connection was established"，4 路 WebSearch + 5 个高价值页面抓取全部失败
  expected_output: 4 路搜索返回各 ~10 条 AI Agent 相关结果
  root_cause: Tavily MCP 网络层 TLS 握手失败（网络环境受限）
  fix_status: fixed
  fix_version: v1.0.1
  resolution: 已回退到 mmx search query (4 路并发)，并按全局规则绕过 WebFetch 优先调用 mmx。WebFetch 因 hooks 要求先调 mmx，未使用。最终 4 路搜索均成功，每个返回 10 条 organic 结果
  data_impact: 数据时效性未损失（mmx 实时返回），但缺少 5 个高价值数据源的交叉验证（aihot.paicoding / 36kr / huasheng.ai / cloud.tencent / zhuanlan.zhihu），改用搜索结果中嵌入的间接引用
  reliability_note: 本次 confidence 标记为 medium（仅 1 个源，mmx search）
```

```
#CASE: 2026-06-20-002
  date: 2026-06-20
  trigger_word: multi-agent-trend-ai (默认参数)
  stage: Step 4
  error_type: scoring_anomaly
  actual_output: 使用 min-max 归一化（基于本批次 min/max）后，28 词中 23 词被压入 C 梯队（<55），分布严重失衡（S=2, A=1, B=2, C=23）
  expected_output: 分布合理（约 S=10%, A=40%, B=30%, C=20%）
  root_cause: min-max 归一化对极值极敏感。MCP 协议 search_index=18500 拉高 max，导致大部分词归一化后分数被压扁
  fix_status: fixed
  fix_version: v1.0.1
  resolution: 改用对数归一化作为交叉验证手段，最终采用 70% 原库权威分 + 30% 对数分 的混合策略；新词按对数分位置插入相邻梯队。修复后分布 S=3(10.7%) A=12(42.9%) B=8(28.6%) C=5(17.9%)
  doc_update: 已在 heat-scoring.md 备注中追加"扩展 min-max 范围（理论 max=25000/18000/600/0.10）"作为冷启动/中等样本量场景的备选方案
```

```
#CASE: 2026-06-20-003
  date: 2026-06-20
  trigger_word: multi-agent-trend-ai
  stage: Step 6
  error_type: viz_fail
  actual_output: matplotlib / wordcloud 不可用（ModuleNotFoundError）
  expected_output: 横向条形图 + 标签云 PNG
  root_cause: 当前 Python 环境未安装可视化库
  fix_status: pending
  fix_version: -
  resolution: 已降级到自包含 HTML 报告（CSS 横向条形图 + 表格），无需 matplotlib/wordcloud 依赖
```

```
#CONFIG: 2026-06-20-001
  date: 2026-06-20
  type: user-preference-update
  scope: skill-defaults
  changes:
    - deliverable_format: md+chart → html
    - output_path: outputs/ → current-directory
    - content_constraint[no_first_person_in_topics]: true
    - content_constraint[evidence_required]: true
    - content_constraint[topic_logic_required]: true
  reason: 用户要求修改 skills 行为
  affects: SKILL.md frontmatter (version 1.0.0 → 1.1.0), Quick Start, Outputs 章节
  migration:
    - 历史 outputs/trend-report-*.md 仍可访问
    - 新生成的报告位于当前工作目录
    - mmx search 取代 Tavily 作为主搜索源
  regression_test: 2026-06-20 生成的 trend-report-2026-06-20.html 已验证 4 条选题均不含第一人称、所有 evidence URL 来自 mmx search organic 结果、每条选题含 4 点逻辑依据
```

---

## 触发条件检查脚本

```bash
# 未修复条数
grep -c "修复状态.*pending" references/failure_case_log.md

# 同一触发词频次
grep "触发词" references/failure_case_log.md | sort | uniq -c | sort -rn
```

---

## 历史归档

每次复盘完成后，未修复案例移入 `archive/failure-case-log-{YYYYMMDD}.md`。
