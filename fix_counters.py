"""
fix_counters.py
Corrige num-pill e tags de navegacao em todos os slides do projeto TIB.

Mudancas aplicadas em todos os .htm:
  1. Slide 1 hero: nav-pill TREE -> 01 / 10
  2. Slide 7 CTA:  num-pill TREE -> 07 / 10
  3. Slide 9:      tag "O Mercado" -> "Condicoes"
  4. Slide 9:      pill 08 / 10 -> 09 / 10 (nos arquivos com valor errado)
  5. Slide 10:     The Real Estate Experience pill 09 / 10 -> 10 / 10

Uso: python fix_counters.py
"""

import re
import os
import glob

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def fix_file(filepath):
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    original = content
    changes = []

    # ------------------------------------------------------------------
    # Fix 1: Slide 1 hero nav-pill TREE -> 01 / 10
    # Formato: <div class=nav-pill>TREE</div>
    # ------------------------------------------------------------------
    old = "<div class=nav-pill>TREE</div>"
    new = "<div class=nav-pill>01 / 10</div>"
    if old in content:
        content = content.replace(old, new)
        changes.append("nav-pill TREE -> 01 / 10 (slide 1)")

    # ------------------------------------------------------------------
    # Fix 2: Slide 7 CTA num-pill TREE -> 07 / 10
    # Formato: <div class=num-pill>TREE</div>
    # ------------------------------------------------------------------
    old = "<div class=num-pill>TREE</div>"
    new = "<div class=num-pill>07 / 10</div>"
    if old in content:
        content = content.replace(old, new)
        changes.append("num-pill TREE -> 07 / 10 (slide 7)")

    # Variante com aspas duplas (condicoes.htm pode usar este formato)
    old = '<div class="num-pill">TREE</div>'
    new = '<div class="num-pill">07 / 10</div>'
    if old in content:
        content = content.replace(old, new)
        changes.append('num-pill "TREE" -> "07 / 10" (slide 7, aspas duplas)')

    # ------------------------------------------------------------------
    # Fix 3: Slide 9 tag "O Mercado" -> "Condicoes"
    # Formatos sem aspas e com aspas duplas
    # ------------------------------------------------------------------
    for old, new in [
        ("<div class=tag>O Mercado</div>", "<div class=tag>Condi\u00e7\u00f5es</div>"),
        ('<div class="tag">O Mercado</div>', '<div class="tag">Condi\u00e7\u00f5es</div>'),
    ]:
        if old in content:
            content = content.replace(old, new)
            changes.append("tag O Mercado -> Condicoes (slide 9)")

    # ------------------------------------------------------------------
    # Fix 4: Slide 9 pill 08 / 10 -> 09 / 10 (somente apos tag Condicoes)
    # ------------------------------------------------------------------
    for tag_open, pill_sep in [
        ("<div class=tag>Condi\u00e7\u00f5es</div>\n <div class=num-pill>", None),
        ('<div class="tag">Condi\u00e7\u00f5es</div>\n<div class="num-pill">', None),
        ("<div class=tag>Condi\u00e7\u00f5es</div>\n<div class=num-pill>", None),
    ]:
        old_pill = tag_open + "08 / 10</div>"
        new_pill = tag_open + "09 / 10</div>"
        if old_pill in content:
            content = content.replace(old_pill, new_pill)
            changes.append("pill 08 / 10 -> 09 / 10 (slide 9 Condicoes)")

    # ------------------------------------------------------------------
    # Fix 5: Slide 10 The Real Estate Experience pill 09 / 10 -> 10 / 10
    # (o slide 7 ja foi corrigido para 07/10, entao apenas o slide 10 tem 09/10)
    # ------------------------------------------------------------------
    for tag_open in [
        "<div class=tag>The Real Estate Experience</div>\n <div class=num-pill>",
        '<div class="tag">The Real Estate Experience</div>\n<div class="num-pill">',
        "<div class=tag>The Real Estate Experience</div>\n<div class=num-pill>",
    ]:
        old_pill = tag_open + "09 / 10</div>"
        new_pill = tag_open + "10 / 10</div>"
        if old_pill in content:
            content = content.replace(old_pill, new_pill)
            changes.append("pill 09 / 10 -> 10 / 10 (slide 10)")

    if content != original:
        with open(filepath, "w", encoding="utf-8", errors="ignore") as f:
            f.write(content)
        print("[OK]   " + os.path.basename(filepath))
        for c in changes:
            print("       + " + c)
    else:
        print("[--]   " + os.path.basename(filepath) + " (sem alteracoes)")

    return content != original


def verify(filepath):
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    tags  = re.findall(r'<div class=.?tag.?>(.*?)</div>', content)
    pills = re.findall(r'<div class=.{0,4}(?:num|nav)-pill.?>(.*?)</div>', content)
    return list(zip(tags, pills))


def main():
    htm_files = sorted(glob.glob(os.path.join(BASE_DIR, "*.htm")))
    if not htm_files:
        print("Nenhum arquivo .htm encontrado.")
        return

    print("=== Aplicando correcoes em " + str(len(htm_files)) + " arquivo(s) ===\n")
    for fp in htm_files:
        fix_file(fp)

    print("\n=== Verificacao final ===\n")
    wrong_pills = {"TREE", "08 / 10"}  # pills que nao devem mais aparecer

    for fp in htm_files:
        name = os.path.basename(fp)
        pairs = verify(fp)
        has_error = any(pill in wrong_pills for _, pill in pairs)
        status = "ERRO" if has_error else "OK"
        print("[" + status + "] " + name[:35])
        for tag, pill in pairs:
            marker = "!" if pill in wrong_pills else " "
            print("  " + marker + " [" + pill + "] " + tag[:40])
        print()


if __name__ == "__main__":
    main()
