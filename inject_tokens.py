"""
inject_tokens.py
Injeta os tokens de design faltantes (espaçamento, opacidades, tipografia)
no bloco :root de todos os slides .htm do projeto TIB.

Uso: python inject_tokens.py
"""

import re
import os
import glob

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Tokens a injetar — apenas os que NÃO existem nos slides
MISSING_TOKENS = """
  /* --- Opacidades gold adicionais --- */
  --gold-50:rgba(217,184,85,0.50);
  --gold-45:rgba(217,184,85,0.45);
  --gold-30:rgba(217,184,85,0.30);
  --gold-20:rgba(217,184,85,0.20);
  --gold-15:rgba(217,184,85,0.15);
  --gold-10:rgba(217,184,85,0.10);
  --gold-grad-rev:linear-gradient(135deg,#D9B855 0%,#F2DEA0 40%,#D9B36C 65%,#A66617 100%);
  /* --- Background padrão --- */
  --bg:linear-gradient(160deg,#010A26 0%,#00113F 55%,#011640 100%);
  /* --- Opacidades branco adicionais --- */
  --white-80:rgba(255,255,255,0.80);
  --white-40:rgba(255,255,255,0.40);
  --white-25:rgba(255,255,255,0.25);
  --white-12:rgba(255,255,255,0.12);
  --white-05:rgba(255,255,255,0.05);
  --white-04:rgba(255,255,255,0.04);
  --white-02:rgba(255,255,255,0.02);
  /* --- Tipografia --- */
  --font-display:"Oswald",sans-serif;
  --font-body:"Raleway",sans-serif;
  --text-xs:14px;
  --text-sm:18px;
  --text-md:22px;
  --text-lg:28px;
  --text-xl:34px;
  --text-2xl:48px;
  --text-3xl:52px;
  --text-fluid-sm:clamp(38px,5.5vw,80px);
  --text-fluid-md:clamp(44px,7vw,96px);
  --text-fluid-lg:clamp(52px,6vw,88px);
  --text-fluid-xl:clamp(80px,11vw,175px);
  /* --- Espaçamento (escala base 4px) --- */
  --sp-1:4px;
  --sp-2:8px;
  --sp-3:12px;
  --sp-4:16px;
  --sp-5:20px;
  --sp-6:24px;
  --sp-7:28px;
  --sp-8:32px;
  --sp-9:36px;
  --sp-10:40px;
  --sp-12:48px;
  --sp-14:56px;
  --sp-16:64px;
  --sp-20:80px;
  /* --- Raios de borda --- */
  --radius-sm:4px;
  --radius-md:8px;
  --radius-lg:12px;
  --radius-xl:16px;
  --radius-pill:999px;
  /* --- Bordas padrão --- */
  --border-gold:1px solid rgba(217,184,85,0.30);
  --border-white:1px solid rgba(255,255,255,0.20);
  /* --- Z-index --- */
  --z-slide:1;
  --z-ui:100;
  --z-nav:9998;
  --z-cursor:9999;
  /* --- Transições --- */
  --transition-fast:0.15s ease-out;
  --transition-base:0.3s ease;
  --transition-slow:0.75s ease;"""

SENTINEL = "--tib-tokens-injected:1;"


def inject_into_file(filepath):
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    if SENTINEL in content:
        print(f"  [SKIP] já processado: {os.path.basename(filepath)}")
        return False

    # Localiza o bloco :root{...} — pode estar comprimido (sem espaços)
    root_pattern = re.compile(r'(:root\s*\{)(.*?)\}', re.DOTALL)
    match = root_pattern.search(content)

    if not match:
        print(f"  [WARN] :root não encontrado em: {os.path.basename(filepath)}")
        return False

    original_root_open = match.group(1)
    original_root_body = match.group(2)
    original_full = match.group(0)

    # Monta o novo bloco :root com os tokens extras no final
    new_root = (
        original_root_open
        + original_root_body
        + SENTINEL
        + MISSING_TOKENS
        + "}"
    )

    new_content = content.replace(original_full, new_root, 1)

    with open(filepath, "w", encoding="utf-8", errors="ignore") as f:
        f.write(new_content)

    print(f"  [OK]   tokens injetados: {os.path.basename(filepath)}")
    return True


def main():
    htm_files = glob.glob(os.path.join(BASE_DIR, "*.htm"))
    if not htm_files:
        print("Nenhum arquivo .htm encontrado.")
        return

    print(f"Processando {len(htm_files)} arquivo(s)...\n")
    updated = 0
    for fp in sorted(htm_files):
        if inject_into_file(fp):
            updated += 1

    print(f"\nConcluído: {updated}/{len(htm_files)} arquivo(s) atualizado(s).")


if __name__ == "__main__":
    main()
