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
Yargıtay karar arama sitesinden (karararama.yargitay.gov.tr) veri çekiliyor.

Not: Site, bulut sunucu IP'lerini (Azure/Codespaces) engellediği için veri toplama scripti (main.py) yerel bir bilgisayardan çalıştırılıp kararlar.json dosyası üretildi, ardından bu depoya yüklendi.

İndeksleme (indeksle.py):
- kararlar.json okunur, geçersiz/placeholder içerikler filtrelenir
- Her karar 'kararlar' tablosuna yazılır
- Karar metni ~800 karakterlik parçalara bölünür (100 karakter örtüşme ile)
- Her parça embed edilir (şu an geçici/rastgele vektör, LiteLLM API anahtarı geldiğinde gerçek embedding'e geçilecek) ve 'parcalar' tablosuna yazılır
- Veri yüklendikten sonra pgvector HNSW indeksi oluşturulur

Toplam: 183 karar, 2919 parça

## Uç Noktalar

Şu an fonksiyon seviyesinde çalışıyor, FastAPI endpoint'lerine Aşama 6'da dönüştürülecek:
- arama.py -> en_yakin_parcalari_bul(soru, limit): soruya en yakın N parçayı döndürür (modelsiz test için)
- cevap.py -> soru_sor(soru, limit): parçaları bulur, prompt şablonuna yerleştirir, model çağrısı yapar (şu an geçici stub, LiteLLM API anahtarı geldiğinde gerçek çağrıya geçilecek) ve cevap + kaynak kararlar listesini döndürür
