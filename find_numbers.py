import re
import glob

slides = glob.glob('*.htm')
for slide in slides:
    with open(slide, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    
    # Find all instances of digits / digits that are NOT inside num-pill
    # We do this by iterating over matches
    matches = re.finditer(r'>\s*0?\d\s*/\s*10\s*<', text)
    for m in matches:
        start = max(0, m.start() - 150)
        end = min(len(text), m.end() + 20)
        snippet = text[start:end].replace('\n', ' ')
        if 'num-pill' not in snippet and 'slide-num' not in snippet:
            print(f'File {slide}: {snippet}')
