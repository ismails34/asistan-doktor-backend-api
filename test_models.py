import google.generativeai as genai
import os
from dotenv import load_dotenv

# .env dosyasındaki anahtarı yükle
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("HATA: API Anahtarı bulunamadı! .env dosyasını kontrol edin.")
else:
    print(f"Kullanılan Anahtar: {api_key[:5]}...{api_key[-4:]}")
    
    try:
        genai.configure(api_key=api_key)
        
        print("\n--- ERİŞİLEBİLİR MODELLER LİSTESİ ---")
        # Modelleri listele
        for m in genai.list_models():
            # Sadece içerik üretebilen (chat) modelleri göster
            if 'generateContent' in m.supported_generation_methods:
                print(f"- {m.name}")
        
        print("\n-------------------------------------")

    except Exception as e:
        print(f"\nBÜYÜK HATA OLUŞTU: {str(e)}")