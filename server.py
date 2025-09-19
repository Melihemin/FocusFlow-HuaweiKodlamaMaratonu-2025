import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager

# Router'lar
from router.main import router as main_router
from router.platform import router as platform_router # 'education' router'ınızın adı buysa...

# Statik dosyalar ve şablonlar
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Veritabanı ve RAG Modeli
from database.settings import engine, Base, SessionLocal
import rag.model as rag_model

# Loglama yapılandırması
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Veritabanı tablolarını oluşturma
logging.info("Veritabanı tabloları kontrol ediliyor/oluşturuluyor...")
Base.metadata.create_all(bind=engine)

# --- KRİTİK EKSİK BÖLÜM: LIFESPAN YÖNETİCİSİ ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("="*50)
    logging.info(">>> UYGULAMA YAŞAM DÖNGÜSÜ BAŞLIYOR (LIFESPAN)...")
    
    # Sunucu başlarken önce diskten retriever'ı yüklemeyi dene
    rag_model.retriever_cache = rag_model.load_retriever_from_disk()

    # Eğer diskte hazır retriever yoksa, veritabanından oluştur
    if rag_model.retriever_cache is None:
        logging.warning("Disk üzerinde hazır bir retriever bulunamadı. Veritabanından yeniden oluşturulacak.")
        db = SessionLocal()
        try:
            # Veritabanından oluştur ve diske kaydet
            rag_model.retriever_cache = rag_model.create_and_save_retriever_from_db(db)
        finally:
            db.close()

    if rag_model.retriever_cache:
        logging.info(">>> Retriever başarıyla yüklendi. Uygulama hazır. <<<")
    else:
        logging.error(">>> KRİTİK HATA: Retriever yüklenemedi! <<<")
    
    logging.info("="*50)
    yield
    # Uygulama kapandığında çalışacak kod
    logging.info("\nUygulama kapanıyor.")

# FastAPI uygulamasını lifespan yöneticisiyle başlat
app = FastAPI(lifespan=lifespan)

# Router'ları uygulamaya dahil et
app.include_router(main_router)
app.include_router(platform_router)

# Statik dosyaları bağla
app.mount("/static", StaticFiles(directory="static"), name="static")

# (İsteğe bağlı, notlara bakın) Şablonları burada da tanımlayabilirsiniz
templates = Jinja2Templates(directory="templates")

# Sağlık kontrolü endpoint'i
@app.get("/health", tags=["System"])
def health_check():
    if rag_model.retriever_cache is not None:
        return {"status": "ok", "retriever_status": "ready"}
    else:
        return {"status": "error", "retriever_status": "not_ready"}

# Uvicorn ile çalıştırma komutu
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)