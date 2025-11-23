import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import os
from typing import List, Dict
import json
import PIL.Image
import io
import base64

class AIService:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable bulunamadı!")
        genai.configure(api_key=api_key)
        
        # En uyumlu model
        self.model = genai.GenerativeModel('gemini-flash-latest')

        self.safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]

    # --- DÜZELTİLEN KISIM: Hem metin hem resim kabul ediyor ---
    def analyze_report(self, report_text: str = None, image_data: str = None) -> Dict:
        
        # Prompt (Basit Dil Talimatı)
        prompt = """Sen yardımsever bir sağlık asistanısın.
        Bu tahlil raporunu (resim veya metin) incele ve tıp bilmeyen birine 
        en sade, basit ve anlaşılır şekilde özetle.

        Kurallar:
        1. Sadece en önemli 1-2 sonucu söyle.
        2. Uzun açıklamalar yapma, en fazla 3-4 cümle kur.
        3. Tıbbi terim kullanma, halk diliyle konuş (Örn: Lökosit yerine 'Savunma hücreleri' de).
        4. Cevabı MUTLAKA şu JSON formatında ver:
        {{
            "analysis": "Raporun çok kısa ve net özeti.",
            "medications": ["Varsa ilaç/vitamin (yoksa boş bırak)"],
            "recommendations": "1-2 tane çok kısa öneri."
        }}
        """
        
        # İçerik listesi oluştur (Prompt + Metin + Resim)
        content = [prompt]
        
        if report_text:
            content.append(f"Rapor Metni: {report_text}")
            
        if image_data:
            try:
                if "base64," in image_data:
                    image_data = image_data.split("base64,")[1]
                img_bytes = base64.b64decode(image_data)
                img = PIL.Image.open(io.BytesIO(img_bytes))
                content.append(img)
            except Exception as e:
                print(f"Resim hatası: {e}")

        try:
            response = self.model.generate_content(
                content,
                safety_settings=self.safety_settings
            )
            
            result_text = response.text
            
            # JSON Temizleme
            try:
                if "```json" in result_text:
                    result_text = result_text.replace("```json", "").replace("```", "")
                elif "```" in result_text:
                    result_text = result_text.replace("```", "")
                
                start_idx = result_text.find('{')
                end_idx = result_text.rfind('}') + 1
                if start_idx != -1 and end_idx != 0:
                    json_text = result_text[start_idx:end_idx]
                    result = json.loads(json_text)
                    return result
            except:
                pass
            
            return {
                "analysis": result_text,
                "medications": ["Doktorunuza danışınız"],
                "recommendations": "Sağlıklı günler."
            }
        
        except Exception as e:
            print(f"\n!!! RAPOR HATASI !!!: {str(e)}\n")
            return {
                "analysis": "Raporu okurken bir hata oluştu.",
                "medications": [],
                "recommendations": ""
            }
    
    def chat_with_doctor(self, message: str, conversation_history: List[Dict] = None) -> str:
        if conversation_history is None:
            conversation_history = []
        
        system_prompt = """Sen çok kısa ve öz konuşan bir sağlık asistanısın.
        Cevapların net, basit ve anlaşılır olsun.
        Asla uzun paragraflar yazma. Maksimum 2-3 cümle ile cevap ver."""
        
        chat_prompt = system_prompt + "\n\n"
        
        for hist in conversation_history:
            role = hist.get("role", "user")
            content = hist.get("content", "")
            if role == "user":
                chat_prompt += f"Kullanıcı: {content}\n\n"
            elif role == "assistant":
                chat_prompt += f"Asistan: {content}\n\n"
        
        chat_prompt += f"Kullanıcı: {message}\n\nAsistan: "
        
        try:
            response = self.model.generate_content(
                chat_prompt,
                safety_settings=self.safety_settings
            )
            return response.text
        
        except Exception as e:
            print(f"\n!!! CHAT HATASI !!!: {str(e)}\n")
            return "Bağlantı hatası."