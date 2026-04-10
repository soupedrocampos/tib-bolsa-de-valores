import re
import os
import glob

# Gradiente dourado metalizado - simula reflexo de metal polido
GOLD_GRADIENT_CSS = (
    "background: linear-gradient(135deg, #BF953F 0%, #FDE992 20%, #B38728 40%, #FCF6BA 60%, #AA771C 80%, #E8C84A 100%);"
    "-webkit-background-clip: text;"
    "-webkit-text-fill-color: transparent;"
    "background-clip: text;"
)

# Versao para substituir dentro de blocos CSS (regras de classe)
# Ex: color: var(--gold) => [gradiente]
GOLD_GRADIENT_BLOCK = (
    "background: linear-gradient(135deg, #BF953F 0%, #FDE992 20%, #B38728 40%, #FCF6BA 60%, #AA771C 80%, #E8C84A 100%);\n"
    "    -webkit-background-clip: text;\n"
    "    -webkit-text-fill-color: transparent;\n"
    "    background-clip: text;"
)

files = glob.glob('*.htm')

# CSS de animacao de brilho metalico a ser injetado em cada arquivo
METAL_SHIMMER_CSS = """
/* === EFEITO METALICO DOURADO === */
@keyframes goldShimmer {
  0%   { background-position: -200% center; }
  100% { background-position: 200% center; }
}

/* Aplicado via JS abaixo a todos elementos com text-fill transparent */
.gold-metal-text {
  background: linear-gradient(
    110deg,
    #7A5C00 0%,
    #BF953F 15%,
    #FDE992 30%,
    #FCF6BA 40%,
    #B38728 55%,
    #FBD85D 70%,
    #AA771C 85%,
    #E8C84A 100%
  );
  background-size: 200% auto;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: goldShimmer 4s linear infinite;
}
"""

def process_file(fname):
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    original = content
    changes = 0
    
    # --- PASSO 1: Substituir em blocos <style> ---
    # Encontrar blocos de estilo
    def process_style_block(m):
        nonlocal changes
        block = m.group(0)
        original_block = block
        
        # Substituir "color: var(--gold)" dentro de regras CSS
        # Padrao: color\s*:\s*var\(--gold\)\s*;?
        def replace_color_gold(cm):
            nonlocal changes
            changes += 1
            indent = cm.group(1) if cm.group(1) else '    '
            important = ' !important' if '!important' in cm.group(0) else ''
            return (
                f"{indent}background: linear-gradient(110deg, #7A5C00 0%, #BF953F 15%, #FDE992 30%, "
                f"#FCF6BA 40%, #B38728 55%, #FBD85D 70%, #AA771C 85%, #E8C84A 100%) !important;\n"
                f"{indent}background-size: 200% auto !important;\n"
                f"{indent}-webkit-background-clip: text !important;\n"
                f"{indent}-webkit-text-fill-color: transparent !important;\n"
                f"{indent}background-clip: text !important;\n"
                f"{indent}animation: goldShimmer 4s linear infinite !important;"
            )
        
        block = re.sub(
            r'([ \t]*)color\s*:\s*var\(--gold\)\s*(?:!important\s*)?;',
            replace_color_gold,
            block
        )
        
        return block
    
    content = re.sub(r'<style[^>]*>.*?</style>', process_style_block, content, flags=re.DOTALL | re.IGNORECASE)
    
    # --- PASSO 2: Substituir em estilos inline ---
    # Ex: style="... color: var(--gold) ..."
    def replace_inline_gold(m):
        nonlocal changes
        style_attr = m.group(1)
        if 'var(--gold)' not in style_attr:
            return m.group(0)
        
        # Remove color: var(--gold) e adiciona gradiente
        new_style = re.sub(
            r'color\s*:\s*var\(--gold\)\s*(?:!important\s*)?;?',
            (
                'background: linear-gradient(110deg, #7A5C00 0%, #BF953F 15%, #FDE992 30%, '
                '#FCF6BA 40%, #B38728 55%, #FBD85D 70%, #AA771C 85%, #E8C84A 100%);'
                'background-size:200% auto;'
                '-webkit-background-clip:text;'
                '-webkit-text-fill-color:transparent;'
                'background-clip:text;'
                'animation:goldShimmer 4s linear infinite;'
            ),
            style_attr
        )
        
        if new_style != style_attr:
            changes += 1
        
        return f'style="{new_style}"'
    
    content = re.sub(r'style="([^"]*)"', replace_inline_gold, content, flags=re.IGNORECASE)
    
    # --- PASSO 3: Injetar CSS de animacao antes do </style> ---
    if METAL_SHIMMER_CSS not in content:
        # Insere antes do primeiro </style>
        content = content.replace('</style>', METAL_SHIMMER_CSS + '\n</style>', 1)
    
    if content != original:
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(content)
        print('[OK] ' + fname + ' -- ' + str(changes) + ' substituicoes')
    else:
        print('[--] ' + fname + ' -- sem mudancas')

for f in sorted(files):
    process_file(f)

print('')
print('[DONE] Efeito de ouro metalizado aplicado em todos os slides.')
print('       Cores afetadas: color: var(--gold) => gradiente metalico animado')
