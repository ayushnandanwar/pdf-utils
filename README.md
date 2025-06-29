# PDF Utils

Convert scanned/image-based PDFs into searchable, text-based PDFs using OCR (Tesseract) and PyMuPDF.

## Features

- **Batch Conversion:** Process multiple PDFs in parallel for efficiency.
- **OCR Extraction:** Uses Tesseract to extract text from images in PDFs.
- **Organized Output:** Saves converted PDFs in structured folders.
- **Customizable:** Easily adjust batch size and output settings.

## Installation
1. Install Tesseract OCR:
    - macOS: `brew install tesseract`
    - Ubuntu: `sudo apt-get install tesseract-ocr`
    - Windows: Download from https://github.com/tesseract-ocr/tesseract

2. Install Python dependencies:
    ```
    pip install pytesseract pymupdf Pillow
    ```
