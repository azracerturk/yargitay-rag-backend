import psycopg2
import random

DATABASE_URL = "postgresql://user:password@localhost:5432/yargitay_rag"

def embed_metin(metin):
    """
    GEÇİCİ ÇÖZÜM: indeksle.py'deki ile aynı mantık.
    Gerçek LiteLLM API anahtarı gelince bu fonksiyon güncellenecek.
    """
    return [random.uniform(-1, 1) for _ in range(1536)]

def en_yakin_parcalari_bul(soru, limit=5):
    """
    Verilen soruya en yakın (cosine benzerlik açısından) parçaları
    veritabanından bulur. Model çağrısı YAPMAZ, sadece arama yapar.
    """
    soru_embedding = embed_metin(soru)

    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute(
        """
        SELECT p.id, p.metin, p.karar_id, k.baslik, k.kaynak_url,
               p.embedding <=> %s::vector AS mesafe
        FROM parcalar p
        JOIN kararlar k ON p.karar_id = k.id
        ORDER BY mesafe ASC
        LIMIT %s
        """,
        (soru_embedding, limit)
    )

    sonuclar = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {
            "parca_id": r[0],
            "metin": r[1],
            "karar_id": r[2],
            "karar_baslik": r[3],
            "kaynak_url": r[4],
            "mesafe": float(r[5])
        }
        for r in sonuclar
    ]

if __name__ == "__main__":
    soru = "borç yenileme sözleşmesi nedir"
    sonuclar = en_yakin_parcalari_bul(soru, limit=5)

    print(f"Soru: {soru}\n")
    print(f"{len(sonuclar)} parça bulundu:\n")
    for i, s in enumerate(sonuclar, 1):
        print(f"--- Sonuç {i} (mesafe: {s['mesafe']:.4f}) ---")
        print(f"Karar: {s['karar_baslik']}")
        print(f"Metin: {s['metin'][:150]}...")
        print()