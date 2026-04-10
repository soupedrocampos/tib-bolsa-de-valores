import re

with open('6889c58f-5abe-4a7a-b7fd-0d9856245d74.htm', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

imgs = re.findall(r'<img[^>]*>', text)
for i, img in enumerate(imgs):
    m = re.search(r'alt=["\']([^"\']*)["\']', img, re.IGNORECASE)
    if m:
        alt = m.group(1)
        if 'TIB' in alt or 'Best Invest' in alt:
            print(f'Alt: {alt}, Length: {len(img)}')
