import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import os

class OCRService:
    def __init__(self):
        # Windows için Tesseract path (gerekirse ayarlayın)
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        pass
    
    def extract_text(self, file_path: str) -> str:
        """
        Görüntü veya PDF dosyasından metin çıkarır
        """
        try:
            file_ext = os.path.splitext(file_path)[1].lower()
            
            if file_ext == '.pdf':
                # PDF'i görüntüye çevir
                images = convert_from_path(file_path)
                text = ""
                for image in images:
                    text += pytesseract.image_to_string(image, lang='tur') + "\n"
                return text.strip()
            
            elif file_ext in ['.jpg', '.jpeg', '.png', '.bmp']:
                # Görüntü dosyasını oku
                image = Image.open(file_path)
                text = pytesseract.image_to_string(image, lang='tur')
                return text.strip()
            
            else:
                raise ValueError(f"Desteklenmeyen dosya formatı: {file_ext}")
        
        except Exception as e:
            raise Exception(f"OCR hatası: {str(e)}")




