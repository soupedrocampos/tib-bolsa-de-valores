import os
import re

target = os.path.abspath(r"..\apresentação TIB\tib_tree_v3.html")
print(f"Modifying {target}")

if not os.path.exists(target):
    print("File not found!")
    exit(1)

with open(target, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

original = content

# Increase the height of the flip-card
# Let's find flip-card or flip-card-front height CSS
# Often it's height: 400px; or similar. Or flex.
# I will append some custom CSS directly before </style> to ensure the boxes are bigger.
custom_css = """
/* CUSTOM OVERRIDES FOR TIB_TREE_V3 */
.flip-card { height: 450px !important; }
.flip-card-inner { height: 100% !important; }
.flip-card-front, .flip-card-back { height: 100% !important; }
.partner-card { height: 100% !important; }

/* In case the flip-front-title wrapper needs adjustment */
.flip-front-title-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}
.number-big {
    font-size: 1.2em; /* little bigger than title */
    margin-bottom: 5px;
    color: #d4af37;
    font-weight: bold;
}
</style>
"""
content = content.replace('</style>', custom_css, 1)

# Add the numbers above Construtoras, Corretores, Investidores
# We will use the number-big class right before the title
content = content.replace(
    '<div class=flip-front-title>Construtoras</div>',
    '<div class="flip-front-title number-big">10</div><div class=flip-front-title>Construtoras</div>'
)
content = content.replace(
    '<div class=flip-front-title>Corretores<br>Diretos</div>',
    '<div class="flip-front-title number-big">150</div><div class=flip-front-title>Corretores<br>Diretos</div>'
)
content = content.replace(
    '<div class=flip-front-title>Investidores<br>Ativos</div>',
    '<div class="flip-front-title number-big">+1M</div><div class=flip-front-title>Investidores<br>Ativos</div>'
)

# Fix partner names and swap
# First swap order
content = content.replace('<div class=partner-name>Peixoto</div>', '<div class=partner-name>TEMP_PEIXOTO</div>')
content = content.replace('<div class=partner-name>DomPierri</div>', '<div class=partner-name style="white-space:nowrap;font-size:0.75em;">Peixoto</div>')
content = content.replace('<div class=partner-name>TEMP_PEIXOTO</div>', '<div class=partner-name style="white-space:nowrap;font-size:0.75em;">Dom Pierre</div>')

# Fix Patrick Piccoli
content = content.replace('<div class=partner-name>Patrick<br>Piccoli</div>', '<div class=partner-name style="white-space:nowrap;font-size:0.70em;">Patrick Piccoli</div>')
# Fix Cristian Nascimento
content = content.replace('<div class=partner-name>Cristian<br>Nascimento</div>', '<div class=partner-name style="white-space:nowrap;font-size:0.56em;">Cristian Nascimento</div>')

# Wait, if `tib_tree_v3.html` uses different quotes or spacing, replace might fail. 
# But usually SingleFile output is consistent.

if content != original:
    with open(target, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully updated tib_tree_v3.html")
else:
    print("No changes were made. Perhaps the strings don't match.")
