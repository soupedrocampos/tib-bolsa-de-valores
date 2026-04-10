import re

with open("c:\\Users\\pacc1\\Downloads\\PATRICK\\tib site\\slide_text.txt", "r", encoding="utf-8") as f:
    text = f.read()

def replacer(match):
    prefix = match.group(1) # e.g. "02"
    return f"{prefix} / 10"

new_text = re.sub(r'(0[1-9])\s*/\s*0[679]', replacer, text)

# Now, we also need to handle the specific slide number shift for slides 8 and 9
# For file 8 (the old 8, now 9): the prefix "08" needs to become "09"
# For file 9 (the old 9, now 10): the prefix "09" needs to become "10"

print("Matches found:")
for m in re.finditer(r'(0[1-9])\s*/\s*0[679]', text):
    print(m.group(0))

print("\nAfter replacement snippet:")
for x in new_text.split('\n'):
    if '/ 10' in x:
        print(x)
