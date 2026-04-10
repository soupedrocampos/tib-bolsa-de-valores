"""
standardize_fonts.py
Two tasks in one pass:

A) INJECT MISSING CSS — 9 UUID files had inline→class replacements applied but
   CSS class definitions never injected (inject_css used </body> which only
   exists in condicoes.htm). This script inserts the missing <style> blocks
   before <yd-sidebar> for the UUID files.

B) TOKENIZE FONT SIZES — Replace literal px font-size values that have exact
   matching design tokens, within the custom slide CSS block only.

   Token map (from design-tokens.css / inject_tokens.py):
     22px / 22.0px → var(--text-md)    (22px)
     28px / 28.0px → var(--text-lg)    (28px)
     34px / 34.0px → var(--text-xl)    (34px)
     48px          → var(--text-2xl)   (48px)
     52px          → var(--text-3xl)   (52px)
   Left as literals (no exact token):
     20px / 20.0px  (between --text-sm:18px and --text-md:22px)
     24px           (between --text-md:22px and --text-lg:28px)
     42px           (between --text-xl:34px and --text-2xl:48px)

Usage: python standardize_fonts.py
"""

import os
import glob

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SENTINEL = "--tib-fonts-standardized:1;"

# ---------------------------------------------------------------------------
# CSS to inject for non-condicoes slides (Round 1 classes)
# ---------------------------------------------------------------------------
R1_CSS = """\
<style>
  /* --- TIB: inline styles moved to classes (--tib-inline-refactored:1;) --- */
  --tib-inline-refactored:1;;
  /* Logo images (partner boxes) */
  .logo-img{height:50px;width:auto;display:block}
  /* Decorative hero figure */
  .deco-figure{position:absolute;right:5%;bottom:0;height:85%;width:auto;object-fit:contain;z-index:1;pointer-events:none;filter:drop-shadow(0 0 30px rgba(0,0,0,.8))}
  /* Sec-card left-aligned variant */
  .sec-card--left{align-items:flex-start;text-align:left;padding:26px 20px}
  /* Flip card title spacing */
  .flip-front-title{margin-bottom:5px}
  /* Dark radial slide background */
  .slide-bg-dark{background:radial-gradient(circle at right center,rgba(30,40,60,1) 0%,var(--bg) 100%)}
  /* Section description flex layout */
  .sc-desc{display:flex;flex-direction:column;gap:var(--sp-3)}
</style>
"""

# ---------------------------------------------------------------------------
# CSS to inject for all slides (Round 2 classes) — font-size tokens applied
# ---------------------------------------------------------------------------
R2_CSS = """\
<style>
  /* --- TIB: round-2 inline-to-class refactor --- */
  --tib-inline-r2:1;
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
  /* pull-quote (gold left-border tagline) — font-size tokenized to var(--text-lg) */
  .pull-quote{font-family:var(--font-display);font-size:var(--text-lg);color:rgba(255,255,255,.9);letter-spacing:2px;padding-left:var(--sp-6);border-left:4px solid var(--gold)}
  /* sc-title font-size variants (class base is 24px) */
  .sc-title--sm{font-size:20px;margin-bottom:20px}
  .sc-title--md{font-size:var(--text-md);margin-bottom:20px}
  /* partner-name small variant */
  .partner-name--sm{font-size:0.63em}
</style>
"""

# ---------------------------------------------------------------------------
# Token substitution map: literal px → CSS variable
# ---------------------------------------------------------------------------
TOKEN_MAP = [
    ("font-size:52px",    "font-size:var(--text-3xl)"),  # 52px = --text-3xl
    ("font-size:48px",    "font-size:var(--text-2xl)"),  # 48px = --text-2xl
    ("font-size:34.0px",  "font-size:var(--text-xl)"),   # 34px = --text-xl
    ("font-size:34px",    "font-size:var(--text-xl)"),
    ("font-size:28.0px",  "font-size:var(--text-lg)"),   # 28px = --text-lg
    ("font-size:28px",    "font-size:var(--text-lg)"),
    ("font-size:22.0px",  "font-size:var(--text-md)"),   # 22px = --text-md
    ("font-size:22px",    "font-size:var(--text-md)"),
]


def find_custom_css_bounds(content):
    """Return (start, end) of the custom TIB CSS <style>...</style> block.

    Identified by the :root{--gold token. Bounded on the right by the
    SweetAlert CSS which begins with 'div:where(.swal2-container)'.
    """
    marker = ":root{--gold:#D9B855"
    root_pos = content.find(marker)
    if root_pos == -1:
        return None, None

    # <style> tag immediately before the :root block
    style_open = content.rfind("<style>", 0, root_pos)
    if style_open == -1:
        style_open = content.rfind("<style ", 0, root_pos)
    if style_open == -1:
        return None, None

    # </style> immediately before the SweetAlert block
    swal_anchor = "div:where(.swal2-container)"
    swal_pos = content.find(swal_anchor)
    if swal_pos == -1:
        # condicoes.htm might not have SweetAlert — fall back
        style_close = content.find("</style>", root_pos)
    else:
        style_close = content.rfind("</style>", 0, swal_pos)

    if style_close == -1:
        return None, None

    return style_open, style_close + len("</style>")


def tokenize_block(block):
    """Apply TOKEN_MAP replacements inside a CSS block string."""
    changes = []
    for old, new in TOKEN_MAP:
        count = block.count(old)
        if count:
            block = block.replace(old, new)
            changes.append(f"{old} -> {new.split(':')[1]} x{count}")
    return block, changes


def process_file(filepath):
    name = os.path.basename(filepath)
    is_condicoes = name == "condicoes.htm"

    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    if SENTINEL in content:
        print(f"[SKIP] {name} (already processed)")
        return False

    changes = []

    # ------------------------------------------------------------------
    # Task A: inject missing CSS for UUID files
    # ------------------------------------------------------------------
    if not is_condicoes:
        has_r1 = "--tib-inline-refactored:1;" in content
        has_r2 = "--tib-inline-r2:1;" in content

        if not has_r1:
            if "<yd-sidebar>" in content:
                content = content.replace("<yd-sidebar>", R1_CSS + "<yd-sidebar>", 1)
                changes.append("injected R1 CSS (logo-img, deco-figure, etc.)")
            else:
                # append before end of file
                content = content + "\n" + R1_CSS
                changes.append("injected R1 CSS (appended)")

        if not has_r2:
            if "<yd-sidebar>" in content:
                content = content.replace("<yd-sidebar>", R2_CSS + "<yd-sidebar>", 1)
                changes.append("injected R2 CSS (cl-metrics, pull-quote, etc.)")
            else:
                content = content + "\n" + R2_CSS
                changes.append("injected R2 CSS (appended)")

    # ------------------------------------------------------------------
    # Task B: tokenize font-size in the custom CSS block
    # ------------------------------------------------------------------
    start, end = find_custom_css_bounds(content)
    if start is not None:
        original_block = content[start:end]
        new_block, tok_changes = tokenize_block(original_block)
        if tok_changes:
            content = content[:start] + new_block + content[end:]
            changes.extend(tok_changes)
    else:
        print(f"  [WARN] {name}: custom CSS block not found")

    # Also tokenize within our injected blocks (R1/R2) if they're present
    # The injected blocks are right before <yd-sidebar> or </body>
    # Just apply tokenization globally to the injected block content
    # (safe because the literals only appear in our CSS, not base64/SingleFile)
    #
    # For condicoes.htm: tokenize the existing injected block's font-size:28px
    if is_condicoes:
        # Only within content AFTER the custom CSS block (to avoid touching it twice)
        after_custom = content[end:] if end else content
        new_after, tok_changes2 = tokenize_block(after_custom)
        if tok_changes2:
            content = content[:end] + new_after
            changes.extend([c + " [injected]" for c in tok_changes2])

    # Stamp the sentinel in a new <style> before <yd-sidebar> or </body>
    sentinel_css = f"<style>/* TIB: font sizes tokenized */\n  {SENTINEL}\n</style>\n"
    if "<yd-sidebar>" in content:
        content = content.replace("<yd-sidebar>", sentinel_css + "<yd-sidebar>", 1)
    elif "</body>" in content:
        content = content.replace("</body>", sentinel_css + "</body>", 1)
    else:
        content = content + "\n" + sentinel_css

    with open(filepath, "w", encoding="utf-8", errors="ignore") as f:
        f.write(content)

    if changes:
        print(f"[OK]   {name}")
        for c in changes:
            print(f"       + {c}")
    else:
        print(f"[CSS]  {name} (sentinel only, no other changes)")
    return True


def verify(filepath):
    """Report remaining literal px font-size values in custom+injected CSS."""
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    start, end = find_custom_css_bounds(content)
    if start is None:
        return []

    # Check ONLY the custom CSS block (SweetAlert/preview-UI/extension blocks
    # come after and have their own font-size:22px values we must not touch)
    check_zone = content[start:end]
    found = []
    for px in ["font-size:22px", "font-size:22.0px", "font-size:52px",
               "font-size:28px", "font-size:28.0px", "font-size:34px",
               "font-size:34.0px", "font-size:48px"]:
        n = check_zone.count(px)
        if n:
            found.append(f"{px} x{n}")
    return found


def main():
    htm_files = sorted(glob.glob(os.path.join(BASE_DIR, "*.htm")))
    if not htm_files:
        print("No .htm files found.")
        return

    print(f"=== Processing {len(htm_files)} file(s) ===\n")
    updated = 0
    for fp in htm_files:
        if process_file(fp):
            updated += 1

    print(f"\n=== Verification — remaining tokenizable font-sizes ===\n")
    for fp in htm_files:
        remaining = verify(fp)
        name = os.path.basename(fp)
        status = "CLEAN" if not remaining else "REMAINING"
        print(f"[{status}] {name}")
        for r in remaining:
            print(f"  - {r}")

    print(f"\nDone: {updated}/{len(htm_files)} file(s) updated.")


if __name__ == "__main__":
    main()
