import os
import fitz
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


# Register fonts once
FONT_DIR = "fonts"

pdfmetrics.registerFont(
    TTFont("Deva", os.path.join(FONT_DIR, "NotoSansDevanagari-VariableFont_wdth,wght.ttf"))
)

pdfmetrics.registerFont(
    TTFont("Gujarati", os.path.join(FONT_DIR, "NotoSansGujarati-VariableFont_wdth,wght.ttf"))
)


def extract_pdf_blocks(path):

    #Extracts text blocks with positions using PyMuPDF
    
    doc = fitz.open(path)
    pages = []

    for page in doc:
        blocks = page.get_text("blocks")
        pages.append(blocks)

    return pages


def rebuild_pdf(pages, output_path, target_language):
    
    #Rebuild PDF using Unicode fonts so Indian scripts render correctly
   

    c = canvas.Canvas(output_path, pagesize=A4)

    if target_language in ["Hindi", "Marathi"]:
        font_name = "Deva"
    elif target_language == "Gujarati":
        font_name = "Gujarati"
    else:
        font_name = "Helvetica"

    c.setFont(font_name, 10)

    for page in pages:
        for block in page:
            x, y, w, h, text, *_ = block

            # Avoid empty blocks
            if not text.strip():
                continue

            c.drawString(x, 800 - y, text)

        c.showPage()

    c.save()
