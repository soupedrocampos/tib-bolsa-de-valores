import re

files = [
    '2595c031-784a-4bcc-926b-40930d15d505.htm',
    'd44e90f7-4cba-419a-8fb6-e67b9f1c3244.htm',
    '6889c58f-5abe-4a7a-b7fd-0d9856245d74.htm',
    'b52cd9d4-d5d6-4bfd-b3c8-3978f01817dc.htm',
    'decb2a9f-0689-4ab8-be02-57d48b45364d.htm',
    'fed32750-c044-4f3c-85eb-569045ba5cd5.htm',
    '467f4cfd-096f-43c8-ae7f-ff5c63804069.htm',
    '8ca20ea5-73c0-45e7-bbc7-9318fcf90089.htm',
]

for f in files:
    try:
        with open(f, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()
        
        original = content
        
        # Fix partner names - remove all previous inline font-size overrides we added
        # And instead inject a CSS rule that makes partner-name look like THE REAL ESTATE EXPERIENCE
        # "tag" class is the heading style. Let's just set it explicitly via injected CSS.
        
        # Remove old inline styles we added in tmp_update.py:
        content = content.replace(
            '<div class=partner-name style="white-space:nowrap;font-size:0.75em;">Dom Pierre</div>',
            '<div class=partner-name>Dom Pierre</div>'
        )
        content = content.replace(
            '<div class=partner-name style="white-space:nowrap;font-size:0.75em;">Peixoto</div>',
            '<div class=partner-name>Peixoto</div>'
        )
        content = content.replace(
            '<div class=partner-name style="white-space:nowrap;font-size:0.70em;">Patrick Piccoli</div>',
            '<div class=partner-name>Patrick Piccoli</div>'
        )
        content = content.replace(
            '<div class=partner-name style="white-space:nowrap;font-size:0.56em;">Cristian Nascimento</div>',
            '<div class=partner-name>Cristian Nascimento</div>'
        )

        # Now inject CSS right before </style> to style partner-name like .tag
        # Looking at "THE REAL ESTATE EXPERIENCE." - class is "tag"
        partner_css = """
.partner-name {
  font-family: inherit !important;
  font-size: clamp(14px, 1.5vw, 22px) !important;
  font-weight: 700 !important;
  letter-spacing: 0.08em !important;
  color: #FFE566 !important;
  white-space: nowrap !important;
  text-transform: uppercase !important;
}
"""
        # Inject before the closing style tag
        if partner_css not in content:
            content = content.replace('</style>', partner_css + '</style>', 1)
        
        if content != original:
            with open(f, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f'Updated: {f}')
        else:
            print(f'No change: {f}')
    except Exception as e:
        print(f'Error in {f}: {e}')

print('Done.')
