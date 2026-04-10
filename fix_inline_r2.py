"""
fix_inline_r2.py
Round-2 inline style cleanup for TIB slides.

Handles single-quoted and unquoted style attributes missed in round 1,
and fixes the .partner-name !important conflict in style block 1.

New classes created:
  .cl-metrics      layout for the metrics/bullet list container
  .cl-intro        subheading inside cl-metrics ("Se voce e uma construtora...")
  .cl-item         list item inside cl-metrics
  .g--block        gold text span with display:inline-block;margin-top:10px
  .cl-h--sm        cl-h with smaller fluid font (clamp 32-64px)
  .mb-0            margin-bottom:0 utility
  .mb-20           margin-bottom:20px utility
  .mb-50           margin-bottom:50px utility
  .pt-30           padding-top:30px utility
  .pt-60           padding-top:60px utility
  .pt-100          padding-top:100px utility
  .body-text       paragraph with white-60, 1.8 line-height (pablo description)
  .pull-quote      gold left-border tagline div
  .sc-title--sm    sc-title at 20px (UUID slides override)
  .sc-title--md    sc-title at 22px (condicoes override)
  .partner-name--sm partner name at 0.63em (smaller variant)

Also patches style block 1 to remove !important overrides on .partner-name.

Usage: python fix_inline_r2.py
"""

import os
import re
import glob

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SENTINEL = "--tib-inline-r2:1;"

# New CSS block injected via <style> before </body>
NEW_CSS = """
  /* --- TIB: round-2 inline-to-class refactor --- */
  %s
  /* cl-metrics (bullet list container) */
  .cl-metrics{display:flex;flex-direction:column;gap:var(--sp-4);align-items:center;margin:0 0 50px;font-family:var(--font-display);text-transform:uppercase}
  /* cl-metrics children */
  .cl-intro{font-size:var(--text-md);letter-spacing:1px;color:var(--white-60);margin-bottom:10px}
  .cl-item{font-size:20px;color:var(--white);letter-spacing:2px}
  /* span.g inline-block variant */
  .g--block{display:inline-block;margin-top:10px}
  /* cl-h small fluid variant */
  .cl-h--sm{font-size:clamp(32px,5vw,64px);line-height:1;margin-bottom:0}
  /* spacing utilities */
  .mb-0{margin-bottom:0}
  .mb-20{margin-bottom:var(--sp-5)}
  .mb-50{margin-bottom:50px}
  .pt-30{padding-top:30px}
  .pt-60{padding-top:var(--sp-16)}
  .pt-100{padding-top:100px}
  /* body text paragraph */
  .body-text{font-size:var(--text-md);line-height:1.8;color:var(--white-60);margin-bottom:30px;max-width:480px}
  /* pull-quote (gold left-border tagline) */
  .pull-quote{font-family:var(--font-display);font-size:28px;color:rgba(255,255,255,.9);letter-spacing:2px;padding-left:var(--sp-6);border-left:4px solid var(--gold)}
  /* sc-title font-size variants (class base is 24px) */
  .sc-title--sm{font-size:20px;margin-bottom:20px}
  .sc-title--md{font-size:var(--text-md);margin-bottom:20px}
  /* partner-name small variant */
  .partner-name--sm{font-size:0.63em}
"""


def inject_css(content):
    block = NEW_CSS % SENTINEL
    new_style = "<style>" + block + "</style>\n"
    return content.replace("</body>", new_style + "</body>", 1)


# ---------------------------------------------------------------------------
# A — Single-quoted and unquoted style fixers
# ---------------------------------------------------------------------------

def fix_cl_metrics(content):
    """Remove single-quoted style from .cl-metrics."""
    count = 0
    # The full single-quoted style value (may vary slightly — match core portion)
    old = (
        "<div class=cl-metrics style='flex-direction:column;gap:16px;align-items:center;"
        "margin:0 0 50px;font-family:\"Oswald\",sans-serif;text-transform:uppercase'>"
    )
    new = "<div class=cl-metrics>"
    if old in content:
        content = content.replace(old, new)
        count = 1
    return content, count


def fix_cl_intro(content):
    """Replace anonymous cl-intro div (font-size:22.0px subheading)."""
    count = 0
    old = "<div style=font-size:22.0px;letter-spacing:1px;color:rgba(255,255,255,.6);margin-bottom:10px>"
    new = "<div class=cl-intro>"
    while old in content:
        content = content.replace(old, new)
        count += 1
    return content, count


def fix_cl_items(content):
    """Replace anonymous cl-item divs (font-size:20.0px list items)."""
    count = 0
    old = "<div style=font-size:20.0px;color:var(--white);letter-spacing:2px>"
    new = "<div class=cl-item>"
    while old in content:
        content = content.replace(old, new)
        count += 1
    return content, count


def fix_gold_spans(content):
    """Replace <span style=color:var(--gold)> with <span class=g>."""
    count = 0
    old = "<span style=color:var(--gold)>"
    new = "<span class=g>"
    while old in content:
        content = content.replace(old, new)
        count += 1
    return content, count


def fix_g_block(content):
    """Replace class=g style=display:inline-block;margin-top:10px with class='g g--block'."""
    count = 0
    old = '<span class=g style=display:inline-block;margin-top:10px>'
    new = '<span class="g g--block">'
    while old in content:
        content = content.replace(old, new)
        count += 1
    return content, count


def fix_sc_desc_unquoted(content):
    """Remove unquoted style from class=sc-desc (CSS already handles it after r1)."""
    count = 0
    old = "class=sc-desc style=display:flex;flex-direction:column;gap:12px;font-size:22px>"
    new = "class=sc-desc>"
    while old in content:
        content = content.replace(old, new)
        count += 1
    return content, count


def fix_sc_title_unquoted(content):
    """Replace unquoted sc-title style with modifier class."""
    count = 0
    old = "class=sc-title style=font-size:20.0px;margin-bottom:20px>"
    new = 'class="sc-title sc-title--sm">'
    while old in content:
        content = content.replace(old, new)
        count += 1
    return content, count


def fix_sc_title_condicoes(content):
    """Fix condicoes.htm sc-title double-quoted style."""
    count = 0
    old = 'class="sc-title" style="font-size:22px;margin-bottom:20px">'
    new = 'class="sc-title sc-title--md">'
    while old in content:
        content = content.replace(old, new)
        count += 1
    return content, count


def fix_cl_h_sm(content):
    """Replace cl-h with fluid-small inline style with modifier class."""
    count = 0
    old = "class=cl-h style=font-size:clamp(32px,5vw,64px);line-height:1;margin-bottom:0>"
    new = 'class="cl-h cl-h--sm">'
    while old in content:
        content = content.replace(old, new)
        count += 1
    return content, count


def fix_sec_title_margins(content):
    """Add mb-* utility classes to sec-title with margin overrides."""
    count = 0
    for (old, new) in [
        ("class=sec-title style=margin-bottom:0>",      'class="sec-title mb-0">'),
        ("class=sec-title style=margin-bottom:20px>",   'class="sec-title mb-20">'),
        ("class=sec-title style=margin-bottom:50px>",   'class="sec-title mb-50">'),
        ('class="sec-title" style="margin-bottom:0">',      'class="sec-title mb-0">'),
        ('class="sec-title" style="margin-bottom:20px">', 'class="sec-title mb-20">'),
        ('class="sec-title" style="margin-bottom:50px">', 'class="sec-title mb-50">'),
    ]:
        while old in content:
            content = content.replace(old, new)
            count += 1
    return content, count


def fix_slide_body_padding(content):
    """Add pt-* utility classes to slide-body/close-body with padding overrides."""
    count = 0
    for (old, new) in [
        ("class=slide-body style=padding-top:100px>",   'class="slide-body pt-100">'),
        ("class=slide-body style=padding-top:60px>",    'class="slide-body pt-60">'),
        ("class=close-body style=padding-top:30px>",    'class="close-body pt-30">'),
        ('class="slide-body" style="padding-top:100px">',  'class="slide-body pt-100">'),
        ('class="slide-body" style="padding-top:60px">',   'class="slide-body pt-60">'),
        ('class="close-body" style="padding-top:30px">',   'class="close-body pt-30">'),
    ]:
        while old in content:
            content = content.replace(old, new)
            count += 1
    return content, count


def fix_sec_label_margin(content):
    """Add mb-20 to sec-label with margin override."""
    count = 0
    for (old, new) in [
        ("class=sec-label style=margin-bottom:20px>",   'class="sec-label mb-20">'),
        ('class="sec-label" style="margin-bottom:20px">', 'class="sec-label mb-20">'),
        ('class="sec-label" style="margin-bottom:10px;">', 'class="sec-label mb-10">'),
    ]:
        while old in content:
            content = content.replace(old, new)
            count += 1
    return content, count


def fix_body_text(content):
    """Replace anonymous body-text paragraph with .body-text class."""
    count = 0
    old = "<p style=font-size:22px;line-height:1.8;color:var(--white-60);margin-bottom:30px;max-width:480px>"
    new = "<p class=body-text>"
    while old in content:
        content = content.replace(old, new)
        count += 1
    # Also double-quoted version in condicoes.htm
    old2 = '<p style="font-size:22px;line-height:1.8;color:var(--white-60);margin-bottom:30px;max-width:480px">'
    while old2 in content:
        content = content.replace(old2, new)
        count += 1
    return content, count


def fix_pull_quote(content):
    """Replace anonymous pull-quote div with .pull-quote class."""
    count = 0
    old = '<div style=\'font-family:"Oswald",sans-serif;font-size:28.0px;color:rgba(255,255,255,0.9);letter-spacing:2px;padding-left:24px;border-left:4px solid var(--gold)\'>'
    new = "<div class=pull-quote>"
    if old in content:
        content = content.replace(old, new)
        count = 1
    return content, count


def fix_second_sq_style(content):
    """Handle the second single-quoted style (font-family:Oswald heading variant)."""
    count = 0
    # Try to match the pattern with regex for safety (single-quoted)
    m = re.search(
        r"style='font-family:\"Oswald\",sans-serif;font-size:28\.0px;color:rgba\(255,255,255,0\.9\);letter-spacing:2px;padding-left:24px;border-left:4px solid var\(--gold\)'",
        content
    )
    if m:
        content = content[:m.start()] + "class=pull-quote" + content[m.end():]
        count = 1
    return content, count


# ---------------------------------------------------------------------------
# B — Fix partner-name !important in style block 1
# ---------------------------------------------------------------------------

PARTNER_OLD = """.pablo-name, .partner-name, [class*="partner"], [class*="pablo"] {
    /* Target names specifically if they are text */
}
/* High priority Pablo Spyer name enhancement */
.partner-name, .pablo-name {
    font-size: 90px !important;
    white-space: nowrap !important;
    line-height: 1.1 !important;
    text-transform: uppercase !important;
    margin-top: -20px !important;
}
/* Positioning fix to raise text */
.partner-box, .pablo-content {
    margin-top: -80px !important;
}"""

PARTNER_NEW = """/* partner-name — corrected from debug overrides */
.partner-name, .pablo-name {
    font-size: 0.75em;
    white-space: nowrap;
    line-height: 1.1;
    text-transform: uppercase;
    margin-top: -20px;
}
.partner-box, .pablo-content {
    margin-top: -80px;
}"""


def fix_partner_name_css(content):
    """Fix the !important overrides in style block 1."""
    if PARTNER_OLD in content:
        content = content.replace(PARTNER_OLD, PARTNER_NEW)
        return content, 1
    return content, 0


def fix_partner_name_inline(content):
    """Remove inline style from .partner-name (0.75em — now handled by CSS)."""
    count = 0
    for (old, new) in [
        ('<div class="partner-name" style="white-space:nowrap;font-size:0.75em;">',
         '<div class="partner-name">'),
        ('<div class="partner-name" style="white-space:nowrap;font-size:0.63em;">',
         '<div class="partner-name partner-name--sm">'),
    ]:
        while old in content:
            content = content.replace(old, new)
            count += 1
    return content, count


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------

def process_file(filepath):
    is_condicoes = os.path.basename(filepath) == "condicoes.htm"

    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    if SENTINEL in content:
        print("[SKIP] " + os.path.basename(filepath))
        return False

    changes = []

    for fn, label in [
        (fix_cl_metrics,         "cl-metrics SQ"),
        (fix_cl_intro,           "cl-intro"),
        (fix_cl_items,           "cl-items"),
        (fix_gold_spans,         "gold spans"),
        (fix_g_block,            "g--block"),
        (fix_sc_desc_unquoted,   "sc-desc UQ"),
        (fix_sc_title_unquoted,  "sc-title--sm"),
        (fix_cl_h_sm,            "cl-h--sm"),
        (fix_sec_title_margins,  "sec-title margins"),
        (fix_slide_body_padding, "slide-body/close-body padding"),
        (fix_sec_label_margin,   "sec-label margin"),
        (fix_body_text,          "body-text"),
        (fix_pull_quote,         "pull-quote"),
        (fix_partner_name_css,   "partner-name CSS fix"),
        (fix_partner_name_inline,"partner-name inline"),
    ]:
        content, n = fn(content)
        if n:
            changes.append(label + " x" + str(n))

    if is_condicoes:
        content, n = fix_sc_title_condicoes(content)
        if n: changes.append("sc-title--md (condicoes) x" + str(n))

    content = inject_css(content)

    with open(filepath, "w", encoding="utf-8", errors="ignore") as f:
        f.write(content)

    if changes:
        print("[OK]   " + os.path.basename(filepath))
        for c in changes:
            print("       + " + c)
    else:
        print("[CSS]  " + os.path.basename(filepath) + " (CSS injected only)")
    return True


def verify(filepath):
    skip = [
        "background-blend-mode", "background-clip", "mix-blend-mode",
        "plasmo", "z-index:2147483647", "display:none",
        "display:flex;position:absolute;top:0px", "wxt-shadow", "yd-sidebar",
        "left:1458px", "left:943px", "left:946",
        # Remaining intentional per-slide overrides
        "font-size:40.0px", "font-size:38px",   # cl-h overrides
        "font-size:clamp(40px",                  # pablo-name
        "font-size:clamp(36px",                  # sec-title in condicoes
        "padding-left:50px",                     # slide-body unique layout
        "margin-top:15px",                       # stat-note variant
        "opacity: 0.7",                          # particionado span
        "margin-bottom:0",                       # sec-title--flush fallback
        # condicoes specific
        "padding-top:40px",
        "padding-top:100px",                     # close-body variant
        "font-size:52px",                        # gold stat value
        "display:grid",                          # stat-grid fallback
    ]
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    all_styles = re.findall(r"style=[\"'=]([^\"'>\s][^\"'>]*)[\"'>]?", content)
    remaining = []
    for s in all_styles:
        s = s.strip("\"'")
        if not any(p in s for p in skip) and len(s) > 5:
            remaining.append(s[:90])
    return remaining


def main():
    htm_files = sorted(glob.glob(os.path.join(BASE_DIR, "*.htm")))
    if not htm_files:
        print("No .htm files found.")
        return

    print("=== Round-2 inline style cleanup — " + str(len(htm_files)) + " file(s) ===\n")
    for fp in htm_files:
        process_file(fp)

    print("\n=== Remaining inline styles (after both rounds) ===\n")
    for fp in htm_files:
        remaining = verify(fp)
        name = os.path.basename(fp)
        print("[" + str(len(remaining)) + " remaining] " + name)
        for s in remaining[:6]:
            print("  - " + s)
        if len(remaining) > 6:
            print("  ... +" + str(len(remaining) - 6) + " more")
        print()


if __name__ == "__main__":
    main()
