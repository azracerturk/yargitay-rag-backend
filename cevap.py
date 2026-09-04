from arama import en_yakin_parcalari_bul

PROMPT_SABLONU = """Aşağıda Yargıtay kararlarından alınmış bazı metin parçaları verilmiştir.
SADECE bu parçalara dayanarak soruyu cevapla. Parçalarda yeterli bilgi yoksa
"Verilen kararlarda bu soruya yeterli bilgi bulunamadı." diye belirt.
Kendi genel bilginden veya parçalarda olmayan bilgilerden yararlanma.

--- KARAR PARÇALARI ---
{parcalar_metni}
--- KARAR PARÇALARI SONU ---

SORU: {soru}

CEVAP:"""

def prompt_olustur(soru, parcalar):
    parcalar_metni = "\n\n".join(
        f"[Parça {i+1} - {p['karar_baslik']}]\n{p['metin']}"
        for i, p in enumerate(parcalar)
    )
    return PROMPT_SABLONU.format(parcalar_metni=parcalar_metni, soru=soru)

def cevap_uret(soru, parcalar):
    """
    GEÇİCİ ÇÖZÜM: Gerçek LiteLLM API anahtarı gelene kadar
    model çağrısı yapmadan placeholder bir cevap döndürür.
    İleride SADECE bu fonksiyonun içi LiteLLM çağrısına dönüşecek.
    """
    prompt = prompt_olustur(soru, parcalar)
    # Gerçek model çağrısı burada olacak, örn:
    # response = litellm.completion(model="...", messages=[{"role": "user", "content": prompt}])
    # return response.choices[0].message.content
    return f"[GEÇİCİ CEVAP - model henüz bağlı değil] {len(parcalar)} parça bulundu, prompt {len(prompt)} karakter uzunluğunda hazırlandı."

def soru_sor(soru, limit=5):
    """
    Ana fonksiyon: soruyu al, ilgili parçaları bul, cevabı üret,
    cevap + kaynak kararları birlikte döndür.
    """
    parcalar = en_yakin_parcalari_bul(soru, limit=limit)
    cevap = cevap_uret(soru, parcalar)

    kaynaklar = [
        {"baslik": p["karar_baslik"], "kaynak_url": p["kaynak_url"]}
        for p in parcalar
    ]

    return {
        "soru": soru,
        "cevap": cevap,
        "kaynaklar": kaynaklar
    }

if __name__ == "__main__":
    sonuc = soru_sor("borç yenileme sözleşmesi nedir")

    print(f"Soru: {sonuc['soru']}\n")
    print(f"Cevap: {sonuc['cevap']}\n")
    print("Kaynaklar:")
    for k in sonuc["kaynaklar"]:
        print(f"  - {k['baslik']} ({k['kaynak_url']})")