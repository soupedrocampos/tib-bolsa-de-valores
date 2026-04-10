import re
import os

files = [
    '6889c58f-5abe-4a7a-b7fd-0d9856245d74.htm',
    'd44e90f7-4cba-419a-8fb6-e67b9f1c3244.htm',
    'fed32750-c044-4f3c-85eb-569045ba5cd5.htm',
    'a23cc662-dd07-4e88-ad78-4390fb4159b5.htm',
    'decb2a9f-0689-4ab8-be02-57d48b45364d.htm',
    '2595c031-784a-4bcc-926b-40930d15d505.htm',
    'b52cd9d4-d5d6-4bfd-b3c8-3978f01817dc.htm',
    'condicoes.htm',
    '467f4cfd-096f-43c8-ae7f-ff5c63804069.htm',
    '8ca20ea5-73c0-45e7-bbc7-9318fcf90089.htm',
]

MIN_FONT_SIZE = 20.0   # px — abaixo disso será elevado
TARGET_FONT_SIZE = 22  # px — novo tamanho mínimo

def replace_small_font(match):
    """Substitui font-size < 20px por 22px. Ignora clamp(), em, rem, %."""
    original = match.group(0)
    value_str = match.group(1)
    
    # Ignora clamp() e valores não-px
    if 'clamp' in value_str or 'em' in value_str or 'rem' in value_str or '%' in value_str or 'vw' in value_str or 'vh' in value_str:
        return original
    
    # Extrai o número
    num_match = re.match(r'^(\d+(?:\.\d+)?)\s*px', value_str.strip())
    if not num_match:
        return original
    
    num = float(num_match.group(1))
    
    if num < MIN_FONT_SIZE:
        # Substitui mantendo o prefixo (ex: "font-size:" ou "font-size: ")
        new_val = original.replace(match.group(1), f'{TARGET_FONT_SIZE}px')
        return new_val
    
    return original

# Padrão para capturar font-size em CSS inline e blocos de estilo
# Captura: font-size: VALOR (com possíveis espaços e !important)
font_size_pattern = re.compile(
    r'(font-size\s*:\s*)([^;}"\'!\s][^;}"\'!]*?)(\s*(?:!important)?\s*(?=[;}\"\']))',
    re.IGNORECASE
)

def replace_font_in_line(line):
    """Substitui font-sizes pequenos em uma linha."""
    
    def replacer(m):
        prefix = m.group(1)   # "font-size: "
        value  = m.group(2)   # "12px" ou "0.75em" etc.
        suffix = m.group(3)   # ";" ou "!important;"
        
        value = value.strip()
        
        # Ignora unidades relativas e funções
        if any(x in value for x in ['clamp', 'em', 'rem', '%', 'vw', 'vh', '#', 'var(']):
            return m.group(0)
        
        # Tenta extrair número + px
        num_match = re.match(r'^(\d+(?:\.\d+)?)\s*px$', value)
        if not num_match:
            return m.group(0)
        
        num = float(num_match.group(1))
        if num < MIN_FONT_SIZE:
            return f'{prefix}{TARGET_FONT_SIZE}px{suffix}'
        
        return m.group(0)
    
    return font_size_pattern.sub(replacer, line)


total_changes = 0

for fname in files:
    if not os.path.exists(fname):
        print(f'⚠️  Não encontrado: {fname}')
        continue
    
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    original = content
    
    # Aplicar substituição linha a linha para contar mudanças
    lines = content.split('\n')
    new_lines = []
    file_changes = 0
    
    for line in lines:
        new_line = replace_font_in_line(line)
        if new_line != line:
            file_changes += 1
        new_lines.append(new_line)
    
    new_content = '\n'.join(new_lines)
    
    if new_content != original:
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'[OK] {fname} -- {file_changes} linha(s) alterada(s)')
    else:
        print(f'[--] {fname} -- sem alteracoes')
    
    total_changes += file_changes

print(f'\n[DONE] Total de linhas alteradas: {total_changes}')
print(f'   Regra: font-size < {MIN_FONT_SIZE}px -> {TARGET_FONT_SIZE}px')
print(f'   (clamp, em, rem, %, vw, vh foram preservados)')
