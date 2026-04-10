import os
import re

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

def style_num(number):
    return f'<div class="card-number" style="font-size: 110px; font-weight: bold; font-family: \'Oswald\', sans-serif; color: #F8F25C; text-shadow: 0px 4px 15px rgba(0,0,0,0.5); background: linear-gradient(135deg, #FFEA2E 0%, #E8D021 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; margin-bottom: -20px; line-height: 1;">{number}</div>'


for slide in slides:
    if not os.path.exists(slide): continue
    
    with open(slide, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # 1. FIX THE BULL (Remove aggressive CSS that hid all images with TIB in alt)
    content = content.replace('img[alt*="TIB"], img[alt*="Best Invest"] { display: none !important; }', '')
    
    # Forcefully remove the specific old text logo img if it's there
    content = re.sub(r'<img[^>]*alt=["\']TIB \| The Best Invest["\'][^>]*>', '', content, flags=re.IGNORECASE)

    # 2. Add numbers to slide 4 ONLY
    if slide == 'a23cc662-dd07-4e88-ad78-4390fb4159b5.htm':
        # Remove old ones just in case script is run twice
        content = re.sub(r'<div class="card-number"[^>]*>.*?</div>', '', content, flags=re.DOTALL)
        
        # Inject new numbers
        content = content.replace('<div class=flip-front-title>Construtoras</div>', 
                                  f'<div class=flip-front-title>{style_num("10")}Construtoras</div>')
        content = content.replace('<div class=flip-front-title>Corretores<br>Diretos</div>', 
                                  f'<div class=flip-front-title>{style_num("150")}Corretores<br>Diretos</div>')
        content = content.replace('<div class=flip-front-title>Investidores<br>Ativos</div>', 
                                  f'<div class=flip-front-title>{style_num("+1M")}Investidores<br>Ativos</div>')

    with open(slide, 'w', encoding='utf-8', errors='ignore') as f:
        f.write(content)
    
    print(f'Fixed {slide}')

print("Done. Check slide 4 and slide 1.")
