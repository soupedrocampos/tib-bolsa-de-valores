import re, glob

for f in sorted(glob.glob('*.htm')):
    content = open(f, encoding='utf-8', errors='ignore').read()
    matches = re.findall(r'font-size\s*:\s*(\d+(?:\.\d+)?px)', content, re.IGNORECASE)
    sizes = sorted(set(matches), key=lambda x: float(x.replace('px','')))
    small = [s for s in sizes if float(s.replace('px','')) < 20]
    if small:
        print('ATENCAO ' + f + ': ainda tem tamanhos pequenos: ' + str(small))
    else:
        print('OK ' + f + ': tamanhos px=' + str(sizes))
