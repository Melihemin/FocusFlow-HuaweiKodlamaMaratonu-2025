import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends
from sqlalchemy.orm import Session
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from database.settings import SessionLocal
from database.models import Lesson

# --- Kurulum ve Konfigürasyon ---

# Veritabanı bağlantısı için gerekli fonksiyon ve dependency
def connect():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(connect)]

# API Anahtarı ve Model Yapılandırması
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY bulunamadı.")

# 1. LangChain Modelini Başlatma
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key)

# 2. Çıktıyı metne çevirecek parser
parser = StrOutputParser()

# 3. Prompt Şablonu
explanator_prompt_template = ChatPromptTemplate.from_template(
    "Senin görevin, DEHB (Dikkat Eksikliği ve Hiperaktivite Bozukluğu) olan, konuya yeni başlayan bir kişiye eğitim vermek."
    "Aşağıdaki konuyu sade, anlaşılır ve dikkat dağıtmayan bir şekilde açıklaman gerekiyor:\n\n{unit_content}\n\n"
    "Lütfen anlatımında şu prensiplere dikkat et:\n"
    "- Kısa ve net cümleler kullan.\n"
    "- Her paragrafta tek fikir ver.\n"
    "- Karmaşık terimleri basitleştirerek tanımla.\n"
    "- Anahtar noktaları vurgulamak için örnekler ve benzetmeler kullan.\n"
    "- Gerekirse adım adım anlatım yap.\n"
    "- Görsel düşünebilecek şekilde açıklamalar yap (örneğin: 'bunu bir trafik ışığı gibi düşünebilirsin').\n"
    "- Konunun özünü kaçırmadan detaylı ama sade bir anlatım sun.\n\n"
    "Hedefin: Konuyu DEHB'li bir bireyin dikkatini kaybetmeden, merakını canlı tutarak öğrenmesini sağlamak."
)

# 4. LangChain Zinciri (Chain)
# Bu üç bileşeni birbirine bağlıyoruz.
chain = explanator_prompt_template | model | parser


# --- Orijinal Fonksiyonun LangChain ile Yeniden Yazılmış Hali ---

def generate_explanation(lesson_id: int, unit_id: int, db: db_dependency) -> str:

    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        return "Lesson not found"
    
    # getattr() ile ilgili ünite içeriğini güvenli bir şekilde al
    unit_content = getattr(lesson, f'unit_{unit_id}', None)
    if not unit_content:
        return "Unit not found"
    
    # Orijinal koddaki model.generate_content() çağrısı yerine
    # LangChain zincirini .invoke() ile çağırıyoruz.
    response_text = chain.invoke({"unit_content": unit_content})
    
    return response_text