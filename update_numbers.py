import os
import re

files = [
    "6889c58f-5abe-4a7a-b7fd-0d9856245d74.htm",
    "d44e90f7-4cba-419a-8fb6-e67b9f1c3244.htm",
    "fed32750-c044-4f3c-85eb-569045ba5cd5.htm",
    "a23cc662-dd07-4e88-ad78-4390fb4159b5.htm",
    "decb2a9f-0689-4ab8-be02-57d48b45364d.htm",
    "2595c031-784a-4bcc-926b-40930d15d505.htm",
    "b52cd9d4-d5d6-4bfd-b3c8-3978f01817dc.htm",
    "condicoes.htm",
    "467f4cfd-096f-43c8-ae7f-ff5c63804069.htm",
    "8ca20ea5-73c0-45e7-bbc7-9318fcf90089.htm"
]

base_dir = r"c:\Users\pacc1\Downloads\PATRICK\tib site"

for filename in files:
    filepath = os.path.join(base_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Clean up all denominators to / 10
    content = re.sub(r'(0[1-9])\s*/\s*0[6-9]', r'\g<1> / 10', content)

    # Shift numbers for slide 9 (467f...)
    if filename == "467f4cfd-096f-43c8-ae7f-ff5c63804069.htm":
        content = content.replace("08 / 10", "09 / 10")
    
    # Shift numbers for slide 10 (8ca2...)
    if filename == "8ca20ea5-73c0-45e7-bbc7-9318fcf90089.htm":
        content = content.replace("09 / 10", "10 / 10")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Processed {filename}")
