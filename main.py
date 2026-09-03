import requests
import time
from bs4 import BeautifulSoup

BASE_URL = "https://karararama.yargitay.gov.tr"
HEADERS = {"Content-Type": "application/json"}

def karar_listesi_getir(sayfa_no, sayfa_boyutu=10, arama_kelimesi="borç"):
    url = f"{BASE_URL}/aramalist"
    payload = {
        "data": {
            "aranan": arama_kelimesi,
            "arananKelime": arama_kelimesi,
            "pageSize": sayfa_boyutu,
            "pageNumber": sayfa_no
        }
    }
    response = requests.post(url, json=payload, headers=HEADERS)
    response.raise_for_status()
    return response.json()["data"]["data"]

def karar_metni_getir(karar_id):
    url = f"{BASE_URL}/getDokuman"
    params = {"id": karar_id}
    response = requests.get(url, params=params, headers=HEADERS)
    response.raise_for_status()
    html_icerik = response.json()["data"]
    soup = BeautifulSoup(html_icerik, "html.parser")
    return soup.get_text(separator="\n", strip=True)

def tum_kararlari_topla(hedef_sayi=200, arama_kelimesi="borç"):
    toplanan = []
    sayfa_no = 1
    sayfa_boyutu = 10

    while len(toplanan) < hedef_sayi:
        ozet_liste = karar_listesi_getir(sayfa_no, sayfa_boyutu, arama_kelimesi)
        if not ozet_liste:
            break

        for ozet in ozet_liste:
            if len(toplanan) >= hedef_sayi:
                break
            print(f"Çekiliyor: {ozet['esasNo']} / {ozet['kararNo']}")
            tam_metin = karar_metni_getir(ozet["id"])
            toplanan.append({
                "baslik": f"{ozet['daire']} - {ozet['esasNo']}/{ozet['kararNo']}",
                "tam_metin": tam_metin,
                "kaynak_url": f"{BASE_URL}/getDokuman?id={ozet['id']}",
                "tarih": ozet["kararTarihi"]
            })
            time.sleep(1)

        sayfa_no += 1
        time.sleep(1)

    return toplanan

if __name__ == "__main__":
    kararlar = tum_kararlari_topla(hedef_sayi=5)
    print(f"\nToplam {len(kararlar)} karar toplandı.")
    print(kararlar[0])
