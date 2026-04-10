import re
text = open('a23cc662-dd07-4e88-ad78-4390fb4159b5.htm', 'r', encoding='utf-8').read()

with open('tmp_slide4_matches.txt', 'w', encoding='utf-8') as f:
    for w in ['Construtoras', 'Corretores', 'Investidores']:
        matches = re.finditer(w, text, re.IGNORECASE)
        for m in matches:
            context = text[m.start()-50:m.end()+50].replace('\n', ' ')
            f.write(f'{w} at {m.start()}: {context}\n')
