from bs4 import BeautifulSoup
filepath = r"c:\Users\pacc1\Downloads\PATRICK\tib site\condicoes.htm"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

soup = BeautifulSoup(content, 'html.parser')
slides = soup.find_all('div', class_='slide')
for s in slides:
    if 'Posicionamento Final' in s.text:
        print(f"Found in slide id: {s.get('id')}")
