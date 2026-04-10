import re
import glob

html_files = glob.glob('*.htm')

for f in html_files:
    with open(f, 'r', encoding='utf-8') as file:
        text = file.read()
    
    # We want to delete things like <div class=nav-pill>01 / 10</div>
    # or <div class=slide-num id=snum>01 / 10</div>
    # The regex targets a div tag, containing strictly spaces and \d / 10 and spaces
    
    def replacer(match):
        full_tag = match.group(0)
        # Preserve <div class="num-pill"... >
        if 'num-pill' in full_tag:
            return full_tag  # Do not modify
        return '' # Delete
    
    # regex: <div[^>]*>\s*0?\d\s*/\s*10\s*</div>
    new_text = re.sub(r'<div[^>]*>\s*0?\d\s*/\s*10\s*</div>', replacer, text, flags=re.IGNORECASE)
    
    # Also catch spans just in case: <span[^>]*>\s*0?\d\s*/\s*10\s*</span>
    new_text = re.sub(r'<span[^>]*>\s*0?\d\s*/\s*10\s*</span>', replacer, new_text, flags=re.IGNORECASE)
    
    if new_text != text:
        with open(f, 'w', encoding='utf-8') as file:
            file.write(new_text)
        print(f"Fixed numbers in {f}")

print("Done removing stray numbers.")
