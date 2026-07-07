"""Chunking — ham dökümanları embed edilecek anlamlı parçalara (chunk) böler.

Her chunk, kaynağından bağımsız ORTAK bir sözlük yapısına normalize edilir:
    {
        "content":  str,          # embed edilecek + context olarak dönecek metin
        "source":   str,          # kaynak dosya etiketi (ör. "afet_victim_qa.md")
        "type":     str,          # "qa" | "prose"
        "role":     str | None,   # "victim" | "rescuer" | None (prose'da None)
        "category": str | None,   # varsa Q&A kategorisi
    }
"""


def chunk_qa_markdown(text: str, source: str, role: str) -> list[dict]:
    """Q&A markdown metnini, her '## soru + cevabı' bir chunk olacak şekilde böler.

    Beklenen blok biçimi:
        ## <soru>
        **Kategori:** <kategori>
        <cevap paragrafı>
        ---
    """
    chunks: list[dict] = []

    blocks = text.split("##")

    for block in blocks[1:]:
        rows = block.strip().splitlines()

        questions = rows[0].strip
        category = rows[1].strip
        answers = rows[2].strip()

        content = questions + "\n" + answers

        chunks = {
        "content": content,
        "source": source,
        "type": "qa",
        "role": role,
        "category": category
    }



   
    return chunks









 