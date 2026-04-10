from bs4 import BeautifulSoup

with open(r"c:\Users\pacc1\Downloads\PATRICK\tib site\condicoes.htm", 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

element = soup.find(string=lambda t: t and '100k' in t)
if element:
    parent = element.parent.parent.parent
    with open("list_structure.txt", "w", encoding="utf-8") as out:
        out.write(str(parent))
