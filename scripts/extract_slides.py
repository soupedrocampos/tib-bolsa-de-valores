import fitz
import json

def extract_pdf_content(pdf_path):
    doc = fitz.open(pdf_path)
    slides = []
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text("text")
        
        # Clean text
        raw_lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        # Remove consecutive duplicates which often happen in PDF extractions with layers
        # Or even better: unique lines preserving order
        unique_lines = []
        for line in raw_lines:
            if not unique_lines or line != unique_lines[-1]:
                unique_lines.append(line)
        
        slides.append({
            "slide_index": page_num + 1,
            "content": unique_lines
        })
    
    return slides

if __name__ == "__main__":
    pdf_path = "4. O MELHOR VENDEDOR - TONOLHER - 040225-compactado.pdf"
    slides_content = extract_pdf_content(pdf_path)
    
    with open("slides_data.json", "w", encoding="utf-8") as f:
        json.dump(slides_content, f, ensure_ascii=False, indent=2)
    
    print(f"Extracted {len(slides_content)} slides with duplicate filtering.")
