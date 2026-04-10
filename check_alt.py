import re
with open('6889c58f-5abe-4a7a-b7fd-0d9856245d74.htm', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

imgs = re.findall(r'<img[^>]*>', text)
for i, img in enumerate(imgs):
    alt_match = re.search(r'alt=["\']([^"\']*)["\']', img, re.IGNORECASE)
    alt_text = alt_match.group(1) if alt_match else 'NO ALT TEXT'
    print(f'Image {i}: alt="{alt_text}", length={len(img)}')
