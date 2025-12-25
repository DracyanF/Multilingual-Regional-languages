import streamlit as st
import tempfile

from docx_utils import extract_docx_paragraphs, rebuild_docx
from pdf_utils import extract_pdf_blocks, rebuild_pdf
from translator import translate_blocks

st.set_page_config("Document Translator", layout="wide")

st.title("📄 Multilingual Document Translator (Groq API)")

uploaded_file = st.file_uploader("Upload PDF or DOCX", type=["pdf", "docx"])

col1, col2 = st.columns(2)
with col1:
    source_lang = st.selectbox("Source Language", ["English", "Hindi", "Gujarati", "Marathi"])
with col2:
    target_lang = st.selectbox("Target Language", ["English", "Hindi", "Gujarati", "Marathi"])

if uploaded_file and source_lang != target_lang:
    if st.button("Translate"):
        with st.spinner("Translating..."):
            suffix = uploaded_file.name.split(".")[-1]
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix="." + suffix)
            tmp.write(uploaded_file.read())

            if suffix == "docx":
                blocks = extract_docx_paragraphs(tmp.name)
                translated = translate_blocks(blocks, source_lang, target_lang)
                output_path = "translated.docx"
                rebuild_docx(tmp.name, translated, output_path)

            elif suffix == "pdf":
                pages = extract_pdf_blocks(tmp.name)
                new_pages = []

                for page in pages:
                    texts = [b[4] for b in page]
                    translated = translate_blocks(texts, source_lang, target_lang)

                    updated = []
                    for i, block in enumerate(page):
                        b = list(block)
                        b[4] = translated[i]
                        updated.append(tuple(b))

                    new_pages.append(updated)

                output_path = "translated.pdf"
                rebuild_pdf(new_pages, output_path, target_lang)

            st.success("Translation complete!")

            with open(output_path, "rb") as f:
                st.download_button(
                    "Download translated file",
                    f,
                    file_name=output_path
                )
