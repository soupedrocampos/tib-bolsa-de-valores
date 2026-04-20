"""
Replace hardcoded border-radius: 8px and border-radius: 12px with 16px
across all .htm files in the project. Skips 50% (circles) and small decorative radii.
"""
import re, pathlib, sys

ROOT = pathlib.Path(r"c:\Users\pacc1\Downloads\PATRICK\tib site")

# Directories to scan
DIRS = [ROOT, ROOT / "licenciados-2", ROOT / "treinamento", ROOT / "treinamento-2"]

# Values to replace → 16px
# We target 8px, 10px, 12px (panel/card radii) but NOT:
#   - 50%  (circles/cursor)
#   - 3px, 4px, 5px, 6px (tiny decorative)
#   - partial radii like "10px 10px 0 0" (keep as-is)
TARGET_PATTERN = re.compile(
    r'(border-radius\s*:\s*)(\b(?:8|10|12)px\b)(;)',
)

def process_file(path):
    text = path.read_text(encoding="utf-8", errors="ignore")
    new_text, count = TARGET_PATTERN.subn(r'\g<1>16px\g<3>', text)
    if count:
        path.write_text(new_text, encoding="utf-8")
        print(f"  ✅ {path.name}  — {count} substituição(ões)")
    return count

total = 0
for d in DIRS:
    for f in sorted(d.glob("*.htm")):
        total += process_file(f)

print(f"\nTotal: {total} valores substituídos em todos os .htm")
