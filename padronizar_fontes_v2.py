import re
import os
import glob

MIN_PX = 20.0
TARGET_PX = 22

files = glob.glob('*.htm')

def fix_font_sizes(content):
    """
    Substitui font-size: Xpx onde X < MIN_PX por TARGET_PXpx.
    Preserva: clamp(), em, rem, %, vw, vh, var().
    """
    
    # Padrão mais amplo: font-size seguido de espaços/dois pontos e um valor
    pattern = re.compile(
        r'(font-size\s*:\s*)([\d.]+)(px)',
        re.IGNORECASE
    )
    
    def replacer(m):
        prefix  = m.group(1)
        num_str = m.group(2)
        unit    = m.group(3)
        
        try:
            num = float(num_str)
        except ValueError:
            return m.group(0)
        
        if num < MIN_PX:
            return prefix + str(TARGET_PX) + unit
        return m.group(0)
    
    return pattern.sub(replacer, content)

total = 0
for f in sorted(files):
    with open(f, 'r', encoding='utf-8', errors='ignore') as fh:
        original = fh.read()
    
    new_content = fix_font_sizes(original)
    
    if new_content != original:
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(new_content)
        
        # Conta mudancas
        orig_matches = re.findall(r'font-size\s*:\s*([\d.]+)px', original, re.IGNORECASE)
        new_matches  = re.findall(r'font-size\s*:\s*([\d.]+)px', new_content, re.IGNORECASE)
        changed = sum(1 for o, n in zip(orig_matches, new_matches) if o != n)
        total += changed
        print('ATUALIZADO: ' + f + ' (' + str(changed) + ' ocorrencias)')
    else:
        print('OK (sem mudanca): ' + f)

print('')
print('Total de ocorrencias atualizadas: ' + str(total))

# Verificacao final
print('')
print('=== VERIFICACAO FINAL ===')
for f in sorted(files):
    content = open(f, encoding='utf-8', errors='ignore').read()
    sizes_px = re.findall(r'font-size\s*:\s*([\d.]+)px', content, re.IGNORECASE)
    small = [s for s in sizes_px if float(s) < MIN_PX]
    if small:
        print('ATENCAO ' + f + ': ainda tem < 20px: ' + str(sorted(set(small))))
    else:
        all_px = sorted(set(sizes_px), key=float)
        print('OK ' + f + ': menores=' + str(all_px[:3]) + '...')
