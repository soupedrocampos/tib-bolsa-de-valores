from bs4 import BeautifulSoup
import re

filepath = r"c:\Users\pacc1\Downloads\PATRICK\tib site\condicoes.htm"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

soup = BeautifulSoup(content, 'html.parser')

element = soup.find(string=re.compile(r'100K PELA', re.IGNORECASE))
if element:
    parent = element.parent
    while parent and not (parent.name == 'div' and 'close-body' in parent.get('class', [])):
        parent = parent.parent
    
    if parent:
        new_html = """
        <div class="close-body" style="padding-top:40px; display:flex; flex-direction:column; align-items:center; width: 100%;">
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
                    <div style="font-size:16px; color:rgba(255,255,255,0.8); margin-top:15px; font-weight: 300;">+ imóvel a partir de <strong>R$ 500mil</strong> <span style="opacity: 0.7">(particionado)</span></div>
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
        parent.replace_with(new_soup)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print("Updated condicoes.htm successfully! Found exact matching slide text.")
    else:
        print("Could not find close-body parent")
else:
    print("Could not find the 100k string. Here are the texts found:")
    for text in soup.stripped_strings:
        if '100' in text:
            print(repr(text))
