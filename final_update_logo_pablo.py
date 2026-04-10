import os
import re

# Base64 for the logo (cached from previous step)
with open('logo_b64.txt', 'r') as f:
    logo_b64 = f.read().strip()

logo_html = f'<div class="logo"><img src="data:image/png;base64,{logo_b64}" style="height: 50px; width: auto; display: block;"></div>'

slides = [f for f in os.listdir('.') if f.endswith('.htm')]

for slide in slides:
    with open(slide, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # 1. Replacement of Logo
    # Regex to catch the various ways the logo div might be written
    pattern = r'<div\s+class=["\']?logo["\']?>.*?TIB\s*<b>\s*(?:\||/)\s*TREE\s*</b>.*?</div>'
    new_content = re.sub(pattern, logo_html, content, flags=re.IGNORECASE | re.DOTALL)
    
    # 2. Improvement of Pablo Spyer Slide
    if 'PABLO' in content.upper() and 'SPYER' in content.upper():
        print(f"Applying Pablo fix to {slide}")
        # Ensure name is on a single line
        new_content = re.sub(r'PABLO\s*<br/?>\s*SPYER', 'PABLO SPYER', new_content, flags=re.IGNORECASE)
        
        # Inject styles to increase size and raise components
        pablo_style = """
<style>
/* Pablo Spyer name styling */
.pablo-name, .partner-name, h2:contains("PABLO") {
    font-size: 80px !important;
    white-space: nowrap !important;
    line-height: 1 !important;
    margin-bottom: 20px !important;
    display: block !important;
}
/* Raise the content box */
.partner-box, .pablo-content, .pablo-section {
    transform: translateY(-60px) !important;
    margin-top: -40px !important;
}
</style>
"""
        # Note: :contains is not valid CSS usually, but we can target the class
        # Correcting the style to use only valid selectors or high-impact ones
        pablo_style = """
<style>
.pablo-name, .partner-name, [class*="partner"], [class*="pablo"] {
    /* Target names specifically if they are text */
}
/* High priority Pablo Spyer name enhancement */
.partner-name, .pablo-name {
    font-size: 90px !important;
    white-space: nowrap !important;
    line-height: 1.1 !important;
    text-transform: uppercase !important;
    margin-top: -20px !important;
}
/* Positioning fix to raise text */
.partner-box, .pablo-content {
    margin-top: -80px !important;
}
</style>
"""
        if '</head>' in new_content:
            new_content = new_content.replace('</head>', pablo_style + '</head>')
        else:
            new_content = pablo_style + new_content

    with open(slide, 'w', encoding='utf-8', errors='ignore') as f:
        f.write(new_content)
    print(f"Updated {slide}")

print("Global update and Pablo fix finished.")
