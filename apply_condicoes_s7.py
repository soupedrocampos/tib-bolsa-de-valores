from bs4 import BeautifulSoup
import re

filepath = r"c:\Users\pacc1\Downloads\PATRICK\tib site\condicoes.htm"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

soup = BeautifulSoup(content, 'html.parser')

# Find slide s7 which is the old "O Mercado" slide, now our conditions slide
slide_s7 = soup.find('div', id='s7')

if slide_s7:
    close_body = slide_s7.find('div', class_='close-body')
    if close_body:
        new_html = """
        <div class="close-body" style="padding-top:40px; display:flex; flex-direction:column; align-items:center; width: 100%;">
            <p class="sec-label" style="margin-bottom:10px;">THE REAL ESTATE EXPERIENCE</p>
            <h2 class="pablo-name" style="margin-bottom: 50px; text-align: center;">Condições de Entrada</h2>
            
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
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print("Updated condicoes.htm successfully.")
    else:
        print("Could not find close-body inside s7")
else:
    print("Could not find s7")

