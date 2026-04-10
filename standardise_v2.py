import os
import re

# Base64 logo
with open('logo_b64.txt', 'r') as f:
    logo_b64 = f.read().strip()

logo_html = f'<div class="logo"><img src="data:image/png;base64,{logo_b64}" style="height: 50px; width: auto; display: block;"></div>'

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

# Global CSS to position the counter correctly
global_style = """
<style>
/* Remove the old slide-number box just in case */
.slide-number { display: none !important; }

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
    font-size: 28px !important; /* Slightly larger as requested by visual cues in image 1 */
    font-weight: bold !important;
    z-index: 9999 !important; /* Top layer */
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    letter-spacing: 2px !important;
}

/* Ensure logo and branding are correct */
.logo { z-index: 10000 !important; }
</style>
"""

for i, slide in enumerate(slides):
    if not os.path.exists(slide):
        print(f'Skipping {slide}')
        continue
        
    with open(slide, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # 1. Remove golden slide-number block
    # Regex to find the div and its contents
    # Variation: some slides might have split tags
    content = re.sub(r'<div class=["\']?slide-number["\']?.*?>.*?</div>', '', content, flags=re.DOTALL | re.IGNORECASE)

    # 2. Add / Update Logo on Slide 1
    if slide == '6889c58f-5abe-4a7a-b7fd-0d9856245d74.htm' or i == 0:
        if 'class="logo"' not in content.lower():
            if '<body>' in content:
                content = content.replace('<body>', '<body>' + logo_html)

    # 3. Fix Slide 9 title
    # Slide 9 in index.html is 467f4cfd-096f-43c8-ae7f-ff5c63804069.htm
    if slide == '467f4cfd-096f-43c8-ae7f-ff5c63804069.htm' or i == 8:
         content = re.sub(r'O\s*MERCADO', 'CONDIÇÕES', content, flags=re.IGNORECASE)

    # 4. Standardise and audit Numbering
    # The user wants "N / 10" style.
    expected_num = f'{i+1:02} / 10'
    
    # Check for either .num-pill or .slide-number (though gold numbering should be gone)
    if 'num-pill' in content:
        # Regex to update the inner text of num-pill
        content = re.sub(r'(<div[^>]*class=["\']?num-pill["\']?[^>]*>)\s*.*?\s*(</div>)', f'\\1{expected_num}\\2', content, flags=re.DOTALL | re.IGNORECASE)
    else:
        # Inject at the start of body
        content = content.replace('<body>', f'<body><div class="num-pill">{expected_num}</div>')

    # 5. Inject Global Style Fixes before head ends
    if '</head>' in content:
        content = content.replace('</head>', global_style + '</head>')

    with open(slide, 'w', encoding='utf-8', errors='ignore') as f:
        f.write(content)
    print(f'Slide {i+1}: Updated {slide}')

print("Standardisation complete.")
