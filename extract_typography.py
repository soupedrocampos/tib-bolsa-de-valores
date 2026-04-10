import re
import glob
import os
from html.parser import HTMLParser

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.results = []
        self.tag_stack = []
        self.style_stack = []
        self.current_style = {}
        self.in_style = False
        self.skip_tags = {'script', 'style', 'head', 'meta', 'link'}
        self.css_rules = {}
    
    def parse_inline_style(self, style_str):
        props = {}
        if not style_str:
            return props
        for item in style_str.split(';'):
            parts = item.strip().split(':', 1)
            if len(parts) == 2:
                key = parts[0].strip().lower()
                val = parts[1].strip().replace('!important', '').strip()
                props[key] = val
        return props
    
    def get_computed_style(self, styles_list):
        merged = {}
        for s in styles_list:
            merged.update(s)
        return merged
    
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == 'style':
            self.in_style = True
        
        inline_style = self.parse_inline_style(attrs_dict.get('style', ''))
        
        # Look up class-based styles
        cls = attrs_dict.get('class', '')
        class_style = {}
        for c in cls.split():
            if c in self.css_rules:
                class_style.update(self.css_rules[c])
        
        merged = {}
        merged.update(class_style)
        merged.update(inline_style)
        
        self.tag_stack.append(tag)
        self.style_stack.append(merged)
    
    def handle_endtag(self, tag):
        if tag == 'style':
            self.in_style = False
        if self.tag_stack:
            self.tag_stack.pop()
        if self.style_stack:
            self.style_stack.pop()
    
    def handle_data(self, data):
        if self.in_style:
            return
        if self.tag_stack and self.tag_stack[-1] in self.skip_tags:
            return
        
        text = data.strip()
        if not text or len(text) < 2:
            return
        
        computed = self.get_computed_style(self.style_stack)
        font_size = computed.get('font-size', 'herdado')
        font_family = computed.get('font-family', 'herdado')
        font_weight = computed.get('font-weight', '')
        color = computed.get('color', '')
        
        self.results.append({
            'text': text,
            'font-size': font_size,
            'font-family': font_family,
            'font-weight': font_weight,
            'color': color,
        })


def extract_css_text_rules(content):
    """Extract font-related rules from <style> blocks."""
    css_rules = {}
    style_blocks = re.findall(r'<style[^>]*>(.*?)</style>', content, re.DOTALL | re.IGNORECASE)
    for block in style_blocks:
        # Find class: .classname { ... }
        for match in re.finditer(r'\.([\w-]+)\s*\{([^}]*)\}', block):
            cls = match.group(1)
            props_text = match.group(2)
            props = {}
            for item in props_text.split(';'):
                parts = item.strip().split(':', 1)
                if len(parts) == 2:
                    key = parts[0].strip().lower()
                    val = parts[1].strip().replace('!important', '').strip()
                    props[key] = val
            if cls in css_rules:
                css_rules[cls].update(props)
            else:
                css_rules[cls] = props
    return css_rules


def extract_texts_from_file(filepath):
    """Extract text elements with their styling from an HTML file."""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Extract CSS rules first
    css_rules = extract_css_text_rules(content)
    
    results = []
    
    # Use regex to find elements with visible text + their styles
    # Extract font sizes directly from the CSS using a different approach
    # Look for spans and divs with text and explicit font sizes
    
    # First, find all text nodes with surrounding HTML context
    # Simpler approach: find font-size declarations near text
    
    patterns = [
        # divs and spans with inline style
        r'<(?:div|span|p|h[1-6]|a|li)[^>]*style="([^"]*)"[^>]*>([^<]{2,})</(?:div|span|p|h[1-6]|a|li)>',
        # divs and spans with class
        r'<(?:div|span|p|h[1-6])[^>]*class=["\']?([\w\s-]+)["\']?[^>]*>([^<]{3,})</(?:div|span|p|h[1-6])>',
    ]
    
    # Method: extract all visible text snippets with CSS context
    # Find elements that contain text directly (not nested)
    elem_re = re.compile(
        r'<(div|span|p|h[1-6]|a|strong|em|b|i|label)\b([^>]*)>([^<]{2,})</\1>',
        re.IGNORECASE
    )
    
    for m in elem_re.finditer(content):
        tag = m.group(1)
        attrs_raw = m.group(2)
        text = m.group(3).strip()
        
        if not text or len(text) < 2:
            continue
        
        # Parse style
        style_match = re.search(r'style=["\']([^"\']*)["\']', attrs_raw, re.IGNORECASE)
        inline_style = {}
        if style_match:
            for item in style_match.group(1).split(';'):
                parts = item.strip().split(':', 1)
                if len(parts) == 2:
                    k = parts[0].strip().lower()
                    v = parts[1].strip().replace('!important', '').strip()
                    inline_style[k] = v
        
        # Parse class
        cls_match = re.search(r'class=["\']?([^"\'>\s]+)["\']?', attrs_raw, re.IGNORECASE)
        class_style = {}
        if cls_match:
            for c in cls_match.group(1).split():
                if c in css_rules:
                    class_style.update(css_rules[c])
        
        computed = {}
        computed.update(class_style)
        computed.update(inline_style)
        
        font_size = computed.get('font-size', '—')
        font_family = computed.get('font-family', '—')
        font_weight = computed.get('font-weight', '—')
        color = computed.get('color', '—')
        
        # Clean font family (remove quotes)
        font_family = font_family.replace('"', '').replace("'", '')
        
        results.append({
            'text': text[:80],  # limit text for readability
            'tag': tag.upper(),
            'font-size': font_size,
            'font-family': font_family,
            'font-weight': font_weight,
            'color': color,
        })
    
    return results


# Map of filenames to slide names (based on index.html order)
slide_order = [
    ("6889c58f-5abe-4a7a-b7fd-0d9856245d74.htm", "Slide 1"),
    ("d44e90f7-4cba-419a-8fb6-e67b9f1c3244.htm", "Slide 2"),
    ("fed32750-c044-4f3c-85eb-569045ba5cd5.htm", "Slide 3"),
    ("a23cc662-dd07-4e88-ad78-4390fb4159b5.htm", "Slide 4 — Ecossistema"),
    ("decb2a9f-0689-4ab8-be02-57d48b45364d.htm", "Slide 5"),
    ("2595c031-784a-4bcc-926b-40930d15d505.htm", "Slide 6"),
    ("b52cd9d4-d5d6-4bfd-b3c8-3978f01817dc.htm", "Slide 7"),
    ("condicoes.htm", "Slide 8 — Condições"),
    ("467f4cfd-096f-43c8-ae7f-ff5c63804069.htm", "Slide 9"),
    ("8ca20ea5-73c0-45e7-bbc7-9318fcf90089.htm", "Slide 10"),
]

lines = ["# 📋 Tipografia da Apresentação TIB\n"]
lines.append("> Levantamento completo de textos, fontes e tamanhos em todos os 10 slides.\n")
lines.append("---\n")

for filename, slide_name in slide_order:
    if not os.path.exists(filename):
        lines.append(f"\n## {slide_name}\n\n> ⚠️ Arquivo não encontrado: `{filename}`\n")
        continue
    
    lines.append(f"\n## {slide_name}\n")
    lines.append(f"*Arquivo: `{filename}`*\n\n")
    
    items = extract_texts_from_file(filename)
    
    if not items:
        lines.append("> Nenhum texto encontrado.\n")
        continue
    
    # Deduplicate based on text content
    seen = set()
    unique_items = []
    for item in items:
        key = item['text'].strip()
        if key not in seen:
            seen.add(key)
            unique_items.append(item)
    
    lines.append("| Texto | Tag | Tamanho da Fonte | Família da Fonte | Peso | Cor |\n")
    lines.append("|-------|-----|-----------------|-----------------|------|-----|\n")
    
    for item in unique_items:
        text = item['text'].replace('|', '\\|')
        tag = item['tag']
        size = item['font-size']
        family = item['font-family'][:50] if item['font-family'] != '—' else '—'
        weight = item['font-weight']
        color = item['color']
        lines.append(f"| `{text}` | {tag} | {size} | {family} | {weight} | {color} |\n")
    
    lines.append("\n")

output_path = "tipografia_slides.md"
with open(output_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f"Arquivo gerado: {output_path}")
print(f"Total de slides processados: {len(slide_order)}")
