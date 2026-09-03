# yargitay-rag-backend


Yargıtay kararları üzerinde soru-cevap yapabilen RAG uygulamasının backend'i.

Proje repo'su: (link eklenecek)
Frontend repo'su: (link eklenecek)

## Teknolojiler
- Python
- PostgreSQL + pgvector
- LiteLLM (embedding ve LLM çağrıları için)

## Kurulum

1. Depoyu klonla ve içine gir:

2. Sanal ortam oluştur ve aktive et:

3. Bağımlılıkları kur:

4. `.env.example` dosyasını `.env` olarak kopyala ve kendi bilgilerinle doldur:

5. Uygulamayı çalıştır:

## Veritabanı Hazırlığı
PostgreSQL + pgvector Docker ile çalıştırılıyor:

docker run --name yargitay-postgres \
  -e POSTGRES_USER=user \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=yargitay_rag \
  -p 5432:5432 \
  -d pgvector/pgvector:pg16

Vektör eklentisini aktif et:

docker exec -it yargitay-postgres psql -U user -d yargitay_rag
CREATE EXTENSION IF NOT EXISTS vector;

Tablolar:
- `kararlar`: id, baslik, tam_metin, kaynak_url, tarih
- `parcalar`: id, karar_id, metin, embedding (vector(1536))


## Veri Toplama ve İndeksleme
(yakında)

## Uç Noktalar
(yakında)
