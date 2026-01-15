# palm_app/chatbot/chatbot_engine.py

from django.conf import settings
from google.genai import Client

from palm_app.rag_db.rag_engine import search_similar_chunks

# عميل Gemini – يُستخدم مرة واحدة فقط
client = Client(api_key=settings.GEMINI_API_KEY)


def answer_question(question, context=None):
    """
    دالة رئيسية للـ Chatbot:
    - تأخذ سؤال المستخدم (إجباري)
    - context (اختياري) من تحليل الصورة مثلاً
    - تستخدم RAG + Gemini بنمط Hybrid
    """

    # حماية من القيم الفارغة
    question = (question or "").strip()
    if not question:
        return "لم يتم استلام أي سؤال بعد. حاول أن تكتب سؤالك عن النخيل أو الزراعة بشكل واضح."

    # 1) استرجاع أفضل المقاطع من قاعدة المعرفة (RAG)
    try:
        hits = search_similar_chunks(question, top_k=5, min_score=0.35)
    except Exception:
        hits = []

    have_knowledge = bool(hits)
    if have_knowledge:
        knowledge_text = "\n".join(f"- {h['text']}" for h in hits)
    else:
        knowledge_text = "لا توجد مقاطع عالية التطابق من قاعدة المعرفة لهذا السؤال."

    # 2) دمج أي سياق إضافي من تحليل الصورة (إن وُجد)
    image_context_str = ""
    if isinstance(context, dict):
        pred = context.get("predicted_class") or context.get("label")
        if pred:
            image_context_str = (
                f"\nمعلومة إضافية: نتيجة تحليل الصورة تشير إلى الحالة/الفئة التالية للنخلة: «{pred}»."
            )

    # 3) بناء الـ Prompt بنمط Hybrid + فصحى مبسّطة + ٥ أسطر تقريبًا
    prompt = f"""
أنت مساعد ذكي ومتخصص في النخيل وأمراضه ورعايته. تجيب دائمًا بالعربية الفصحى المبسّطة.

أولوية الإجابة تكون اعتمادًا على قاعدة المعرفة التالية (إن وُجدت مقاطع مناسبة):

المعرفة المتاحة:
{knowledge_text}
{image_context_str}

سؤال المستخدم:
{question}

طريقة الإجابة (نمط هجين Hybrid):
- أولًا، حاول أن تبني الإجابة قدر الإمكان على النصوص الموجودة في قاعدة المعرفة أعلاه.
- إذا كانت النصوص تغطي جزءًا من الجواب فقط، يمكنك إكمال الشرح من خبرتك العامة بطريقة مبسّطة، مع تجنّب التفاصيل الطبية أو الكيميائية الدقيقة.
- إذا لم تجد في النصوص ما يساعد تقريبًا، اذكر للمستخدم أن المعلومات في قاعدة المعرفة غير كافية، ثم قدّم إرشادات عامة بسيطة إن أمكن.
- اجعل الإجابة بين ٤ و٦ أسطر، بلغة واضحة ومباشرة ومفهومة للمزارع.
"""

    try:
        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=prompt,
        )
        answer = getattr(response, "text", "").strip()
    except Exception:
        answer = ""

    # 4) حالات الـ fallback
    if not answer:
        if have_knowledge:
            return (
                "تم العثور على بعض المعلومات في قاعدة المعرفة، "
                "لكن تعذّر توليد إجابة في هذه اللحظة. حاول إعادة صياغة سؤالك أو تبسيطه."
            )
        else:
            return (
                "لا تتوفر حاليًا معلومات كافية في قاعدة المعرفة للإجابة عن هذا السؤال. "
                "حاول أن تغيّر طريقة طرح السؤال أو تسأل عن جانب آخر من العناية بالنخيل."
            )

    return answer
