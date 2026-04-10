from bs4 import BeautifulSoup
import sys

filepath = sys.argv[1]
with open(filepath, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

with open('slide_text.txt', 'w', encoding='utf-8') as out:
    out.write(soup.get_text(separator='\n', strip=True))
