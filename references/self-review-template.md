# Self-Review Template — 自我复盘模板

> 本文件是 multi-agent-trend-ai 的自我复盘流程模板。
> 触发条件: failure_case_log.md 未修复 ≥ 5 条，或每周日凌晨 03:30 自动复盘。
> 最后更新: 2026-06-19

---

## 复盘周期

- **自动复盘**: 每周日 03:30（cron）
- **触发复盘**: failure_case_log 未修复 ≥ 5 条
- **手动复盘**: 用户在对话中说"复盘一下"或"运行 analyze_failures"

---

## 复盘报告结构

```markdown
# Self-Review Report — {YYYY-MM-DD}

## 1. 本周期统计
- 调研次数: N
- 成功率: X% (成功/总次数)
- 平均耗时: T 秒
- 数据源健康: M/N 正常

## 2. 失败案例回顾
- 总失败: X 条
- 按阶段分布:
  - Step 1 (搜索): N
  - Step 2 (抓取): N
  - Step 3 (标准化): N
  - Step 4 (评分): N
  - Step 5 (分类): N
  - Step 6 (可视化/选题): N
- 按错误类型:
  - search_fail: N
  - fetch_timeout: N
  - viz_fail: N
  - scoring_anomaly: N
  - hallucination: N
- 复发性错误（同一触发词 ≥ 3 次）: [list]

## 3. 评分漂移检查
- 关键词 heat_score 与上周对比，漂移 > 20% 的:
  - [词条] 旧: 85 → 新: 65 (-23.5%) 原因: ...
- Tier 迁移:
  - [S→A] ...
  - [A→S] ...

## 4. 改进项清单

### P0（必须立即修复）
- [ ] {改进描述} | 负责人 | 截止日期

### P1（本周内修复）
- [ ] {改进描述} | 负责人 | 截止日期

### P2（下个版本优化）
- [ ] {改进描述} | 负责人 | 截止日期

## 5. 下周期 OKR
- O1: 提升数据源健康率至 100%
  - KR1: 修复 36 氪超时问题
  - KR2: 接入新榜作为备用源
- O2: 减少 LLM 幻觉
  - KR1: evidence URL 覆盖率从 80% 提升到 95%
  - KR2: 引入"待观察"区，强制人工审核

## 6. 回归测试
- 已修复案例进入 test_pool.md
- 运行 `python scripts/run_loop.py . --regression`
- 通过率: X/Y

## 7. 总结
- 本周期最大收获: ...
- 下周期最大风险: ...
```

---

## 复盘执行流程

```
[1] analyze_failures.py --auto
        ↓
[2] 生成 failure_report_{date}.md
        ↓
[3] 人工/AI 评估每个失败案例
        ↓
[4] 按 P0/P1/P2 分类
        ↓
[5] 更新 SKILL.md / references/
        ↓
[6] 写入 test_pool.md (回归用例)
        ↓
[7] 运行回归测试
        ↓
[8] 输出 self-review-report_{date}.md
```

---

## 加分项（评审时）

| 条件 | 加分 |
|------|------|
| 有错误日志且 ≥ 3 条记录 | +3 |
| 有自我复盘报告且有改进措施 | +3 |
| 已修复案例进入回归测试池 | +2 |
| 最近 30 天无新增错误 | +2 |
| **最高** | **+10** |

---

## 历史归档

完成的复盘报告移入 `archive/self-review-{YYYYMMDD}.md`。
