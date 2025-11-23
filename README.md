# Asistan Doktor - Backend API

## Kurulum

1. Python 3.8+ yüklü olduğundan emin olun

2. Bağımlılıkları yükleyin:
```bash
pip install -r requirements.txt
```

3. Tesseract OCR'ı yükleyin:
- Windows: https://github.com/UB-Mannheim/tesseract/wiki
- Mac: `brew install tesseract tesseract-lang`
- Linux: `sudo apt-get install tesseract-ocr tesseract-ocr-tur`

4. `.env` dosyası oluşturun ve Google Gemini API anahtarınızı ekleyin:
```
GOOGLE_API_KEY=your_api_key_here
```

   Google Gemini API anahtarı almak için: https://makersuite.google.com/app/apikey

5. Sunucuyu başlatın:
```bash
python main.py
```

API http://localhost:8000 adresinde çalışacaktır.

## Endpoints

- `POST /api/upload-report` - Tahlil raporu yükleme ve analiz
- `POST /api/chat` - Doktor ile sohbet

