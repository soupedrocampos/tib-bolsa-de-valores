import re
import os

filepath = r"c:\Users\pacc1\Downloads\PATRICK\tib site\condicoes.htm"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# I will use regex because BeautifulSoup replacing complex strings can be error-prone with formatting and serialization.
# The section starts with <div class="close-body" style="padding-top:30px">
# It ends at the closing </div> of <div class=slide id=s8> which we can just carefully identify by finding <div class="close-body" style="padding-top:30px"> and replacing until the next <div class="slide" id="s9">... wait, SingleFile makes closing tags hard to match.

# Wait, let's just write a python script with BeautifulSoup, it handles HTML replacement beautifully.
from bs4 import BeautifulSoup

soup = BeautifulSoup(content, 'html.parser')
close_body = soup.find('div', class_='close-body')

new_html = """
<div class="close-body" style="padding-top:30px; display:flex; flex-direction:column; align-items:center; height:100%; justify-content:center;">
    <p class="sec-label" style="margin-bottom:15px; font-size:16px;">THE REAL ESTATE EXPERIENCE</p>
    <h2 class="cl-h" style="font-size:48px; text-transform:uppercase; margin:0 auto 50px;">Condições de <span class="g">Adesão</span></h2>
    
    <div style="display:grid; grid-template-columns: repeat(2, 1fr); gap: 24px; max-width: 900px; width: 100%;">
        
        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 35px; text-align: center; transition: transform 0.3s;" onmouseover="this.style.transform='scale(1.02)'" onmouseout="this.style.transform='scale(1)'">
            <div style="font-size:15px; color:var(--gold); text-transform:uppercase; letter-spacing:2px; margin-bottom:15px; font-family:'Oswald',sans-serif; font-weight: 500;">Prazo de Contrato Mínimo</div>
            <div style="font-size:42px; color:var(--white); font-weight:bold; letter-spacing:1px;">12 <span style="font-size:24px; color:rgba(255,255,255,0.6);">meses</span></div>
        </div>
        
        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 35px; text-align: center; transition: transform 0.3s;" onmouseover="this.style.transform='scale(1.02)'" onmouseout="this.style.transform='scale(1)'">
            <div style="font-size:15px; color:var(--gold); text-transform:uppercase; letter-spacing:2px; margin-bottom:15px; font-family:'Oswald',sans-serif; font-weight: 500;">Setup Inicial</div>
            <div style="font-size:42px; color:var(--white); font-weight:bold; letter-spacing:1px;"><span style="font-size:24px; color:rgba(255,255,255,0.6);">R$</span> 100k</div>
            <div style="font-size:14px; color:rgba(255,255,255,0.7); margin-top:10px; font-weight: 300;">+ 1 imóvel de <strong>R$ 500mil</strong> (particionado)</div>
        </div>
        
        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 35px; text-align: center; transition: transform 0.3s;" onmouseover="this.style.transform='scale(1.02)'" onmouseout="this.style.transform='scale(1)'">
            <div style="font-size:15px; color:var(--gold); text-transform:uppercase; letter-spacing:2px; margin-bottom:15px; font-family:'Oswald',sans-serif; font-weight: 500;">Investimento Mensal</div>
            <div style="font-size:42px; color:var(--white); font-weight:bold; letter-spacing:1px;"><span style="font-size:24px; color:rgba(255,255,255,0.6);">R$</span> 18k</div>
            <div style="font-size:14px; color:rgba(255,255,255,0.5); margin-top:10px; font-weight: 300;">Direcionados para tráfego e campanhas estratégicas</div>
        </div>

        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 35px; text-align: center; transition: transform 0.3s;" onmouseover="this.style.transform='scale(1.02)'" onmouseout="this.style.transform='scale(1)'">
            <div style="font-size:15px; color:var(--gold); text-transform:uppercase; letter-spacing:2px; margin-bottom:15px; font-family:'Oswald',sans-serif; font-weight: 500;">Comissão Mínima Exigida</div>
            <div style="font-size:52px; color:var(--white); font-weight:bold; letter-spacing:1px; margin-top:-5px;">8<span style="font-size:36px; color:var(--gold);">%</span></div>
        </div>
        
    </div>
</div>
"""

new_soup = BeautifulSoup(new_html, 'html.parser')
close_body.replace_with(new_soup)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(str(soup))
