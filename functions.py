import streamlit as st
from zipfile import ZipFile
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO, BytesIO
import base64
import pdf2image
import pytesseract
from pytesseract import Output, TesseractError
import cv2
import numpy as np

# ------- OCR with Image Preprocessing (OpenCV) -----------

def preprocess_image_for_ocr(image):
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    
    # Apply thresholding to make text stand out
    _, processed_image = cv2.threshold(gray_image, 150, 255, cv2.THRESH_BINARY)
    
    return processed_image

@st.cache_data
def images_to_txt(path, language):
    images = pdf2image.convert_from_bytes(path)
    all_text = []
    for i in images:
        processed_image = preprocess_image_for_ocr(i)  # Preprocess image for better OCR
        text = pytesseract.image_to_string(processed_image, lang=language)
        all_text.append(text)
    return all_text, len(all_text)

# ------- PDF to Text Extraction (PDFMiner) -----------

@st.cache_data
def convert_pdf_to_txt_pages(pdf_file):
    texts = []
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    
    size = 0
    c = 0
    nbPages = 0
    with BytesIO(pdf_file) as f:
        for page in PDFPage.get_pages(f):
            interpreter.process_page(page)
            t = retstr.getvalue()
            if c == 0:
                texts.append(t)
            else:
                texts.append(t[size:])
            c += 1
            size = len(t)
            nbPages += 1

    device.close()
    retstr.close()
    return texts, nbPages


@st.cache_data
def convert_pdf_to_txt_file(pdf_file):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    with BytesIO(pdf_file) as f:
        for page in PDFPage.get_pages(f):
            interpreter.process_page(page)

    text = retstr.getvalue()
    device.close()
    retstr.close()
    return text


@st.cache_data
def save_pages(pages):
    files = []
    for page in range(len(pages)):
        filename = "page_" + str(page) + ".txt"
        with open("./file_pages/" + filename, 'w', encoding="utf-8") as file:
            file.write(pages[page])
            files.append(file.name)

    # Create zipfile object
    zip_path = './file_pages/pdf_to_txt.zip'
    with ZipFile(zip_path, 'w') as zipObj:
        for f in files:
            zipObj.write(f)
    
    return zip_path


def display_pdf(file):
    base64_pdf = base64.b64encode(file).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)


# ------- Streamlit UI --------

st.title("PDF to Text Converter")

# Upload PDF
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file is not None:
    st.sidebar.header("Options")
    extraction_method = st.sidebar.selectbox(
        "Choose extraction method:",
        ["PDF Text", "OCR (Image-based PDFs)"]
    )

    language = st.sidebar.text_input("OCR Language (if using OCR)", "eng")

    # Show PDF
    display_pdf(uploaded_file.read())

    if extraction_method == "PDF Text":
        st.write("Extracting text from PDF...")
        pdf_text, num_pages = convert_pdf_to_txt_pages(uploaded_file.read())
        st.write(f"Extracted {num_pages} pages")
        st.text_area("PDF Text", "\n\n".join(pdf_text), height=400)

    elif extraction_method == "OCR (Image-based PDFs)":
        st.write("Extracting text using OCR...")
        ocr_text, num_pages = images_to_txt(uploaded_file.read(), language)
        st.write(f"OCR extracted text from {num_pages} pages")
        st.text_area("OCR Text", "\n\n".join(ocr_text), height=400)
