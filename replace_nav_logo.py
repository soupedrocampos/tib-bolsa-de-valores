"""
replace_nav_logo.py
Substitui o texto "TIB <b>| The Best Invest</b>" no nav-logo de todos os
slides pelo logotipo (LOGO.png) embutido como base64 — sem dependência
de arquivo externo, mantendo os slides self-contained.

Uso: python replace_nav_logo.py
"""

import os
import glob
import base64

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(BASE_DIR, "LOGO.png")

SENTINEL = "--tib-nav-logo:1;"

# Unquoted variant (9 UUID files)
OLD_UQ = 'class=nav-logo>TIB <b>| The Best Invest</b></div>'
# Double-quoted variant (condicoes.htm)
OLD_DQ = 'class="nav-logo">TIB <b>| The Best Invest</b></div>'


def make_logo_tag(b64):
    return (
        'class=nav-logo>'
        f'<img src="data:image/png;base64,{b64}" '
        'alt="TIB | The Best Invest" '
        'style="height:36px;width:auto;display:block;'
        'filter:brightness(0) invert(1)">'
        '</div>'
    )


def make_logo_tag_dq(b64):
    return (
        'class="nav-logo">'
        f'<img src="data:image/png;base64,{b64}" '
        'alt="TIB | The Best Invest" '
        'style="height:36px;width:auto;display:block;'
        'filter:brightness(0) invert(1)">'
        '</div>'
    )


def process_file(filepath, b64):
    name = os.path.basename(filepath)
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    if SENTINEL in content:
        print(f"[SKIP] {name}")
        return False

    original = content
    changes = []

    if OLD_UQ in content:
        content = content.replace(OLD_UQ, make_logo_tag(b64))
        changes.append("nav-logo text -> img (unquoted)")

    if OLD_DQ in content:
        content = content.replace(OLD_DQ, make_logo_tag_dq(b64))
        changes.append("nav-logo text -> img (double-quoted)")

    # Stamp sentinel in existing injected <style> block
    if "--tib-inline-r2:1;" in content:
        content = content.replace("--tib-inline-r2:1;", f"--tib-inline-r2:1;\n  {SENTINEL}")
    elif "--tib-inline-refactored:1;;" in content:
        content = content.replace("--tib-inline-refactored:1;;", f"--tib-inline-refactored:1;;\n  {SENTINEL}")
    else:
        # fallback: append a tiny style block before yd-sidebar or end of file
        sentinel_block = f"<style>/* TIB nav logo replaced */\n  {SENTINEL}\n</style>\n"
        if "<yd-sidebar>" in content:
            content = content.replace("<yd-sidebar>", sentinel_block + "<yd-sidebar>", 1)
        else:
            content += "\n" + sentinel_block

    if content != original:
        with open(filepath, "w", encoding="utf-8", errors="ignore") as f:
            f.write(content)
        print(f"[OK]   {name}")
        for c in changes:
            print(f"       + {c}")
        return True
    else:
        print(f"[--]   {name} (sem alteracoes)")
        return False


def main():
    if not os.path.exists(LOGO_PATH):
        print(f"ERRO: LOGO.png nao encontrado em {LOGO_PATH}")
        return

    with open(LOGO_PATH, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    print(f"LOGO.png carregado ({len(b64)} chars base64)\n")

    htm_files = sorted(glob.glob(os.path.join(BASE_DIR, "*.htm")))
    print(f"=== Substituindo nav-logo em {len(htm_files)} arquivo(s) ===\n")

    updated = 0
    for fp in htm_files:
        if process_file(fp, b64):
            updated += 1

    print(f"\nConcluido: {updated}/{len(htm_files)} arquivo(s) atualizado(s).")


if __name__ == "__main__":
    main()
