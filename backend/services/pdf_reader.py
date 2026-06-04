import pytesseract
from pdf2image import convert_from_path
from pypdf import PdfReader

# =====================================================================
# 🚨 YOUR WINDOWS PATHS CONFIGURED 🚨
# =====================================================================
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
POPPLER_PATH = r'C:\poppler-26.02.0\Library\bin'

def extract_text(pdf_path):
    text = ""
    
    try:
        # Phase 1: Try Standard Digital Extraction (Super Fast)
        print(f"\n[INFO] Attempting standard text extraction for {pdf_path.name}...")
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    except Exception as e:
        print(f"[WARNING] Standard extraction failed: {e}")

    cleaned_text = text.strip()

    # Phase 2: If we got almost no text, it's a scanned image/handwriting! Trigger OCR.
    if len(cleaned_text) < 50:  
        print(f"[INFO] 🚨 Minimal text found in {pdf_path.name}. Triggering OCR for handwriting...")
        
        try:
            # Convert PDF pages to images USING YOUR POPPLER PATH
            images = convert_from_path(pdf_path, poppler_path=POPPLER_PATH) 
            
            ocr_text = ""
            for i, img in enumerate(images):
                print(f"  -> Reading handwriting on Page {i+1}...")
                
                # The OCR magic happens here USING YOUR TESSERACT PATH
                page_ocr = pytesseract.image_to_string(img)
                ocr_text += page_ocr + "\n"
                
            cleaned_text = ocr_text.strip()
            
        except Exception as e:
            print(f"[ERROR] OCR completely failed: {e}")
            print("[HELP] Please ensure the Poppler and Tesseract paths are 100% correct.")

    print(f"\n[DEBUG] Final Extraction: {len(cleaned_text)} characters from {pdf_path.name}")
    
    return cleaned_text