import re

with open('a23cc662-dd07-4e88-ad78-4390fb4159b5.htm', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

idx = content.find('O MOVIMENTO')
nearby = content[max(0,idx-500):idx+4000]

# Remove base64 data
nearby_clean = re.sub(r'data:image/[^;]+;base64,[A-Za-z0-9+/=]+', 'BASE64_DATA', nearby)
nearby_clean = re.sub(r'url\("BASE64_DATA"\)', 'url(BASE64)', nearby_clean)

# Write to output file for easy viewing
with open('slide4_structure.txt', 'w', encoding='utf-8') as f:
    f.write(nearby_clean[:6000])
print("Done! Check slide4_structure.txt")

# Also find the paragraph
idx2 = content.find('gastron')
if idx2 > 0:
    para_section = content[max(0,idx2-800):idx2+2000]
    para_clean = re.sub(r'data:image/[^;]+;base64,[A-Za-z0-9+/=]+', 'BASE64_DATA', para_section)
    with open('slide4_para.txt', 'w', encoding='utf-8') as f:
        f.write(para_clean[:3000])
    print("Para section also saved!")
