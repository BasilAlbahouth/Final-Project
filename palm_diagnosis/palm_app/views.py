import os
import json
import logging
from .ml import classify_image
from google.genai import Client
from django.utils import timezone
from django.urls import reverse_lazy
from django.http import JsonResponse
from .models import Diagnosis, PalmTree
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required


logger = logging.getLogger(__name__)
client = Client(api_key="AIzaSyBYlR8UIjLIaJnRjPlyfjkrb-0I9F2rXq0")


print("DJANGO IS RUNNING FROM THIS PATH:", os.getcwd())

def analyze(request):
    """عرض صفحة التحليل مع جلب نخيل المستخدم إذا كان مسجلاً"""
    context = {}
    if request.user.is_authenticated:
        # جلب نخيل المستخدم فقط لربط الفحص بها
        context['user_palms'] = PalmTree.objects.filter(owner=request.user)
    
    return render(request, 'palm_app/analyze.html', context)


@require_POST
@csrf_exempt  # مؤقتاً للتجربة، والأفضل استخدامه مع Token
def analyze_api(request):
    image = request.FILES.get("image")
    palm_id = request.POST.get("palm_id")

    if not image:
        return JsonResponse({"error": "يرجى اختيار صورة لتحليلها."}, status=400)

    try:
        # 1. التحليل متاح للكل (سواء مسجل أو لا)
        result = classify_image(image)

        if result.get("not_palm"):
            return JsonResponse({"error": "❌ الصورة ليست لنخلة واضحة."}, status=400)

        # 2. منطق الحفظ الذكي: فقط إذا كان مسجل دخول
        if request.user.is_authenticated:
            palm_obj = None
            if palm_id:
                palm_obj = PalmTree.objects.filter(id=palm_id, owner=request.user).first()

            Diagnosis.objects.create(
                user=request.user,
                palm=palm_obj,
                image=image,
                result_label=result.get("predicted_class"),
                confidence_score=result.get("confidence")
            )
            # إضافة رسالة للرد تفيد بأنه تم الحفظ
            result["saved"] = True 
        else:
            # إذا مو مسجل، نرسل له تنبيه بسيط مع النتيجة
            result["saved"] = False
            result["message"] = "سجل دخولك لحفظ نتائج هذا الفحص مستقبلاً."

        return JsonResponse(result)

    except Exception as e:
        return JsonResponse({"error": "حدث خطأ أثناء التحليل."}, status=500)


from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
import json

@login_required
@require_POST
def save_diagnosis_api(request):
    try:
        data = json.loads(request.body)

        label = data.get("label")
        confidence = data.get("confidence")
        if confidence <= 1:
            confidence = round(confidence * 100, 2)
        palm_id = data.get("palm_id")
        palm_name = data.get("new_palm_name", "").strip()

        # ===== اختيار نخلة موجودة =====
        if palm_id:
            palm = PalmTree.objects.get(id=palm_id, owner=request.user)

        # ===== إنشاء نخلة جديدة =====
        else:
            if not palm_name:
                count = PalmTree.objects.filter(owner=request.user).count() + 1
                palm_name = f"نخلة رقم {count}"

            unique_name = palm_name
            counter = 1
            while PalmTree.objects.filter(owner=request.user, name=unique_name).exists():
                unique_name = f"{palm_name} ({counter})"
                counter += 1

            palm = PalmTree.objects.create(
                owner=request.user,
                name=unique_name
            )

        # ===== حفظ التشخيص =====
        Diagnosis.objects.create(
            user=request.user,
            palm=palm,
            result_label=label,
            confidence_score=confidence
        )

        # ✅ مهم جدًا
        return JsonResponse({
            "success": True,
            "palm_name": palm.name
        })

    except Exception as e:
        print("SAVE_DIAGNOSIS_ERROR:", e)
        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=500)




def home(request):
    examples = [
        {
            "title": "سعف سليم",
            "desc": "لون طبيعي بدون إصابات.",
            "img": "images/examples/healthy.jpg"
        },
        {
            "title": "بقعة سوداء",
            "desc": "خطوط وبقع سوداء كأنها محترقة...",
            "img": "images/examples/black_scorch.png"
        },
        {
            "title": "سوسة الدوباس",
            "desc": "حشرة ماصّة تغطي السعف بندوة عسلية...",
            "img": "images/examples/dubas_bug.JPG"
        },
        {
            "title": "أعراض حشرة الدوباس",
            "desc": "بقع باهتة مع عفن أسود (سخامي)...",
            "img": "images/examples/dubas_symptom.jpg"
        },
        {
            "title": "ذبول الفيوزاريوم",
            "desc": "اصفرار وذبول نصف تاج النخلة...",
            "img": "images/examples/fusarium_wilt.png"
        },
        {
            "title": "بقعة ورقية",
            "desc": "بقع بنية أو رمادية على الخوص...",
            "img": "images/examples/leaf_spot.png"
        },
        {
            "title": "بقع بنية",
            "desc": "بقع صفراء صغيرة تتحول لبقع بنية...",
            "img": "images/examples/brown_spot.jpg"
        },
        {
            "title": "لفحة العذق",
            "desc": "اسوداد وجفاف مفاجئ في العرجون...",
            "img": "images/examples/rachis_blight.png"
        },
        {
            "title": "نقص البوتاسيوم",
            "desc": "اصفرار وجفاف تدريجي لأطراف الوريقات...",
            "img": "images/examples/potassium.png"
        },
        {
            "title": "نقص الماغنيسيوم",
            "desc": "اصفرار ناتج عن نقص عنصر الماغنيسيوم...",
            "img": "images/examples/magnesium.png"
        },
        {
            "title": "نقص المنغنيز",
            "desc": "تلون غير طبيعي بسبب نقص المنغنيز...",
            "img": "images/examples/manganese.png"
        },
        {
            "title": "الحشرة القشرية البيضاء",
            "desc": "حراشف بيضاء صغيرة تمتص العصارة...",
            "img": "images/examples/white_scale.jpg"
        },
    ]

    return render(
        request,
        "palm_app/home.html",   # إذا تيمبلت داخل templates/palm_app
        {"examples": examples}
    )

def chatbot_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=400)

    body = json.loads(request.body)
    question = body.get("message", "")

    if not question:
        return JsonResponse({"error": "No message sent"}, status=400)

    # Run Gemini
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=question,
    )

    text = response.text.strip()

    return JsonResponse({"answer": text})

def chatbot(request):
    return render(request, "palm_app/chatbot.html")

@login_required
def profile(request):
    user = request.user
    diagnoses = Diagnosis.objects.filter(user=user)

    total_diagnoses = diagnoses.count()
    total_images = diagnoses.exclude(image="").count()

    last_diagnosis = diagnoses.order_by("-created_at").first()
    days_since_last = None

    if last_diagnosis:
        days_since_last = (timezone.now() - last_diagnosis.created_at).days

    healthy_count = diagnoses.filter(result_label__icontains="سليمة").count()
    healthy_percent = (
        round((healthy_count / total_diagnoses) * 100)
        if total_diagnoses > 0 else 0
    )

    context = {
        "total_diagnoses": total_diagnoses,
        "total_images": total_images,
        "days_since_last": days_since_last,
        "healthy_percent": healthy_percent,
    }

    return render(request, "palm_app/profile.html", context)


@login_required
@login_required
def history(request):
    diagnoses = Diagnosis.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "palm_app/history.html", {"diagnoses": diagnoses})

# palm_app/views.py

@login_required
def my_palms(request):
    # تغيير Palm إلى PalmTree وتغيير user إلى owner
    palms = PalmTree.objects.filter(owner=request.user).order_by('-created_at')
    return render(request, 'palm_app/my_palms.html', {'palms': palms})

@login_required
def palm_detail(request, palm_id):
    palm = PalmTree.objects.get(id=palm_id, owner=request.user)
    diagnoses = Diagnosis.objects.filter(palm=palm).order_by("-created_at")

    return render(request, "palm_app/palm_detail.html", {
        "palm": palm,
        "diagnoses": diagnoses
    })


@login_required
@require_POST
def add_palm_api(request):
    import json
    data = json.loads(request.body)

    palm = PalmTree.objects.create(
        owner=request.user,
        name=data["name"],
        location_lat=data["lat"],
        location_lng=data["lng"]
    )

    return JsonResponse({"success": True, "id": palm.id})

@login_required
def upload_avatar(request):
    if request.method == "POST" and request.FILES.get("avatar"):
        profile = request.user.profile
        profile.avatar = request.FILES["avatar"]
        profile.save()
    return redirect("profile")

@login_required
def edit_profile(request):
    if request.method == "POST":
        user = request.user
        profile = user.profile

        user.first_name = request.POST.get("first_name", "")
        user.last_name = request.POST.get("last_name", "")
        profile.phone = request.POST.get("phone", "")
        profile.location = request.POST.get("location", "")

        user.save()
        profile.save()

    return redirect("profile")
