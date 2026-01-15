# palm_app/rag_db/build_rag_index.py

import os
import pickle
import faiss
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer


# -----------------------------
# 📌 1. Paths
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent
TEXT_PATH = BASE_DIR / "palm_knowledge_ar.txt"
PICKLE_PATH = BASE_DIR / "index.pkl"
FAISS_PATH = BASE_DIR / "index.faiss"


# -----------------------------
# 📌 2. Settings
# -----------------------------
CHUNK_SIZE = 350     # حجم كل مقطع نصي
EMBED_MODEL = "all-MiniLM-L6-v2"


def load_text():
    if not TEXT_PATH.exists():
        raise FileNotFoundError(f"❌ File not found: {TEXT_PATH}")

    with open(TEXT_PATH, "r", encoding="utf-8") as f:
        text = f.read().strip()

    return text


def split_chunks(text, chunk_size=300):
    chunks = []
    buffer = ""

    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue

        # إذا السطر بحد ذاته طويل
        if len(line) > chunk_size:
            parts = [line[i:i+chunk_size] for i in range(0, len(line), chunk_size)]
            chunks.extend(parts)
        else:
            # مراكمة أسطر قصيرة
            if len(buffer) + len(line) <= chunk_size:
                buffer += " " + line
            else:
                chunks.append(buffer.strip())
                buffer = line

    if buffer:
        chunks.append(buffer.strip())

    return chunks


def main():
    print("📌 Loading knowledge text...")
    text = load_text()

    print("✂️ Splitting into chunks...")
    chunks = split_chunks(text, CHUNK_SIZE)
    print(f"📦 Total chunks: {len(chunks)}")

    print("🤖 Loading embedding model:", EMBED_MODEL)
    model = SentenceTransformer(EMBED_MODEL)

    print("🔢 Generating embeddings...")
    embeddings = model.encode(chunks)
    embeddings = np.array(embeddings).astype("float32")

    dim = embeddings.shape[1]
    print(f"📐 Embedding dimension: {dim}")

    print("📥 Creating FAISS index...")
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    print("💾 Saving FAISS index:", FAISS_PATH)
    faiss.write_index(index, str(FAISS_PATH))

    print("💾 Saving docs pickle:", PICKLE_PATH)
    with open(PICKLE_PATH, "wb") as f:
        pickle.dump({"docs": chunks}, f)

    print("\n🎉 Done!")
    print(f"➡️ Saved {len(chunks)} chunks")
    print(f"➡️ Index location: {FAISS_PATH.name}")
    print(f"➡️ Metadata: {PICKLE_PATH.name}")


if __name__ == "__main__":
    main()
