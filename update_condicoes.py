import re

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    replacements = {
        r'Posicionamento Final': r'Condições Estratégicas',
        r'Não estamos criando uma imobiliária\.': r'Para participar da primeira bolsa de valores',
        r'Estamos criando um novo mercado<br>de inteligência focado em performance\.': r'imobiliária da América Latina, as seguintes regras se aplicam:',
        r'Se você é uma construtora que busca:': r'Condições de Entrada:',
        r'Escala em vendas': r'100k pela Vaga exclusiva',
        r'Posicionamento estratégico': r'18k mensal (direcionados para tráfego e campanhas estratégicas)',
        r'Acesso Direto ao Investidor Certo': r'1 imóvel a partir de 500k (para ser particionado)'
    }

    for k, v in replacements.items():
        content, count = re.subn(k, v, content)
        if count == 0:
            print(f"Warning: Could not replace {k}")
        else:
            print(f"Replaced {k}")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

update_file(r"c:\Users\pacc1\Downloads\PATRICK\tib site\condicoes.htm")
