#!/usr/bin/env python3
"""
validate_skill.py — multi-agent-trend-ai SKILL.md 自动验证脚本

按 hermes-agent-skill-authoring 标准验证 SKILL.md 的完整性与正确性。

Usage:
    python scripts/validate_skill.py <SKILL.md 路径>
    python scripts/validate_skill.py .
"""
import sys
import re
import os
from pathlib import Path
from typing import List, Tuple


def parse_frontmatter(content: str) -> dict:
    """解析 YAML frontmatter (支持多行值)"""
    if not content.startswith("---"):
        return {}
    end = content.find("---", 3)
    if end == -1:
        return {}
    fm = content[3:end].strip()
    result = {}
    lines = fm.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        if ":" in line and not line.startswith(" "):
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip().strip('"').strip("'")

            # 处理 YAML 多行值（| 或 >）
            if value in ("|", ">"):
                collected = []
                i += 1
                while i < len(lines) and (lines[i].startswith(" ") or lines[i] == ""):
                    collected.append(lines[i].strip())
                    i += 1
                result[key] = " ".join(collected).strip()
                continue
            result[key] = value
        i += 1
    return result


def validate(skill_dir: str) -> Tuple[int, List[str]]:
    """返回 (得分, 问题列表)"""
    issues = []
    score = 100

    # Windows GBK 编码兼容 - 替换 emoji
    BAD, WARN, OK = "[X]", "[!]", "[OK]"

    skill_path = Path(skill_dir) / "SKILL.md"
    if skill_path.is_dir():
        skill_path = skill_path / "SKILL.md"
    if not skill_path.exists():
        # 也支持当前目录
        skill_path = Path(skill_dir)
        if not (skill_path / "SKILL.md").exists():
            return 0, [f"❌ SKILL.md not found at {skill_path}"]

    content = skill_path.read_text(encoding="utf-8")
    fm = parse_frontmatter(content)
    base = skill_path.parent

    # 1. description 必须以 "Use when" 开头
    desc = fm.get("description", "")
    if not desc.lower().startswith("use when"):
        issues.append(f"{BAD} description must start with 'Use when'")
        score -= 10

    # 2. frontmatter 必填字段
    required = ["name", "description", "version", "author", "license", "platforms"]
    for field in required:
        if field not in fm:
            issues.append(f"{BAD} frontmatter missing required field: {field}")
            score -= 5

    # 3. description ≤ 1024 字符
    if len(desc) > 1024:
        issues.append(f"{BAD} description too long: {len(desc)} chars (max 1024)")
        score -= 5

    # 4. references/ 目录存在（正文 > 8KB 时）
    content_size = len(content.encode("utf-8"))
    ref_dir = base / "references"
    if content_size > 8 * 1024 and not ref_dir.exists():
        issues.append(f"{BAD} references/ dir required (content > 8KB, got {content_size} bytes)")
        score -= 10
    elif ref_dir.exists():
        ref_files = list(ref_dir.glob("*.md"))
        if not ref_files:
            issues.append(f"{WARN} references/ exists but is empty")
            score -= 3

    # 5. test_pool.md 命名正确
    test_files = list(ref_dir.glob("test_*.md")) if ref_dir.exists() else []
    if not any(f.name == "test_pool.md" for f in test_files):
        if ref_dir.exists():
            issues.append(f"{BAD} test_pool.md not found (test_cases.md etc. is invalid)")
            score -= 5

    # 6. 无硬编码敏感信息
    sensitive_patterns = [
        (r"sk-[a-zA-Z0-9]{20,}", "OpenAI API key"),
        (r"tvly-[a-zA-Z0-9]{20,}", "Tavily API key"),
        (r"AKIA[0-9A-Z]{16}", "AWS Access Key"),
        (r"ghp_[a-zA-Z0-9]{36}", "GitHub PAT"),
        (r"password\s*=\s*['\"]", "Hardcoded password"),
        (r"api_key\s*=\s*['\"][a-zA-Z0-9]+", "Hardcoded API key"),
    ]
    for pattern, label in sensitive_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            issues.append(f"{BAD} hardcoded sensitive info detected: {label}")
            score -= 20

    # 7. 自我迭代机制
    if ref_dir.exists():
        if not (ref_dir / "failure_case_log.md").exists():
            issues.append(f"{WARN} failure_case_log.md missing (self-iteration incomplete)")
            score -= 5
        if not (ref_dir / "self-review-template.md").exists():
            issues.append(f"{WARN} self-review-template.md missing (self-iteration incomplete)")
            score -= 5

    # 8. metadata.hermes
    if "metadata:" in content and "hermes:" in content:
        pass  # OK
    elif content_size > 4 * 1024:
        issues.append(f"{WARN} metadata.hermes not found")
        score -= 3

    # 9. name 格式（kebab-case）
    name = fm.get("name", "")
    if name and not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", name):
        issues.append(f"{BAD} name '{name}' not in kebab-case")
        score -= 5

    # 10. 触发词 / 工作流覆盖
    has_workflow = "## Workflow" in content or "## 工作流" in content
    has_inputs = "## Inputs" in content or "## 输入" in content
    has_outputs = "## Outputs" in content or "## 输出" in content
    has_error = "## Error Handling" in content or "## 错误处理" in content

    missing_sections = []
    if not has_workflow:
        missing_sections.append("Workflow")
    if not has_inputs:
        missing_sections.append("Inputs")
    if not has_outputs:
        missing_sections.append("Outputs")
    if not has_error:
        missing_sections.append("Error Handling")

    if missing_sections:
        issues.append(f"{BAD} missing required sections: {', '.join(missing_sections)}")
        score -= 5

    return max(0, score), issues


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_skill.py <SKILL.md or skill dir>")
        sys.exit(1)

    # Windows GBK 编码兼容
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

    target = sys.argv[1]
    score, issues = validate(target)

    # 用 ASCII-safe 字符替代 emoji（Windows 兼容）
    OK, BAD, WARN, FIRE, CELEB, GEAR = "[OK]", "[X]", "[!]", "[FIRE]", "[***]", "[FIX]"

    print(f"\n{'='*60}")
    print(f"Validation Score: {score}/100")
    print(f"{'='*60}\n")

    if not issues:
        print(f"{OK} All checks passed!")
    else:
        for issue in issues:
            # Replace emoji in issues
            safe = issue.replace("❌", BAD).replace("⚠️", WARN).replace("✅", OK)
            print(safe)

    print()
    if score >= 90:
        print(f"{CELEB} Rating: EXCELLENT - ready to ship")
    elif score >= 75:
        print(f"{WARN} Rating: GOOD - ship after minor polish")
    elif score >= 60:
        print(f"{GEAR} Rating: NEEDS WORK - revise and re-validate")
    else:
        print(f"{BAD} Rating: FAIL - must rewrite")

    sys.exit(0 if score >= 75 else 1)


if __name__ == "__main__":
    main()
