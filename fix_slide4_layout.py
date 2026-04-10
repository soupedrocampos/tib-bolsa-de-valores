import re

target_file = 'a23cc662-dd07-4e88-ad78-4390fb4159b5.htm'

with open(target_file, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# CSS to fix layout
layout_css = """
/* TIB LAYOUT FIX: 2-Column Hero Section */
.eco-text-col {
    display: grid !important;
    grid-template-columns: 1.1fr 0.9fr !important;
    grid-template-areas: 
        "label desc"
        "title desc" !important;
    gap: 0 80px !important;
    align-items: start !important;
    max-width: 1400px !important;
    margin: 0 auto !important;
    padding: 20px 0 !important;
}

.sec-label { 
    grid-area: label !important; 
    margin-bottom: 10px !important;
}

.sec-title { 
    grid-area: title !important; 
    margin-top: 0 !important;
}

.eco-desc { 
    grid-area: desc !important; 
    margin-top: 45px !important; /* Aligns with the title start */
    font-size: 24px !important;
    line-height: 1.6 !important;
    color: rgba(255,255,255,0.9) !important;
}

/* Adjust for smaller screens */
@media (max-width: 1200px) {
    .eco-text-col {
        grid-template-columns: 1fr !important;
        grid-template-areas: "label" "title" "desc" !important;
        gap: 20px !important;
    }
    .eco-desc { margin-top: 0 !important; }
}
"""

# Inject before </style> or at the end of head
if '</style>' in content:
    # Find the last </style> before body to ensure it overrides
    body_idx = content.find('<body')
    last_style_idx = content.rfind('</style>', 0, body_idx)
    if last_style_idx > 0:
        content = content[:last_style_idx] + layout_css + content[last_style_idx:]
        print("CSS injected into existing style block.")
    else:
        content = content.replace('<head>', '<head><style>' + layout_css + '</style>')
        print("CSS injected as new style block in head.")
else:
    content = content.replace('</head>', '<style>' + layout_css + '</style></head>')
    print("CSS injected at end of head.")

with open(target_file, 'w', encoding='utf-8', errors='ignore') as f:
    f.write(content)

print(f"Successfully updated {target_file}")
