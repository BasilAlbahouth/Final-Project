# palm_app/ml.py
import os
import numpy as np
from PIL import Image
import tensorflow as tf

# مسار الموديل
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "date_palm_classifier_final (1).keras")

# تحميل الموديل مرة واحدة
model = tf.keras.models.load_model(MODEL_PATH)

# نفس أسماء الكلاسات اللي تدرب عليها الموديل (بالإنجليزي)
CLASSES_EN = [
    "CLASS_00_Healthy",
    "CLASS_03_Pest_Dubas_Symptom",
    "CLASS_05_Disease_LeafSpot_Generic",
    "CLASS_01_Pest_WhiteScale",
    "CLASS_09_Deficiency_K",
    "CLASS_02_Pest_Dubas_Bug",
    "CLASS_11_Deficiency_Mg",
    "CLASS_04_Disease_BrownSpot_Graphiola",
    "CLASS_10_Deficiency_Mn",
    "CLASS_08_Disease_RachisBlight",
    "CLASS_07_Disease_FusariumWilt",
    "CLASS_06_Disease_BlackScorch",
]

# مقابلها بالعربي
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
    "CLASS_06_Disease_BlackScorch": "اللفحة السوداء",
}


def classify_image(django_file):
    """
    يستقبل ملف الصورة من Django، ويرجع:
    {
        "predicted_class": "نقص المنغنيز",
        "confidence": 0.13,
        "classes": [
            {"name": "نقص المنغنيز", "confidence": 0.13},
            {"name": "لفحة العرجون", "confidence": 0.10},
            ...
        ]
    }
    """
    # قراءة الصورة
    img = Image.open(django_file).convert("RGB").resize((224, 224))
    arr = np.array(img, dtype=np.float32) / 255.0
    arr = np.expand_dims(arr, axis=0)

    # تنبؤ الموديل
    preds = model.predict(arr)[0]  # شكلها (عدد_الكلاسات,)

    # ترتيب من الأعلى إلى الأقل
    sorted_idx = np.argsort(preds)[::-1]
    top_idx = int(sorted_idx[0])

    top_class_en = CLASSES_EN[top_idx]
    top_class_ar = CLASSES_AR[top_class_en]
    top_confidence = float(preds[top_idx])

    classes_list = []
    for idx in sorted_idx:
        class_en = CLASSES_EN[int(idx)]
        classes_list.append({
            "name": CLASSES_AR[class_en],
            "confidence": float(preds[idx]),
        })

    return {
        "predicted_class": top_class_ar,
        "confidence": top_confidence,
        "classes": classes_list,
    }
