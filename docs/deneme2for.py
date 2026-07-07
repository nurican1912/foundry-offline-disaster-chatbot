dosya_adi = "afet_rescuer_qa.md" 

with open(dosya_adi, "r", encoding="utf-8") as f:
    tum_metin = f.read()

# 1. ADIM: Metni parçaladık ve koca bir liste elde ettik
bloklar = tum_metin.split("## ")

def chunk_qa_markdown(text: str, source: str, role: str) -> list[dict]:
    chunks: list[dict] = []
    
    bloklar = text.split("## ")

    for blok in bloklar[1:]:
        satirlar = blok.strip().splitlines()

        