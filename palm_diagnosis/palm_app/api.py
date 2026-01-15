from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.decorators.http import require_POST
from .ml import classify_image
from palm_app.chatbot.chatbot_engine import answer_question
from palm_app.rag_db.rag_engine import search_similar_chunks
import os

from google.genai import Client
from django.conf import settings
client = Client(api_key=settings.GEMINI_API_KEY)

@csrf_exempt
def analyze_image(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    image = request.FILES.get("image")
    if not image:
        return JsonResponse({"error": "يرجى رفع صورة"}, status=400)

    try:
        result = classify_image(image)

        if result.get("not_palm"):
            return JsonResponse({"not_palm": True})

        return JsonResponse(result)

    except Exception:
        return JsonResponse({"error": "حدث خطأ أثناء التحليل"}, status=500)

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
KNOWLEDGE_FILE = os.path.join(BASE_PATH, "rag_db", "palm_knowledge_ar.txt")

with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
    KNOWLEDGE_TEXT = f.read()

@csrf_exempt
@require_POST
def chatbot_api(request):
    """
    Endpoint للـ Chatbot:
    - يستقبل message
    - يستدعي answer_question من محرك الـ Chatbot
    - يرجع JSON فيه answer
    """
    try:
        body = json.loads(request.body.decode("utf-8"))
        question = (body.get("message") or "").strip()

        if not question:
            return JsonResponse({"error": "Empty message"}, status=400)

        # هنا كل الشغل الذكي صار داخل answer_question
        answer = answer_question(question)

        return JsonResponse({"answer": answer})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
