import os
import re

with open('logo_b64.txt', 'r', encoding='utf-8') as f:
    logo_b64 = f.read().strip()

logo_html = f'<div class="logo"><img src="data:image/png;base64,{logo_b64}" style="height: 50px; width: auto; display: block; position: fixed; top: 25px; left: 25px; z-index: 10000;"></div>'

slides = [
    '6889c58f-5abe-4a7a-b7fd-0d9856245d74.htm',
    'd44e90f7-4cba-419a-8fb6-e67b9f1c3244.htm',
    'fed32750-c044-4f3c-85eb-569045ba5cd5.htm',
    'a23cc662-dd07-4e88-ad78-4390fb4159b5.htm',
    'decb2a9f-0689-4ab8-be02-57d48b45364d.htm',
    '2595c031-784a-4bcc-926b-40930d15d505.htm',
    'b52cd9d4-d5d6-4bfd-b3c8-3978f01817dc.htm',
    'condicoes.htm',
    '467f4cfd-096f-43c8-ae7f-ff5c63804069.htm',
    '8ca20ea5-73c0-45e7-bbc7-9318fcf90089.htm'
]

global_style = """
<style>
/* HARD HIDE ALL GOLDEN COUNTERS AND OLD LOGOS */
.slide-num, .slide-number, #snum { display: none !important; opacity: 0 !important; visibility: hidden !important; z-index: -1 !important;}
img[alt*="TIB"], img[alt*="Best Invest"] { display: none !important; }

/* Position simple counter at the top right */
.num-pill {
    position: fixed !important;
    top: 25px !important;
    right: 25px !important;
    bottom: auto !important;
    left: auto !important;
    background: transparent !important;
    color: #fff !important;
    padding: 10px 20px !important;
    font-family: 'Oswald', sans-serif !important;
    font-size: 28px !important; 
    font-weight: bold !important;
    z-index: 9999 !important; 
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    letter-spacing: 2px !important;
}
</style>
"""

for i, slide in enumerate(slides):
    if not os.path.exists(slide):
        continue
    
    with open(slide, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Always wipe out existing .logo containers to prevent duplication
    content = re.sub(r'<div class="logo">.*?</div>', '', content, flags=re.DOTALL|re.IGNORECASE)
    
    # Inject our standard logo on EVERY slide to be safe (it's fixed positioned now)
    if '<body>' in content:
        content = content.replace('<body>', '<body>\n' + logo_html)

    # Setup numbering
    expected_num = f'{i+1:02} / 10'
    if 'num-pill' in content:
        content = re.sub(r'(<div[^>]*class=["\']?num-pill["\']?[^>]*>)\s*[\d]+\s*/\s*[\d]+\s*(</div>)', f'\\g<1>{expected_num}\\g<2>', content, flags=re.IGNORECASE)
    else:
        if '<body>' in content:
            content = content.replace('<body>', f'<body>\n<div class="num-pill">{expected_num}</div>')

    # Add standard CSS
    # Clean previous injection if exists
    content = re.sub(r'<style>\n/\* HARD HIDE.*?currentColor;\n}\n</style>', '', content, flags=re.DOTALL)
    if '</head>' in content:
        content = content.replace('</head>', global_style + '\n</head>')

    with open(slide, 'w', encoding='utf-8', errors='ignore') as f:
        f.write(content)
    print(f'Processed {slide}')
