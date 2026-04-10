import re

filepath = r"c:\Users\pacc1\Downloads\PATRICK\tib site\6889c58f-5abe-4a7a-b7fd-0d9856245d74.htm"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r'(<div class="person-layer fade-right">\s*<img\s+src=")(data:image/[^"]*)(")'

new_content, count = re.subn(pattern, r'\1Untitled%20design%20(2).png\3', content, count=1)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"Replaced {count} occurrences.")
