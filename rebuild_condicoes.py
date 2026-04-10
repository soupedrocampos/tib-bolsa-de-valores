import shutil
from bs4 import BeautifulSoup
import re

# Step 1: Re-copy from original slide 8
original_slide = r"c:\Users\pacc1\Downloads\PATRICK\tib site\467f4cfd-096f-43c8-ae7f-ff5c63804069.htm"
condicoes_slide = r"c:\Users\pacc1\Downloads\PATRICK\tib site\condicoes.htm"

shutil.copyfile(original_slide, condicoes_slide)

# Step 2: Open condicoes.htm and parse
with open(condicoes_slide, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

# We know the active slide is s8 because this file was saved when s8 was active.
s8 = soup.find('div', id='s8')

if s8:
    # Let's find the content container in s8
    close_body = s8.find('div', class_='close-body')
    
    if close_body:
        # We replace the entire close_body with our new grid
        new_html = """
        <div class="close-body" style="padding-top:40px; display:flex; flex-direction:column; align-items:center; width: 100%; height:100%; justify-content:center;">
            <p class="sec-label" style="margin-bottom:10px;">THE REAL ESTATE EXPERIENCE</p>
            <h2 class="pablo-name" style="margin-bottom: 50px; text-align: center; text-transform: uppercase;">Condições de Entrada</h2>
            
            <div style="display:grid; grid-template-columns: repeat(2, 1fr); gap: 24px; max-width: 1000px; width: 100%;">
                
                <div style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 40px; text-align: center; display: flex; flex-direction: column; justify-content: center; min-height: 180px;">
                    <div style="font-size:16px; color:rgba(255,255,255,0.6); text-transform:uppercase; letter-spacing:2px; margin-bottom:15px; font-family:'Oswald',sans-serif;">Prazo de Contrato Mínimo</div>
                    <div style="font-size:42px; color:var(--white); font-weight:bold; letter-spacing:1px; line-height: 1;">12 <span style="font-size:24px; color:rgba(255,255,255,0.6);">meses</span></div>
                </div>
                
                <div style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 40px; text-align: center; display: flex; flex-direction: column; justify-content: center; min-height: 180px;">
                    <div style="font-size:16px; color:rgba(255,255,255,0.6); text-transform:uppercase; letter-spacing:2px; margin-bottom:15px; font-family:'Oswald',sans-serif;">Setup Inicial</div>
                    <div style="font-size:42px; color:var(--white); font-weight:bold; letter-spacing:1px; line-height: 1;"><span style="font-size:24px; color:rgba(255,255,255,0.6);">R$</span> 100.000</div>
                    <div style="font-size:16px; color:rgba(255,255,255,0.8); margin-top:15px; font-weight: 300;">+ imóvel de <strong>R$ 500mil</strong> <span style="opacity: 0.7">(particionado)</span></div>
                </div>
                
                <div style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 40px; text-align: center; display: flex; flex-direction: column; justify-content: center; min-height: 180px;">
                    <div style="font-size:16px; color:rgba(255,255,255,0.6); text-transform:uppercase; letter-spacing:2px; margin-bottom:15px; font-family:'Oswald',sans-serif;">Investimento Mensal</div>
                    <div style="font-size:42px; color:var(--white); font-weight:bold; letter-spacing:1px; line-height: 1;"><span style="font-size:24px; color:rgba(255,255,255,0.6);">R$</span> 18.000</div>
                </div>

                <div style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 40px; text-align: center; display: flex; flex-direction: column; justify-content: center; min-height: 180px;">
                    <div style="font-size:16px; color:rgba(255,255,255,0.6); text-transform:uppercase; letter-spacing:2px; margin-bottom:15px; font-family:'Oswald',sans-serif;">Comissão Mínima Exigida</div>
                    <div style="font-size:52px; color:var(--gold); font-weight:bold; letter-spacing:1px; margin-top:-5px; line-height: 1;">8%</div>
                </div>
                
            </div>
        </div>
        """
        new_soup = BeautifulSoup(new_html, 'html.parser')
        close_body.replace_with(new_soup)
        
        # Now update the page numbering exactly like update_numbers.py did
        # For condicoes.htm, it should say 08 / 10.
        nav_nums = soup.find_all('div', class_='nav-num')
        for nav in nav_nums:
            # We want to replace the text with "08 / 10"
            nav.string = "08 / 10"
            
        with open(condicoes_slide, 'w', encoding='utf-8') as f:
            f.write(str(soup))
            
        print("Successfully rebuilt condicoes.htm from scratch, injected grid, and updated slide number to 08/10.")
    else:
        print("Error: close_body not found inside s8.")
else:
    print("Error: s8 not found in the original slide.")

