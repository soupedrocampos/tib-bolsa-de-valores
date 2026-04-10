import re
filepath = r"c:\Users\pacc1\Downloads\PATRICK\tib site\6889c58f-5abe-4a7a-b7fd-0d9856245d74.htm"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('class="person-layer fade-right"')
if idx != -1:
    snippet = content[max(0, idx-200):idx+1000]
    with open('snippet.txt', 'w', encoding='utf-8') as out:
        out.write(snippet)
else:
    with open('snippet.txt', 'w', encoding='utf-8') as out:
        out.write('Not found')
