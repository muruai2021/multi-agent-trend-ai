# Test Pool — 测试用例池

> 本文件维护 multi-agent-trend-ai 的全部测试用例。
> 共 8 个用例：基础功能 3 + 边界场景 3 + 错误恢复 2
> 最后更新: 2026-06-19

---

## 用例总览

| ID | 类别 | 标题 | 状态 |
|----|------|------|------|
| TC-01 | 基础 | 完整调研流程 | ✅ |
| TC-02 | 基础 | 单梯队查询 | ✅ |
| TC-03 | 基础 | 中英双语输出 | ✅ |
| TC-04 | 边界 | 空查询 | ✅ |
| TC-05 | 边界 | 关键词库全空 | ✅ |
| TC-06 | 边界 | 阈值边界（85.0 → S） | ✅ |
| TC-07 | 错误恢复 | 数据源全失败 | ✅ |
| TC-08 | 错误恢复 | 可视化工具不可用 | ✅ |

---

## 基础功能测试

### TC-01 完整调研流程

**Input**:
```json
{
  "query": "做一份 AI Agent 关键词调研，时间范围 30 天",
  "target_platform": "两者",
  "time_window": "30d",
  "user_background": "开发者"
}
```

**Expected**:
- 返回完整 Markdown 报告
- 包含四梯队分布表
- ≥ 20 个关键词
- 3 条以上选题建议
- 配色使用 `#534AB7 / #185FA5 / #3B6D11 / #854F0B`
- 包含可视化产物路径或 Markdown 表格回退

**验证点**:
- [ ] Markdown 结构符合 output schema
- [ ] 四梯队均存在（除非某梯队为空）
- [ ] 至少 1 个 S 梯队词带 evidence URL
- [ ] 选题包含 1 条反共识
- [ ] 数据源声明完整

---

### TC-02 单梯队查询

**Input**:
```json
{
  "query": "只看 S 梯队 AI 热门词",
  "tier_focus": ["S"]
}
```

**Expected**:
- 仅返回 S 梯队关键词
- A/B/C 梯队不在输出中
- 选题建议只基于 S 梯队生成

**验证点**:
- [ ] tier_focus 正确解析为 `["S"]`
- [ ] 输出不含 A/B/C 词条
- [ ] 选题生成 prompt 不含其他梯队

---

### TC-03 中英双语输出

**Input**:
```json
{
  "query": "WeChat AI Agent trend report, 7 days",
  "language": "en-US"
}
```

**Expected**:
- 报告标题、说明文字为英文
- 关键词保留中文原名 + 英文别名
- 选题标题中英双语

**验证点**:
- [ ] 报告标题为英文
- [ ] name_zh 与 name_en 同时存在
- [ ] 选题 title_zh 与 title_en 同时存在

---

## 边界场景测试

### TC-04 空查询

**Input**:
```json
{
  "query": ""
}
```

**Expected**:
- 不调用任何数据源
- 返回澄清问题
- 提示用户补充时间范围、平台范围

**验证点**:
- [ ] 无 WebSearch/WebFetch 调用
- [ ] 提示语清晰（"请告诉我您想调研的方向..."）
- [ ] 不生成任何梯队数据

---

### TC-05 关键词库全空

**Input**:
```json
{
  "query": "调研最新 AI 词"
}
```

**Setup**: 临时清空 `references/keyword-pool.md`（测试后恢复）

**Expected**:
- 4 个数据源均被调用
- 从在线数据源采集并填充新库
- 最终 keyword-pool.md 被更新

**验证点**:
- [ ] 4 个数据源均被调用（监控日志）
- [ ] keyword-pool.md 至少新增 5 个词条
- [ ] 新增词条带 evidence URL

---

### TC-06 阈值边界

**Input**: 模拟某词 heat_score=85.0

**Expected**:
- tier_classify 对 85.0 返回 S
- tier_classify 对 84.9 返回 A
- tier_classify 对 70.0 返回 A
- tier_classify 对 69.9 返回 B
- tier_classify 对 55.0 返回 B
- tier_classify 对 54.9 返回 C

**验证点**:
- [ ] 边界值包含（85.0 ∈ S）
- [ ] 边界值不交叉（84.9 ∉ S）
- [ ] 所有 6 个边界用例通过

**脚本验证**:
```python
assert classify(85.0) == "S"
assert classify(84.9) == "A"
assert classify(70.0) == "A"
assert classify(69.9) == "B"
assert classify(55.0) == "B"
assert classify(54.9) == "C"
```

---

## 错误恢复测试

### TC-07 数据源全失败

**Setup**: 模拟 4 个数据源均返回 5xx 或超时

**Expected**:
- 降级到本地 `keyword-pool.md`
- 输出包含 `degraded_mode` 标记
- `failure_case_log.md` 追加 1 条记录
- 报告头部包含降级说明

**验证点**:
- [ ] failure_case_log.md 行数 +1
- [ ] 报告含 `⚠️ 数据降级` 提示
- [ ] 仍能输出报告（基于本地库）
- [ ] 数据源声明标 "降级到本地缓存"

---

### TC-08 可视化工具不可用

**Setup**: 模拟 matplotlib/wordcloud 导入失败

**Expected**:
- 自动降级到 Markdown 表格 + ANSI 着色
- viz/ 目录无 PNG 文件（已跳过）
- 报告的"可视化"章节使用表格形式

**验证点**:
- [ ] matplotlib 导入错误被捕获
- [ ] 输出包含 Markdown 表格替代
- [ ] 表格带 ANSI 着色标记（终端渲染时）
- [ ] failure_case_log.md 记录 viz_fail
- [ ] 主流程不被阻塞

---

## 测试运行

### 自动化（推荐）
```bash
python scripts/run_loop.py . --test
```

### 手动验证
对照每个 TC 的"验证点"逐项打勾。

### 通过率目标
- **基础功能**: 100% 必须通过
- **边界场景**: 100% 必须通过
- **错误恢复**: 100% 必须通过（降级路径有效）

### 失败处理
任何 TC 失败：
1. 记录到 `failure_case_log.md`
2. 评估严重性（Critical/High/Medium/Low）
3. Critical/High → 立即修复
4. Medium/Low → 进入下个迭代

---

## 测试历史

| 日期 | 通过率 | 失败用例 | 备注 |
|------|--------|---------|------|
| 2026-06-19 | 8/8 (100%) | 无 | 初始基线 |
