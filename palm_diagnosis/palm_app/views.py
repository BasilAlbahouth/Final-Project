import logging

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .ml import classify_image

logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'palm_app/index.html')

def test(request):
    return render(request, 'test123.html')

import os
print("DJANGO IS RUNNING FROM THIS PATH:", os.getcwd())


def analyze(request):
    return render(request, 'palm_app/analyze.html')


@require_POST
def analyze_api(request):
    """Accept an uploaded image and return model predictions as JSON."""
    image = request.FILES.get("image")  # ← نفس الاسم المرسل من JS
    if not image:
        return JsonResponse({"error": "يرجى اختيار صورة لتحليلها."}, status=400)

    try:
        result = classify_image(image)
    except FileNotFoundError as exc:
        logger.exception("Palm diagnosis model not found.")
        return JsonResponse({"error": str(exc)}, status=500)
    except Exception:
        logger.exception("Palm diagnosis inference failed.")
        return JsonResponse(
            {"error": "تعذر إتمام التحليل، حاول مرة أخرى."},
            status=500,
        )

    return JsonResponse(result)


