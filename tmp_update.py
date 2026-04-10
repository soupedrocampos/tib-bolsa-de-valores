import glob, os

files = glob.glob('*.htm')
for f in files:
    if 'a23cc662' in f or 'condicoes' in f: continue
    
    with open(f, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()
        
    original_content = content
    
    # 1. ADD numbers to flip cards
    content = content.replace(
        '<div class=flip-front-title>Construtoras</div>',
        '<div class="flip-front-title" style="margin-bottom: 5px;">10</div><div class=flip-front-title>Construtoras</div>'
    )
    content = content.replace(
        '<div class=flip-front-title>Corretores<br>Diretos</div>',
        '<div class="flip-front-title" style="margin-bottom: 5px;">150</div><div class=flip-front-title>Corretores<br>Diretos</div>'
    )
    content = content.replace(
        '<div class=flip-front-title>Investidores<br>Ativos</div>',
        '<div class="flip-front-title" style="margin-bottom: 5px;">+1M</div><div class=flip-front-title>Investidores<br>Ativos</div>'
    )

    # 2. FIX partner names and swap
    content = content.replace('<div class=partner-name>Peixoto</div>', '<div class=partner-name>TEMP_PEIXOTO</div>')
    content = content.replace('<div class=partner-name>DomPierri</div>', '<div class="partner-name" style="white-space:nowrap;font-size:0.75em;">Peixoto</div>')
    content = content.replace('<div class=partner-name>TEMP_PEIXOTO</div>', '<div class="partner-name" style="white-space:nowrap;font-size:0.75em;">Dom Pierre</div>')
    content = content.replace('<div class=partner-name>Patrick<br>Piccoli</div>', '<div class="partner-name" style="white-space:nowrap;font-size:0.75em;">Patrick Piccoli</div>')
    content = content.replace('<div class=partner-name>Cristian<br>Nascimento</div>', '<div class="partner-name" style="white-space:nowrap;font-size:0.63em;">Cristian Nascimento</div>')

    if content != original_content:
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
print('Done processing names and flip cards.')
