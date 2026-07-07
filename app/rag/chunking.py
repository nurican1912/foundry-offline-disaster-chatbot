from pathlib import Path


def chunk_qa_markdown(text: str, source: str, role: str) -> list[dict]:
    """Q&A markdown metnini, her '## soru + cevabı' bir chunk olacak şekilde böler."""
    chunks: list[dict] = []

    blocks = text.split("## ")

    for block in blocks[1:]:              # blocks[0] = başlık/künye, atla
        lines = block.strip().splitlines()
        if not lines:
            continue

        question = lines[0].strip()

        category = None
        answer_lines = []
        for line in lines[1:]:
            stripped = line.strip()
            if stripped == "---":                       # ayıracı atla
                continue
            if stripped.startswith("**Kategori:**"):     # kategoriyi çek
                category = stripped.replace("**Kategori:**", "").strip()
                continue
            answer_lines.append(line)                    # kalanı cevaba ekle

        answer = "\n".join(answer_lines).strip()
        content = question + "\n" + answer

        chunks.append({
            "content": content,
            "source": source,
            "type": "qa",
            "role": role,
            "category": category,
        })

    return chunks


def chunk_prose_markdown(text: str, source: str) -> list[dict]:
    """Prose (rehber) markdown metnini başlık-tabanlı chunk'lara böler.

    Her '## başlık' + altındaki gövde bir chunk olur. role=None, type='prose'.
    """
    chunks: list[dict] = []

    blocks = text.split("## ")

    for block in blocks[1:]:              # blocks[0] = künye/başlık, atla
        lines = block.strip().splitlines()
        if not lines:
            continue

        heading = lines[0].replace("**", "").strip()   # başlık: '**' işaretlerini temizle
        body = "\n".join(lines[1:]).strip()            # gövde: kalan tüm satırlar

        if len(body) < 50:               # künye/İÇİNDEKİLER gibi kısa gürültüyü ele
            continue

        content = heading + "\n" + body

        chunks.append({
            "content": content,
            "source": source,
            "type": "prose",
            "role": None,
            "category": None,
        })

    return chunks


def load_qa_chunks(docs_dir: str) -> list[dict]:
    """docs_dir içindeki TÜM Q&A markdown dosyalarını okuyup chunk'lara böler.

    Q&A dosyaları adında 'qa' geçen .md dosyalarıdır (ör. afet_victim_qa.md).
    role, dosya adından türetilir: 'victim' veya 'rescuer'.
    """
    all_chunks: list[dict] = []

    # TODO (1) — adında 'qa' geçen .md dosyalarını topla (senin yazdığın kısım)
    qa_files = []
    for file in Path(docs_dir).glob("*.md"):
        if "qa" in file.name:
            qa_files.append(file)

    # TODO (2) — her Q&A dosyasını oku, role'ünü türet, chunk'la, birleştir
    for file in qa_files:
        text = file.read_text(encoding="utf-8")       # dosyanın metnini oku

        if "victim" in file.name:                     # role'ü ad'dan türet
            role = "victim"
        elif "rescuer" in file.name:
            role = "rescuer"
        else:
            role = None

        chunks = chunk_qa_markdown(text, source=file.name, role=role)
        all_chunks.extend(chunks)                     # listeyi düz şekilde ekle

    return all_chunks


def load_prose_chunks(docs_dir: str) -> list[dict]:
    all_chunks: list[dict] = []

    # 1) prose dosyalarını seç: adında "qa" ve "README" GEÇMEYENLER
    prose_files = []
    for file in Path(docs_dir).glob("*.md"):
        if "qa" not in file.name and "README" not in file.name:
            prose_files.append(file)

    # 2) her prose dosyasını oku, prose bölücüden geçir, birleştir
    for file in prose_files:
        text = file.read_text(encoding="utf-8")
        chunks = chunk_prose_markdown(text, source=file.name)
        all_chunks.extend(chunks)

    return all_chunks


def get_all_chunks(docs_dir: str) -> list[dict]:
    """Tüm kaynakların (Q&A + prose) chunk'larını tek düz listede toplar.

    Chunking modülünün TEK giriş noktası — ingestion (Modül C/B3) bunu çağırır,
    altındaki loader/chunker katmanlarını hiç bilmez.
    """
    qa_chunks = load_qa_chunks(docs_dir)
    prose_chunks = load_prose_chunks(docs_dir)
    return qa_chunks + prose_chunks
