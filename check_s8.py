from bs4 import BeautifulSoup

filepath = r"c:\Users\pacc1\Downloads\PATRICK\tib site\condicoes.htm"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

soup = BeautifulSoup(content, 'html.parser')
s8 = soup.find('div', id='s8')
if s8:
    print(s8.prettify()[:1000])
else:
    print("No s8 found")
