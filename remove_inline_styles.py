"""
remove_inline_styles.py
Move inline styles to reusable CSS classes across all TIB slides.

Classes created/augmented:
  .logo-img         — partner logo images (height:50px)
  .deco-figure      — decorative hero figure (position:absolute, right:5%, etc.)
  .sec-card--left   — sec-card alignment variant (left-aligned padding)
  .flip-front-title — adds margin-bottom:5px (already has font styles)
  .slide-bg-dark    — adds radial-gradient background
  .sc-desc          — adds flex layout (font-size already in class CSS)
  .stat-grid        — grid container for CTA stat cards (condicoes.htm)
  .stat-card        — individual stat card box
  .stat-label       — stat card label text
  .stat-value       — stat card value text
  .stat-unit        — stat card unit suffix

Usage: python remove_inline_styles.py
"""

import os
import re
import glob

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SENTINEL = "--tib-inline-refactored:1;"

# New CSS rules to inject into each file (appended as a <style> block)
INJECTED_CSS = """
  /* --- TIB: inline styles moved to classes (%s) --- */
  %s
  /* Logo images (partner boxes) */
  .logo-img{height:50px;width:auto;display:block}
  /* Decorative hero figure */
  .deco-figure{position:absolute;right:5%%;bottom:0;height:85%%;width:auto;object-fit:contain;z-index:1;pointer-events:none;filter:drop-shadow(0 0 30px rgba(0,0,0,.8))}
  /* Sec-card left-aligned variant */
  .sec-card--left{align-items:flex-start;text-align:left;padding:26px 20px}
  /* Flip card title spacing */
  .flip-front-title{margin-bottom:5px}
  /* Dark radial slide background */
  .slide-bg-dark{background:radial-gradient(circle at right center,rgba(30,40,60,1) 0%%,var(--bg) 100%%)}
  /* Section description flex layout */
  .sc-desc{display:flex;flex-direction:column;gap:var(--sp-3)}
"""

# Stat card CSS — only for condicoes.htm
STAT_CSS = """
  /* Stat cards (CTA slide) */
  .stat-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:var(--sp-6);max-width:1000px;width:100%}
  .stat-card{background:var(--white-05);border:1px solid rgba(255,255,255,.1);border-radius:var(--radius-lg);padding:40px;text-align:center;display:flex;flex-direction:column;justify-content:center;min-height:180px}
  .stat-label{font-size:var(--text-md);color:var(--white-60);text-transform:uppercase;letter-spacing:2px;margin-bottom:15px;font-family:var(--font-display)}
  .stat-value{font-size:42px;color:var(--white);font-weight:bold;letter-spacing:1px;line-height:1}
  .stat-unit{font-size:24px;color:var(--white-60)}
  .stat-note{font-size:var(--text-md);color:rgba(255,255,255,.8);margin-top:15px;font-weight:300}
"""


def inject_css(content, is_condicoes):
    """Inject new CSS rules before </body>."""
    stat_block = STAT_CSS if is_condicoes else ""
    css_block = INJECTED_CSS % (SENTINEL, SENTINEL + ";")
    css_block += stat_block

    new_style = "<style>" + css_block + "</style>\n"

    # Insert before </body>
    content = content.replace("</body>", new_style + "</body>", 1)
    return content


# ---------------------------------------------------------------------------
# Transformation helpers — each returns (new_content, change_count)
# ---------------------------------------------------------------------------

def fix_logo_images(content):
    """Replace style='height: 50px; width: auto; display: block;' on <img> with class='logo-img'."""
    count = 0
    old = 'style="height: 50px; width: auto; display: block;"'
    new = 'class="logo-img"'

    while old in content:
        content = content.replace(old, new)
        count += 1

    return content, count


def fix_deco_figure(content):
    """Replace the decorative figure inline style with class='deco-figure'."""
    count = 0
    DECO_STYLE = 'style="position:absolute;right:5%;bottom:0;height:85%;width:auto;object-fit:contain;z-index:1;pointer-events:none;filter:drop-shadow(0 0 30px rgba(0,0,0,0.8))"'
    NEW = 'class="deco-figure"'

    if DECO_STYLE in content:
        content = content.replace(DECO_STYLE, NEW)
        count = 1

    return content, count


def fix_sec_card_left(content):
    """Add sec-card--left class to sec-card g1/g2/g3 with the alignment inline style."""
    count = 0
    SEC_STYLE = 'style="align-items:flex-start;text-align:left;padding:26px 20px"'

    # Handle: class="sec-card g1" style="..." → class="sec-card sec-card--left g1"
    def replace_sec_card(m):
        nonlocal count
        gx = m.group(1)  # e.g. "g1"
        count += 1
        return 'class="sec-card sec-card--left ' + gx + '"'

    # Match both quoted and unquoted gN variants
    content = re.sub(
        r'class="sec-card (g\d)"\s+' + re.escape(SEC_STYLE),
        replace_sec_card,
        content
    )
    return content, count


def fix_flip_front_title(content):
    """Remove margin-bottom:5px inline style from .flip-front-title (already in CSS)."""
    count = 0
    old = '<div class="flip-front-title" style="margin-bottom: 5px;">'
    new = '<div class="flip-front-title">'

    while old in content:
        content = content.replace(old, new)
        count += 1

    return content, count


def fix_slide_bg_dark(content):
    """Remove radial-gradient inline style from .slide-bg-dark (moved to CSS class)."""
    count = 0
    BG_STYLE = 'style="background:radial-gradient(circle at right center,rgba(30,40,60,1) 0%,var(--bg) 100%)"'

    # Handle class="slide-bg-dark" style="..." (double-quoted class)
    old_dq = '<div class="slide-bg-dark" ' + BG_STYLE + '>'
    new_dq = '<div class="slide-bg-dark">'
    while old_dq in content:
        content = content.replace(old_dq, new_dq)
        count += 1

    # Handle class=slide-bg-dark style="..." (unquoted class)
    old_uq = '<div class=slide-bg-dark ' + BG_STYLE + '>'
    new_uq = '<div class=slide-bg-dark>'
    while old_uq in content:
        content = content.replace(old_uq, new_uq)
        count += 1

    return content, count


def fix_sc_desc(content):
    """Remove display:flex flex layout inline style from .sc-desc (moved to CSS)."""
    count = 0
    # The font-size:22px is already in .sc-desc CSS; only the flex layout is new
    SC_STYLE = 'style="display:flex;flex-direction:column;gap:12px;font-size:22px"'

    old_dq = '<div class="sc-desc" ' + SC_STYLE + '>'
    new_dq = '<div class="sc-desc">'
    while old_dq in content:
        content = content.replace(old_dq, new_dq)
        count += 1

    old_uq = '<div class=sc-desc ' + SC_STYLE + '>'
    new_uq = '<div class=sc-desc>'
    while old_uq in content:
        content = content.replace(old_uq, new_uq)
        count += 1

    return content, count


def fix_stat_cards(content):
    """Add named classes to the anonymous stat cards in condicoes.htm CTA slide."""
    count = 0

    STAT_GRID_OLD = 'style="display:grid; grid-template-columns: repeat(2, 1fr); gap: 24px; max-width: 1000px; width: 100%;">'
    STAT_GRID_NEW = 'class="stat-grid">'
    if STAT_GRID_OLD in content:
        content = content.replace(STAT_GRID_OLD, STAT_GRID_NEW)
        count += 1

    CARD_OLD = ('style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); '
                'border-radius: 12px; padding: 40px; text-align: center; display: flex; '
                'flex-direction: column; justify-content: center; min-height: 180px;">')
    CARD_NEW = 'class="stat-card">'
    while CARD_OLD in content:
        content = content.replace(CARD_OLD, CARD_NEW)
        count += 1

    LABEL_OLD = ('style="font-size:22px; color:rgba(255,255,255,0.6); text-transform:uppercase; '
                 "letter-spacing:2px; margin-bottom:15px; font-family:'Oswald',sans-serif;\">")
    LABEL_NEW = 'class="stat-label">'
    while LABEL_OLD in content:
        content = content.replace(LABEL_OLD, LABEL_NEW)
        count += 1

    VALUE_OLD = 'style="font-size:42px; color:var(--white); font-weight:bold; letter-spacing:1px; line-height: 1;">'
    VALUE_NEW = 'class="stat-value">'
    while VALUE_OLD in content:
        content = content.replace(VALUE_OLD, VALUE_NEW)
        count += 1

    UNIT_OLD = 'style="font-size:24px; color:rgba(255,255,255,0.6);">'
    UNIT_NEW = 'class="stat-unit">'
    while UNIT_OLD in content:
        content = content.replace(UNIT_OLD, UNIT_NEW)
        count += 1

    NOTE_OLD = 'style="font-size:22px; color:rgba(255,255,255,0.8); margin-top:15px; font-weight: 300;">'
    NOTE_NEW = 'class="stat-note">'
    while NOTE_OLD in content:
        content = content.replace(NOTE_OLD, NOTE_NEW)
        count += 1

    return content, count


# ---------------------------------------------------------------------------
# Main per-file function
# ---------------------------------------------------------------------------

def process_file(filepath):
    is_condicoes = os.path.basename(filepath) == "condicoes.htm"

    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    if SENTINEL in content:
        print("[SKIP] " + os.path.basename(filepath) + " (already processed)")
        return False

    changes = []

    content, n = fix_logo_images(content)
    if n: changes.append("logo-img x" + str(n))

    content, n = fix_deco_figure(content)
    if n: changes.append("deco-figure x" + str(n))

    content, n = fix_sec_card_left(content)
    if n: changes.append("sec-card--left x" + str(n))

    content, n = fix_flip_front_title(content)
    if n: changes.append("flip-front-title margin x" + str(n))

    content, n = fix_slide_bg_dark(content)
    if n: changes.append("slide-bg-dark bg x" + str(n))

    content, n = fix_sc_desc(content)
    if n: changes.append("sc-desc flex x" + str(n))

    if is_condicoes:
        content, n = fix_stat_cards(content)
        if n: changes.append("stat-cards x" + str(n))

    # Inject CSS (always — sentinel check at top guards against double-run)
    content = inject_css(content, is_condicoes)

    with open(filepath, "w", encoding="utf-8", errors="ignore") as f:
        f.write(content)

    if changes:
        print("[OK]   " + os.path.basename(filepath))
        for c in changes:
            print("       + " + c)
    else:
        print("[CSS]  " + os.path.basename(filepath) + " (CSS injected, HTML already updated)")
    return True


def verify(filepath):
    """Report remaining inline styles (excluding SingleFile artifacts)."""
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # Skip known unremovable patterns
    skip_patterns = [
        "background-blend-mode:normal!important",
        "background-clip:content-box!important",
        "mix-blend-mode:luminosity",
        "plasmo",
        "left:1458px",      # cursor position from SingleFile
        "z-index:2147483647",
        "display:none",
        "display:flex;position:absolute;top:0px",
        "yd-sidebar",
        "wxt-shadow",
    ]

    all_styles = re.findall(r'style=["\']([^"\']+)["\']', content)
    remaining = []
    for s in all_styles:
        if not any(p in s for p in skip_patterns):
            remaining.append(s[:80])

    return remaining


def main():
    htm_files = sorted(glob.glob(os.path.join(BASE_DIR, "*.htm")))
    if not htm_files:
        print("No .htm files found.")
        return

    print("=== Removing inline styles from " + str(len(htm_files)) + " file(s) ===\n")
    updated = 0
    for fp in htm_files:
        if process_file(fp):
            updated += 1

    print("\n=== Verification — remaining inline styles (excl. SingleFile artifacts) ===\n")
    for fp in htm_files:
        remaining = verify(fp)
        name = os.path.basename(fp)
        print("[" + str(len(remaining)) + " remaining] " + name)
        for s in remaining[:8]:
            print("  - " + s)
        if len(remaining) > 8:
            print("  ... and " + str(len(remaining) - 8) + " more")
        print()

    print("Done: " + str(updated) + "/" + str(len(htm_files)) + " file(s) updated.")


if __name__ == "__main__":
    main()
