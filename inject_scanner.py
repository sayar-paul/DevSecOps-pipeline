import re
from pathlib import Path

SYSTEM_PROMPT_PATTERNS = [
    r"SYSTEM" + r"_PROMPT\s*=",
    r"system" + r"_message\s*=",
    r'"' + "role" + r'"\s*:\s*"' + "system" + '"'
]

INJECTION_PHRASES = [
    "ignore previous " + "instructions",
    "you are " + "now",
    "pretend you " + "are" + "",
    "act as if you have " + "no restrictions"
]

def scan_file(file_path):
    findings = []

    try:
        content = file_path.read_text(
            encoding="utf-8",
            errors="ignore"
        )

        lines = content.splitlines()

        for line_number, line in enumerate(lines, start=1):

            
            for pattern in SYSTEM_PROMPT_PATTERNS:
                if re.search(pattern, line, re.IGNORECASE):
                    findings.append(
                        (line_number, "Hardcoded system prompt", line.strip())
                    )

            
            for phrase in INJECTION_PHRASES:
                if phrase.lower() in line.lower():
                    findings.append(
                        (line_number, "Injection phrase detected", line.strip())
                    )

    except Exception as error:
        print(f"[ERROR] Could not scan {file_path}: {error}")

    return findings


def main():
    root = Path(__file__).resolve().parent

    python_files = [
        file for file in root.rglob("*.py")
        if ".git" not in file.parts
        and ".venv" not in file.parts
        and "venv" not in file.parts
    ]
    print(" CUSTOM PROMPT INJECTION SCANNER")
    print(f"Python files found: {len(python_files)}")

    total_findings = 0

    for file_path in python_files:
        findings = scan_file(file_path)

        for line_number, issue, content in findings:
            total_findings += 1

            relative_path = file_path.relative_to(root)

            print(f"\n[BLOCKED] {relative_path}:{line_number}")
            print(f"Issue: {issue}")
            print(f"Matched line: {content}")

    print("\n====================================")

    if total_findings > 0:
        print(f"SCAN FAILED: {total_findings} finding(s) detected.")
        raise SystemExit(1)

    print("SCAN PASSED: No suspicious patterns detected.")
    raise SystemExit(0)


if __name__ == "__main__":
    main()
