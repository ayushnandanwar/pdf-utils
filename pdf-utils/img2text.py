import fitz  # PyMuPDF
from PIL import Image
import pytesseract
from io import BytesIO
import textwrap
import os

def image_pdf_to_text_pdf(input_pdf, output_pdf):
    doc = fitz.open(input_pdf)
    text_pdf = fitz.open()

    for page_num in range(len(doc)):
        page = doc[page_num]
        image_list = page.get_images(full=True)
        
        if not image_list:
            continue

        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            img = Image.open(BytesIO(image_bytes)).convert('RGB')
            
            # Extract text using Tesseract
            extracted_text = pytesseract.image_to_string(img).strip('\f')
            
            # Create a white background page with extracted text
            if extracted_text:
                new_page = text_pdf.new_page(width=page.rect.width, height=page.rect.height)
                new_page.insert_text((20, 40), extracted_text, fontsize=24)
    
    text_pdf.save(output_pdf)
    print(f"Converted PDF saved as: {output_pdf}")


# Usage
# input_pdf = "/home/ayush.nandanwar/Downloads/Critical_Reading_Part_1_no_anno.pdf"
# output_pdf = "/home/ayush.nandanwar/Downloads/Critical_Reading_Part_1_no_anno_converted.pdf"
# image_pdf_to_text_pdf(input_pdf, output_pdf)

def convert_pdfs_in_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            input_pdf = os.path.join(input_folder, filename)
            output_pdf = os.path.join(output_folder, f"converted_{filename}")
            image_pdf_to_text_pdf(input_pdf, output_pdf)

# Usage
input_folder = "/home/ayush.nandanwar/Downloads/VARC/"
output_folder = "/home/ayush.nandanwar/Downloads/VARC_converted/"

convert_pdfs_in_folder(input_folder, output_folder)

# Install required libraries:
# pip install pymupdf pillow pytesseract opencv-python-headless numpy
# And make sure Tesseract OCR is configured.

# Let me know if you want me to tweak anything further! 🚀
