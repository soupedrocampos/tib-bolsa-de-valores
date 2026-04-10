import os
import re

# Base64 generated from LOGO.png
with open('logo_b64.txt', 'r') as f:
    logo_base64 = f.read().strip()

logo_img_tag = f'<div class="logo"><img src="data:image/png;base64,{logo_base64}" style="height: 50px; width: auto; display: block;"></div>'

# List of slides from index.html
slides = [
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

def update_logo(content):
    # Regex to catch variations of the logo div
    pattern = r'<div\s+class=["\']?logo["\']?>.*?TIB\s*<b>\s*(?:\||/)\s*TREE\s*</b>.*?</div>'
    new_content = re.sub(pattern, logo_img_tag, content, flags=re.IGNORECASE | re.DOTALL)
    # Also catch simple version
    pattern2 = r'<div\s+class=["\']?logo["\']?>TIB\s*\|?\s*TREE</div>'
    new_content = re.sub(pattern2, logo_img_tag, new_content, flags=re.IGNORECASE)
    return new_content

for slide in slides:
    if not os.path.exists(slide):
        print(f"Skipping {slide} - not found")
        continue
    
    with open(slide, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # 1. Update logo globally
    new_content = update_logo(content)
    
    # 2. Specific changes for Slide 10 (Pablo Spyer)
    if slide == "8ca20ea5-73c0-45e7-bbc7-9318fcf90089.htm":
        print(f"Applying specific Pablo Spyer changes to {slide}")
        
        # Make Pablo Spyer single line and bigger
        # Look for PABLO<br>SPYER or PABLO<br/>SPYER
        new_content = re.sub(r'PABLO\s*<br/?>\s*SPYER', 'PABLO SPYER', new_content, flags=re.IGNORECASE)
        
        # Inject CSS to raise the text and make it bigger
        pablo_style = """
<style>
/* Adjust Pablo Spyer name */
.partner-name {
    font-size: 85px !important; /* Larger name */
    white-space: nowrap !important;
    line-height: 1 !important;
}
/* Raise the entire content box */
.pablo-content, .partner-box, .slide-body > .container {
    transform: translateY(-80px) !important; /* Subir o texto */
}
/* Adjust spacing for the smaller badge if it exists */
.pablo-badge {
    margin-bottom: 20px !important;
}
</style>
"""
        # Inject before </body> if present, or at the end
        if '</body>' in new_content:
            new_content = new_content.replace('</body>', pablo_style + '</body>')
        else:
            new_content += pablo_style

    with open(slide, 'w', encoding='utf-8', errors='ignore') as f:
        f.write(new_content)
    print(f"Updated {slide}")

print("All tasks completed.")
