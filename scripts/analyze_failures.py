#!/usr/bin/env python3
"""
analyze_failures.py — multi-agent-trend-ai 错误日志分析脚本

检测是否触发自我迭代，并生成改进建议。

Usage:
    python scripts/analyze_failures.py <skill_dir> --auto
    python scripts/analyze_failures.py <skill_dir> --suggest
    python scripts/analyze_failures.py <skill_dir> --regression
"""
import sys
import re
from pathlib import Path
from collections import Counter
from typing import List, Dict


def parse_failure_log(log_path: Path) -> List[Dict]:
    """解析 failure_case_log.md（支持 #CASE: 与旧版 ### [...] 两种格式）"""
    if not log_path.exists():
        return []
    content = log_path.read_text(encoding="utf-8")
    cases = []
    current = {}
    in_code_block = False
    for line in content.split("\n"):
        # 跳过 markdown 代码块（避免模板示例被误解析）
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        # 新格式：#CASE: <id>
        if line.startswith("#CASE:"):
            if current and len(current) > 1:
                cases.append(current)
            current = {"id": line.strip()}
        # 旧格式：### [date] #id
        elif line.startswith("### [") and "id" not in current:
            if current and len(current) > 1:
                cases.append(current)
            current = {"id": line.strip()}
        # 键值对（缩进 2 空格）
        elif line.strip().startswith("- **"):
            m = re.match(r"- \*\*(\w+)\*\*: (.+)", line)
            if m:
                current[m.group(1)] = m.group(2).strip()
        elif re.match(r"^\s{2}(\w+):\s*(.+)", line):
            m = re.match(r"^\s{2}(\w+):\s*(.+)", line)
            if m:
                current[m.group(1)] = m.group(2).strip()
    if current and len(current) > 1:
        cases.append(current)
    return cases


def check_trigger(cases: List[Dict]) -> Dict:
    """检测迭代触发条件"""
    pending = [c for c in cases if c.get("修复状态", "").startswith("pending")]
    trigger_words = Counter()
    for c in cases:
        word = c.get("触发词", "")
        if word:
            trigger_words[word] += 1

    recurrent = {w: n for w, n in trigger_words.items() if n >= 3}

    return {
        "total": len(cases),
        "pending_count": len(pending),
        "trigger_iteration": len(pending) >= 5,
        "recurrent_words": recurrent,
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_failures.py <skill_dir> [--auto|--suggest|--regression]")
        sys.exit(1)

    # Windows GBK 编码兼容
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

    skill_dir = Path(sys.argv[1])
    log_path = skill_dir / "references" / "failure_case_log.md"
    cases = parse_failure_log(log_path)
    result = check_trigger(cases)

    # ASCII-safe 字符
    OK, NO, WARN = "[OK]", "[X]", "[!]"

    print(f"\n{'='*60}")
    print(f"Failure Analysis Report - {skill_dir.name}")
    print(f"{'='*60}\n")
    print(f"Total failure cases: {result['total']}")
    print(f"Pending: {result['pending_count']}")
    print(f"Recurrent trigger words: {result['recurrent_words'] or 'None'}")
    iter_status = f"{OK} YES" if result['trigger_iteration'] else f"{NO} NO"
    print(f"Iteration triggered: {iter_status}\n")

    if "--suggest" in sys.argv and result["pending_count"] > 0:
        print("[Suggest] Improvements (by priority):\n")
        if result["trigger_iteration"]:
            print("  P0: Start root-cause analysis immediately")
        if result["recurrent_words"]:
            print("  P0: Fix root cause of recurrent errors")
        print("  P1: Improve degradation fallback text")
        print("  P2: Add evidence URL coverage check")

    if "--regression" in sys.argv:
        print("\n[Regression] Cases recommended for regression pool:")
        for c in cases[:5]:
            print(f"  - {c.get('id', '?')}: {c.get('trigger_word', c.get('触发词', '?'))}")


if __name__ == "__main__":
    main()
