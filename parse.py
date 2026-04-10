import re

filepath = r"c:\Users\pacc1\Downloads\PATRICK\tib site\6889c58f-5abe-4a7a-b7fd-0d9856245d74.htm"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# remove styles
content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL)
# remove scripts
content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
# remove svgs
content = re.sub(r'<svg[^>]*>.*?</svg>', '', content, flags=re.DOTALL)
# remove big attributes
content = re.sub(r' (src|href|d|class|style)="[^"]{100,}"', '', content)
content = re.sub(r' (src|href|d|class|style)=\'[^\']{100,}\'', '', content)

# try to find elements with position absolute or fixed or classes related to cursor/ball/glow
matches = re.finditer(r'<[a-zA-Z0-9-]+[^>]*>', content)
tags = []
for m in matches:
    tag = m.group(0)
    if 'img' not in tag and 'meta' not in tag:
        tags.append(tag)

with open('tags.txt', 'w', encoding='utf-8') as out:
    for t in tags:
        out.write(t + '\n')
