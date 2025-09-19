import os
import logging
from typing import List
from dotenv import load_dotenv
from sqlalchemy.orm import Session

# LangChain Kütüphaneleri
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from database.models import Lesson

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY bulunamadı. Lütfen .env dosyasını kontrol edin.")

model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key)
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)
parser = StrOutputParser()


rag_prompt_template = ChatPromptTemplate.from_template(
    "Sen, DEHB (Dikkat Eksikliği ve Hiperaktivite Bozukluğu) olan bireyler için uzman bir eğitim materyali yazarı ve kişisel bir öğretmensin.\n"
    "Görevin, sana verilen ham konu metinlerini (`BAĞLAM`) kullanarak, belirtilen isteğe (`İSTEK`) uygun, yepyeni ve anlaşılır bir konu anlatımı hazırlamaktır.\n\n"
    "Anlatımında şu prensiplere harfiyen uy:\n"
    "- Sadece ve sadece BAĞLAM'daki bilgileri kullan, dışarıdan asla bilgi ekleme.\n"
    "- Adım adım, basit ve net cümleler kur.\n"
    "- Her paragrafta sadece tek bir fikre odaklan.\n"
    "- Karmaşık terimleri mutlaka basitçe tanımla.\n"
    "- Anahtar noktaları vurgulamak için somut örnekler ve akılda kalıcı benzetmeler kullan (örneğin: 'bunu bir trafik ışığı gibi düşünebilirsin').\n\n"
    "--- BAĞLAM ---\n{context}\n\n"
    "--- İSTEK ---\n{istek}\n\n"
    "HAZIRLADIĞIN KONU ANLATIMI:"
)

retriever_cache = None
FAISS_INDEX_PATH = "faiss_index"

def create_and_save_retriever_from_db(db: Session):
    """
    Veritabanından dokümanları okur, bir retriever oluşturur ve onu diske kaydeder.
    Bu fonksiyon sadece ilk kurulumda veya veri güncellendiğinde çalıştırılmalıdır.
    """
    logging.info("Veritabanından retriever oluşturuluyor ve diske kaydedilecek...")
    all_lessons = db.query(Lesson).all()
    docs = []
    for lesson in all_lessons:
        for i in range(1, 11): # Varsayılan 10 ünite
            unit_content = getattr(lesson, f'unit_{i}', None)
            if unit_content:
                docs.append(Document(page_content=unit_content, metadata={"lesson_id": lesson.id, "unit_id": i}))

    if not docs:
        logging.warning("Veritabanında işlenecek doküman bulunamadı. Retriever oluşturulamadı.")
        return None

    try:
        vector_store = FAISS.from_documents(docs, embeddings)
        vector_store.save_local(FAISS_INDEX_PATH)
        logging.info(f"Vektör deposu başarıyla oluşturuldu ve '{FAISS_INDEX_PATH}' konumuna kaydedildi.")
        return vector_store.as_retriever(search_kwargs={"k": 3})
    except Exception as e:
        logging.error(f"Vektör deposu oluşturulurken veya kaydedilirken hata oluştu: {e}")
        return None

def load_retriever_from_disk():
    """
    Diske kaydedilmiş FAISS indeksini yükler ve bir retriever olarak döndürür.
    """
    if not os.path.exists(FAISS_INDEX_PATH):
        logging.warning(f"'{FAISS_INDEX_PATH}' konumunda kayıtlı bir indeks bulunamadı.")
        return None
    
    try:
        logging.info(f"'{FAISS_INDEX_PATH}' konumundan retriever yükleniyor...")
        vector_store = FAISS.load_local(FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
        logging.info("Retriever diskten başarıyla yüklendi.")
        return vector_store.as_retriever(search_kwargs={"k": 3})
    except Exception as e:
        logging.error(f"Retriever diskten yüklenirken hata oluştu: {e}")
        return None

def format_docs(docs: List[Document]) -> str:
    """Retriever'dan gelen dokümanları tek bir metin haline getirir."""
    return "\n\n".join(doc.page_content for doc in docs)

def generate_rag_answer(request_text: str) -> str:
    """
    Verilen isteğe göre, hafızadaki retriever'ı kullanarak bir konu anlatımı üretir.
    """
    global retriever_cache
    if retriever_cache is None:
        logging.warning("generate_rag_answer çağrıldı ancak retriever hazır değil.")
        return "Hata: Bilgi tabanı (retriever) henüz hazır değil. Lütfen sunucu loglarını kontrol edin veya yöneticiyle iletişime geçin."

    rag_chain = (
        {"context": retriever_cache | format_docs, "istek": RunnablePassthrough()}
        | rag_prompt_template
        | model
        | parser
    )
    
    # Zinciri, kullanıcıdan gelen istek metniyle çalıştır
    response_text = rag_chain.invoke(request_text)
    return response_text