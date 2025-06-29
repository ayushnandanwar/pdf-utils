import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import os
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor
import shutil

def image_pdf_to_text_pdf(input_pdf, output_pdf):
    print(f"Converting PDF: {input_pdf}")
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
                lines = extracted_text.split('\n')
                
                # Define margins and font size
                margin = 20
                font_size = 24
                line_height = font_size * 1.5
                max_height = page.rect.height - 2 * margin
                
                y_offset = 40
                new_page = text_pdf.new_page(width=page.rect.width, height=page.rect.height)
                
                for line in lines:
                    if y_offset + line_height > max_height:
                        # Start a new page only when text overflows
                        new_page = text_pdf.new_page(width=page.rect.width, height=page.rect.height)
                        y_offset = 40
                    
                    new_page.insert_text((margin, y_offset), line, fontsize=font_size)
                    y_offset += line_height
    
    text_pdf.save(output_pdf)
    print(f"Converted PDF saved as: {output_pdf}")

# Usage
# input_pdf = "/home/ayush.nandanwar/Downloads/Critical_Reading_Part_1_no_anno.pdf"
# output_pdf = "/home/ayush.nandanwar/Downloads/Critical_Reading_Part_1_no_anno_converted.pdf"
# image_pdf_to_text_pdf(input_pdf, output_pdf)


def convert_pdfs_in_folder(input_folder, output_folder, batch_size=2):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    def convert_file(filename):
        if filename.endswith(".pdf"):
            input_pdf = os.path.join(input_folder, filename)
            output_pdf = os.path.join(output_folder, f"converted_{filename}")
            image_pdf_to_text_pdf(input_pdf, output_pdf)

    files = [f for f in os.listdir(input_folder) if f.endswith(".pdf")]
    
    with ThreadPoolExecutor(max_workers=batch_size) as executor:
        for i in range(0, len(files), batch_size):
            batch = files[i:i + batch_size]
            executor.map(convert_file, batch)

# Usage
# input_folder = "/Users/ayush.nandanwar/Downloads/CR"
# output_folder = "/Users/ayush.nandanwar/Downloads/CR_converted"

# convert_pdfs_in_folder(input_folder, output_folder)

# Install required libraries:
# pip install pymupdf pillow pytesseract

# Let me know if you want more fine-tuning! 🚀

def organize_and_convert_pdfs(input_dir):
    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
    def process_pdf(pdf_file):
        pdf_name = os.path.splitext(pdf_file)[0]
        pdf_dir = os.path.join(input_dir, pdf_name)
        if not os.path.exists(pdf_dir):
            os.makedirs(pdf_dir)
        original_pdf_path = os.path.join(input_dir, pdf_file)
        new_original_path = os.path.join(pdf_dir, pdf_file)
        os.rename(original_pdf_path, new_original_path)
        # shutil.copy2(original_pdf_path, new_original_path)
        converted_pdf_path = os.path.join(pdf_dir, f"converted_{pdf_file}")
        image_pdf_to_text_pdf(new_original_path, converted_pdf_path)

    # Set batch size (number of parallel threads)
    batch_size = 4  # You can make this configurable via function argument

    with ThreadPoolExecutor(max_workers=batch_size) as executor:
        executor.map(process_pdf, pdf_files)

# Usage
# input_dir = "/Users/ayush.nandanwar/Downloads/CR/CR_Based_Option_Elimination_Practice_I_KD_Sir_I_26th_March_
# 2025_with_anno.pdf"
input_dir = "/Users/ayush.nandanwar/Downloads/vocab"
organize_and_convert_pdfs(input_dir)
