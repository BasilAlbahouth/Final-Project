import numpy as np
from PIL import Image
from django.http import JsonResponse
import tensorflow as tf
import os

# تحميل الموديل عند أول تشغيل (مرة واحدة)
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "date_palm_classifier_final (1).keras")
model = tf.keras.models.load_model(MODEL_PATH)

# الأصناف بالعربي
CLASSES_AR = {
    "CLASS_00_Healthy": "سليمة",
    "CLASS_03_Pest_Dubas_Symptom": "أعراض حشرة الدُبّاس",
    "CLASS_05_Disease_LeafSpot_Generic": "تبقّع الأوراق (عام)",
    "CLASS_01_Pest_WhiteScale": "الحشرة القشرية البيضاء",
    "CLASS_09_Deficiency_K": "نقص البوتاسيوم (K)",
    "CLASS_02_Pest_Dubas_Bug": "حشرة الدُبّاس",
    "CLASS_11_Deficiency_Mg": "نقص المغنيسيوم (Mg)",
    "CLASS_04_Disease_BrownSpot_Graphiola": "تبقّع بني (جرافيولا)",
    "CLASS_10_Deficiency_Mn": "نقص المنغنيز (Mn)",
    "CLASS_08_Disease_RachisBlight": "لفحة العرجون",
    "CLASS_07_Disease_FusariumWilt": "ذبول الفيوزاريوم",
    "CLASS_06_Disease_BlackScorch": "اللفحة السوداء"
}

CLASSES = list(CLASSES_AR.keys())

# def analyze_api(request):
#     if request.method != "POST":
#         return JsonResponse({"error": "POST only"}, status=400)

#     file = request.FILES.get("file")
#     if not file:
#         return JsonResponse({"error": "No file uploaded"}, status=400)

#     img = Image.open(file).resize((224, 224))
#     arr = np.array(img) / 255.0
#     arr = np.expand_dims(arr, axis=0)

#     preds = model.predict(arr)[0]
#     idx = int(np.argmax(preds))

#     class_en = CLASSES[idx]
#     class_ar = CLASSES_AR[class_en]
#     accuracy = float(preds[idx] * 100)

#     return JsonResponse({
#         "class_en": class_en,
#         "class_ar": class_ar,
#         "accuracy": accuracy
#     })
