import re
with open(r"c:\Users\pacc1\Downloads\PATRICK\tib site\467f4cfd-096f-43c8-ae7f-ff5c63804069.htm", 'r', encoding='utf-8') as f:
    text = f.read()

res = re.findall(r'.{0,30}0[1-9]\s*/\s*0[6-9].{0,30}', text)
for r in res:
    print(r)
