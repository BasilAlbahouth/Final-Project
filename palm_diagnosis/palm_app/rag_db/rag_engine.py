import os
import pickle
import numpy as np
import faiss

from sentence_transformers import SentenceTransformer
from deep_translator import GoogleTranslator
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
PICKLE_PATH = BASE_DIR / "index.pkl"
FAISS_PATH = BASE_DIR / "index.faiss"
TEXT_DB_PATH = BASE_DIR / "palm_knowledge_ar.txt"

_index = None
_docs = []
_embed_model = None


def init_rag():
    """
    تحميل نموذج التع嵌ين + تحميل قاعدة البيانات + قراءة FAISS
    """
    global _index, _docs, _embed_model

    try:
        if not _embed_model:
            _embed_model = SentenceTransformer("all-MiniLM-L6-v2")

        if not PICKLE_PATH.exists() or not FAISS_PATH.exists():
            print("❌ RAG index missing")
            return

        with open(PICKLE_PATH, "rb") as f:
            data = pickle.load(f)
            _docs = data.get("docs", [])

        _index = faiss.read_index(str(FAISS_PATH))

        print(f"🟢 Loaded FAISS and {len(_docs)} chunks")

    except Exception as e:
        print(f"❌ RAG init failed: {e}")


def _embed_text(q: str):
    if not _embed_model:
        return None
    emb = _embed_model.encode([q])
    return np.array(emb).astype("float32")


def search_similar_chunks(question: str, top_k: int = 5, min_score: float = 0.35):
    """
    إرجاع أفضل المقاطع المتعلقة بالسؤال
    """
    global _index, _docs
    if _index is None or not _docs:
        return []

    question = question.strip()
    if not question:
        return []

    vec = _embed_text(question)
    if vec is None:
        return []

    k = min(top_k, len(_docs))
    scores, indices = _index.search(vec, k)

    results = []
    for idx, score in zip(indices[0], scores[0]):
        if idx < 0 or idx >= len(_docs):
            continue
        if score < min_score:
            continue
        results.append({"text": _docs[idx], "score": float(score)})

    return sorted(results, key=lambda x: x["score"], reverse=True)


def answer_with_rag(question: str) -> str:
    """
    إجابة جاهزة بالنقاط — تستخدم داخل chatbot لو حبيت
    """
    try:
        question_ar = GoogleTranslator(source="auto", target="ar").translate(question)
    except:
        question_ar = question

    hits = search_similar_chunks(question_ar, top_k=6, min_score=0.35)

    if not hits:
        return "لا تتوفر معلومات كافية للإجابة."

    bullets = "\n".join(f"- {h['text']}" for h in hits)
    return f"🔍 نقاط مرتبطة بسؤالك:\n{bullets}"


init_rag()
