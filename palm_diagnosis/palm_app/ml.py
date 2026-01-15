import numpy as np
from PIL import Image
import tensorflow as tf
import requests
import tempfile
import os
from django.conf import settings


# ===============================================================
# 1) تحميل موديل كاشف النخيل (FLOAT32 TFLite)
# ===============================================================

PALM_DETECTOR_PATH = os.path.join(settings.BASE_DIR, "models_tflite", "palm_detector_INT8.tflite")

palm_interpreter = tf.lite.Interpreter(model_path=PALM_DETECTOR_PATH)
palm_interpreter.allocate_tensors()
palm_input = palm_interpreter.get_input_details()
palm_output = palm_interpreter.get_output_details()


# ===============================================================
# 2) تحميل موديل التصنيف الرئيسي (FLOAT32 TFLite)
# ===============================================================

CLASSIFIER_PATH = os.path.join(settings.BASE_DIR, "models_tflite", "date_palm_classifier_final_INT8.tflite")

classifier_interpreter = tf.lite.Interpreter(model_path=CLASSIFIER_PATH)
classifier_interpreter.allocate_tensors()
classifier_input = classifier_interpreter.get_input_details()
classifier_output = classifier_interpreter.get_output_details()


# ===============================================================
# 3) تعريف الكلاسات (بدون تغيير)
# ===============================================================

CLASSES_EN = [
    "CLASS_00_Healthy",
    "CLASS_01_Pest_WhiteScale",
    "CLASS_02_Pest_Dubas_Bug",
    "CLASS_03_Pest_Dubas_Symptom",
    "CLASS_04_Disease_BrownSpot_Graphiola",
    "CLASS_05_Disease_LeafSpot_Generic",
    "CLASS_06_Disease_BlackScorch",
    "CLASS_07_Disease_FusariumWilt",
    "CLASS_08_Disease_RachisBlight",
    "CLASS_09_Deficiency_K",
    "CLASS_10_Deficiency_Mn",
    "CLASS_11_Deficiency_Mg",
]

CLASSES_AR = {
    "CLASS_00_Healthy": "سليمة",
    "CLASS_01_Pest_WhiteScale": "الحشرة القشرية البيضاء",
    "CLASS_02_Pest_Dubas_Bug": "حشرة الدُّبّاس",
    "CLASS_03_Pest_Dubas_Symptom": "أعراض حشرة الدُّبّاس",
    "CLASS_04_Disease_BrownSpot_Graphiola": "تبقّع بني (جرافيولا)",
    "CLASS_05_Disease_LeafSpot_Generic": "تبقّع الأوراق (عام)",
    "CLASS_06_Disease_BlackScorch": "اللفحة السوداء",
    "CLASS_07_Disease_FusariumWilt": "ذبول الفيوزاريوم",
    "CLASS_08_Disease_RachisBlight": "لفحة العرجون",
    "CLASS_09_Deficiency_K": "نقص البوتاسيوم",
    "CLASS_10_Deficiency_Mn": "نقص المنغنيز",
    "CLASS_11_Deficiency_Mg": "نقص المغنيسيوم",
}


# ===============================================================
# 4) دالة كشف النخيل — تعمل الآن بشكل صحيح
# ===============================================================

def is_palm_leaf(django_file):
    """يرجع True إذا كانت الصورة نخلة، False إذا لم تكن نخلة"""

    img = Image.open(django_file).convert("RGB").resize((224, 224))

    # الموديل يتطلب float32 وليس INT8 (حسب الخطأ)
    arr = np.array(img, dtype=np.float32) / 255.0
    arr = np.expand_dims(arr, axis=0)

    palm_interpreter.set_tensor(palm_input[0]["index"], arr)
    palm_interpreter.invoke()

    pred = palm_interpreter.get_tensor(palm_output[0]["index"])[0][0]

    print("Palm Detector Output:", pred)

    return pred >= 0.5



# ===============================================================
# 5) دالة التصنيف — نفس النظام القديم بدون تغيير
# ===============================================================

def classify_image(django_file):

    # 1) التحقق: هل الصورة نخلة؟
    if not is_palm_leaf(django_file):
        return {"not_palm": True}

    # 2) تحليل الأمراض
    img = Image.open(django_file).convert("RGB").resize((224, 224))

    # FLOAT32 input (مطلوب للموديل)
    arr = np.array(img, dtype=np.float32) / 255.0
    arr = np.expand_dims(arr, axis=0)

    classifier_interpreter.set_tensor(classifier_input[0]["index"], arr)
    classifier_interpreter.invoke()

    preds = classifier_interpreter.get_tensor(classifier_output[0]["index"])[0]

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
