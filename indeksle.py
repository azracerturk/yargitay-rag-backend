import json
import psycopg2
import random

DATABASE_URL = "postgresql://user:password@localhost:5432/yargitay_rag"

def embed_metin(metin):
    """
    GEÇİCİ ÇÖZÜM: Gerçek LiteLLM/API anahtarı gelene kadar
    rastgele 1536 boyutlu bir vektör döndürür.
    """
    return [random.uniform(-1, 1) for _ in range(1536)]

def metni_parcala(metin, parca_boyutu=800, ortusme=100):
    parcalar = []
    basla = 0
    while basla < len(metin):
        bitis = basla + parca_boyutu
        parcalar.append(metin[basla:bitis])
        basla += parca_boyutu - ortusme
    return parcalar

def gecerli_mi(karar):
    """Placeholder/geçersiz içerikleri filtreler."""
    metin = karar.get("tam_metin", "")
    if len(metin) < 200:  # çok kısa metinler muhtemelen placeholder
        return False
    if metin.strip().startswith("(Kapatılan)"):
        return False
    return True

def indeksle():
    with open("kararlar.json", "r", encoding="utf-8") as f:
        kararlar = json.load(f)

    kararlar = [k for k in kararlar if gecerli_mi(k)]
    print(f"Filtreleme sonrası {len(kararlar)} geçerli karar bulundu.")

    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    for i, karar in enumerate(kararlar):
        cur.execute(
            """
            INSERT INTO kararlar (baslik, tam_metin, kaynak_url, tarih)
            VALUES (%s, %s, %s, TO_DATE(%s, 'DD.MM.YYYY'))
            RETURNING id
            """,
            (karar["baslik"], karar["tam_metin"], karar["kaynak_url"], karar["tarih"])
        )
        karar_id = cur.fetchone()[0]

        parcalar = metni_parcala(karar["tam_metin"])
        for parca in parcalar:
            embedding = embed_metin(parca)
            cur.execute(
                "INSERT INTO parcalar (karar_id, metin, embedding) VALUES (%s, %s, %s)",
                (karar_id, parca, embedding)
            )

        conn.commit()
        print(f"[{i+1}/{len(kararlar)}] {karar['baslik']} -> {len(parcalar)} parça indekslendi")

    cur.close()
    conn.close()
    print("\nİndeksleme tamamlandı.")

if __name__ == "__main__":
    indeksle()