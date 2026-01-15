// analyze.js
document.addEventListener("DOMContentLoaded", () => {

/* =============================================================
   عناصر الواجهة
============================================================= */

const cameraBtn = document.getElementById("cameraBtn");
const uploadBtn = document.getElementById("uploadBtn");
const cameraInput = document.getElementById("cameraInput");
const fileInput = document.getElementById("fileInput");

const openExamples = document.getElementById("openExamples");
const examplesModal = document.getElementById("examplesModal");
const closeExamples = document.querySelector(".close-examples");

/* =============================================================
   مودال الأمثلة
============================================================= */

if (openExamples) openExamples.onclick = () => examplesModal.style.display = "block";
if (closeExamples) closeExamples.onclick = () => examplesModal.style.display = "none";

window.onclick = (e) => {
    if (e.target === examplesModal) examplesModal.style.display = "none";
};

/* =============================================================
   معلومات التشخيص
============================================================= */

const DISEASE_INFO = {
    "سليمة": {
        title: "النخلة سليمة",
        description: "لا توجد أعراض مرضية ظاهرة على السعف."
    },

    "أعراض حشرة الدُّبّاس": {
        title: "أعراض حشرة الدُّبّاس",
        description: "بقع باهتة مع إفرازات الندوة العسلية، وقد يظهر العفن الأسود."
    },

    "حشرة الدُّبّاس": {
        title: "حشرة الدُّبّاس",
        description: "حشرة ماصّة تتغذى على العصارة وتسبب تغير لون السعف."
    },

    "الحشرة القشرية البيضاء": {
        title: "الحشرة القشرية البيضاء",
        description: "نقاط بيضاء صغيرة تلتصق بالسعف وتضعف عملية التمثيل الضوئي."
    },

    "تبقّع بني (جرافيولا)": {
        title: "تبقّع بني (جرافيولا)",
        description: "بقع بنية أو سوداء تنتشر على السعف نتيجة عدوى فطرية."
    },

    "اللفحة السوداء": {
        title: "اللفحة السوداء",
        description: "بقع سوداء تحترق فيها أجزاء من السعف، غالباً بسبب فطر Diplodia."
    },

    "ذبول الفيوزاريوم": {
        title: "ذبول الفيوزاريوم",
        description: "اصفرار نصف السعف وانحناؤه للأسفل بسبب انسداد الأوعية الناقلة."
    },

    "نقص البوتاسيوم": {
        title: "نقص البوتاسيوم (K)",
        description: "احتراق أطراف الوريقات بشكل متدرج من الخارج للداخل."
    },

    "نقص المغنيسيوم": {
        title: "نقص المغنيسيوم (Mg)",
        description: "اصفرار بين العروق مع بقاء الورقة خضراء نسبياً."
    },

    "نقص المنغنيز": {
        title: "نقص المنغنيز (Mn)",
        description: "اصفرار في السعف الجديد مع بقع ميتة بين العروق."
    }
};

/* =============================================================
   أدوات عامة
============================================================= */

function fileToDataURL(file) {
    return new Promise((resolve, reject) => {
        const r = new FileReader();
        r.onload = () => resolve(r.result);
        r.onerror = reject;
        r.readAsDataURL(file);
    });
}

function percent(v) {
    return `${Math.round(v * 100)}%`;
}

function getCsrfToken() {
    const match = document.cookie.match(/csrftoken=([^;]+)/i);
    return match ? match[1] : "";
}

/* =============================================================
   مودال نتيجة التحليل
============================================================= */

function buildResultModal() {
    const modal = document.createElement("div");
    modal.className = "result-modal";

    modal.innerHTML = `
        <div class="result-dialog">
            <button class="result-close">✕</button>
            <div id="resultContent">
                <div class="modal-loading">
                    <span class="dot"></span><span class="dot"></span><span class="dot"></span>
                    <span>جاري التحليل…</span>
                </div>
            </div>
        </div>
    `;

    document.body.appendChild(modal);

    modal.querySelector(".result-close").onclick = () => modal.remove();
    modal.onclick = (e) => { if (e.target === modal) modal.remove(); };

    return modal;
}

function renderResultModal(modal, imgURL, html) {
        modal.querySelector("#resultContent").innerHTML = `
            <div class="result-grid" style="position: relative; display: flex; flex-direction: row-reverse; gap: 20px;">
                <div class="result-left" style="flex: 1;">
                    <h3 class="res-title">الصورة المرفوعة</h3>
                    <div class="res-image"><img src="${imgURL}" style="width:100%; border-radius:15px;"></div>
                </div>

                <div class="result-right" style="flex: 1;">
                    ${html}
                </div>
                
                <button id="mainSaveBtn" class="floating-save-btn" style="display: none;" title="حفظ النتيجة">💾</button>                
                <div id="savePopup" class="save-popup">
                    <h5>حفظ في السجل</h5>
                    <select id="palmSelectResult" class="form-select">
                        <option value="">-- اختر النخلة --</option>
                        <option value="new">+ إضافة نخلة جديدة</option>
                        </select>
                    
                    <div id="newPalmInput" style="display:none;">
                        <input type="text" id="newPalmName" class="form-control" placeholder="اكتب اسم النخلة الجديدة">
                    </div>
                    
                    <button class="btn btn-success btn-sm w-100 mt-2" id="confirmSaveBtn">تأكيد الحفظ</button>
                </div>
            </div>
        `;

        // تفعيل الأحداث داخل المودال بعد بنائه
        setupSaveLogic();
    }

window.toggleSavePopup = function() {
    // 1. التحقق من حالة تسجيل الدخول
    if (typeof isUserAuthenticated === 'undefined' || !isUserAuthenticated) {
        // إذا لم يسجل دخول، نظهر رسالة تنبيه بدلاً من النافذة
        showLoginAlert();
        return;
    }

    // 2. إذا سجل دخول، نفتح النافذة كالمعتاد
    const popup = document.getElementById("savePopup");
    if (popup) {
        popup.style.display = (popup.style.display === "block") ? "none" : "block";
    }
};

// دالة إظهار رسالة التنبيه (Alert)
function showLoginAlert() {
    const confirmLogin = confirm("⚠️ عذراً، يجب عليك تسجيل الدخول أولاً لتتمكن من حفظ النتائج في سجلك.\n\nهل تريد الانتقال إلى صفحة تسجيل الدخول الآن؟");
    if (confirmLogin) {
        // الانتقال لصفحة تسجيل الدخول (تأكد من صحة الرابط حسب مشروعك)
        window.location.href = "/accounts/login/"; 
    }
}

function setupSaveLogic() {
    const saveBtn = document.getElementById("mainSaveBtn");
    const popup = document.getElementById("savePopup");
    const select = document.getElementById("palmSelectResult");
    const newPalmInput = document.getElementById("newPalmInput");
    const confirmBtn = document.getElementById("confirmSaveBtn");

    // عند الضغط على زر الحفظ العائم 💾
    saveBtn.onclick = (e) => {
        e.stopPropagation();

        // الحارس (Guard): تحقق هل المستخدم مسجل دخول؟
        if (!isUserAuthenticated) {
            // رسالة تنبيهية تظهر في الواجهة
            showAuthAlert();
            return; // توقف هنا ولا تفتح النافذة
        }
    if (confirmBtn) {
        confirmBtn.onclick = function(e) {
            e.stopPropagation();
            
            // جلب اسم المرض المكتوب في النتيجة
            const labelText = document.querySelector(".res-heading").innerText;
            // جلب نسبة الثقة (اختياري، سنرسل 1.0 كافتراضي)
            
            window.confirmFinalSave(labelText, 0.95); 
        };
    }

        // إذا كان مسجل، افتح نافذة الحفظ كالمعتاد
        popup.style.display = (popup.style.display === "block") ? "none" : "block";
    };

    // دالة إظهار التنبيه للمستخدم غير المسجل
    function showAuthAlert() {
        const overlay = document.createElement("div");
        overlay.style = "position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.8); z-index:9999; display:flex; align-items:center; justify-content:center;";
        
        overlay.innerHTML = `
            <div style="background:white; padding:30px; border-radius:20px; text-align:center; max-width:400px; border: 2px solid #27ae60;">
                <h3 style="color:#2c3e50; margin-bottom:15px;">🔒 ميزة للمسجلين فقط</h3>
                <p style="color:#7f8c8d; margin-bottom:20px;">يجب عليك تسجيل الدخول لتتمكن من حفظ نتائج التشخيص وربطها بنخيلك.</p>
                <div style="display:flex; gap:10px; justify-content:center;">
                    <button onclick="this.parentElement.parentElement.parentElement.remove()" style="padding:10px 20px; border-radius:10px; border:1px solid #ddd; background:none; cursor:pointer;">إلغاء</button>
                    <a href="/accounts/login/" style="padding:10px 20px; border-radius:10px; background:#27ae60; color:white; text-decoration:none; font-weight:bold;">تسجيل الدخول الآن</a>
                </div>
            </div>
        `;
        document.body.appendChild(overlay);
    }

    // إظهار حقل النخلة الجديدة عند اختيار "إضافة نخلة جديدة"
    select.onchange = () => {
        newPalmInput.style.display = (select.value === "new") ? "block" : "none";
    };

    // تنفيذ عملية الحفظ الفعلية (تأكيد الحفظ)
    confirmBtn.onclick = async () => {
        // ... كود الإرسال للسيرفر (Save API) ...
    };
}

/* =============================================================
   بطاقات النتيجة
============================================================= */

function classTable(classes) {
    return classes.map((c, i) => `
        <div class="res-row ${i === 0 ? "primary" : ""}">
            <span>${c.name}</span>
            <span>${percent(c.confidence)}</span>
        </div>
    `).join("");
}

function successCard(result) {
    const info = DISEASE_INFO[result.predicted_class];

    return `
        <div class="res-card success">
            <div class="res-icon">🌴</div>
            <div class="res-heading">${info?.title || result.predicted_class}</div>
            <p class="res-desc">${info?.description || "لا يوجد وصف متاح."}</p>

            <div class="res-accuracy">
                <div class="res-acc-head">
                    <span>درجة الثقة</span>
                    <span>${percent(result.confidence)}</span>
                </div>
                <div class="res-bar"><span class="res-fill" style="width:${percent(result.confidence)}"></span></div>
            </div>

            <div class="res-table">
                <div class="res-table-head"><span>الفئة</span><span>الثقة</span></div>
                ${classTable(result.classes)}
            </div>
        </div>
    `;
}


window.saveToHistory = async function(label, confidence) {
    const palmId = document.getElementById("palmSelectResult").value;
    const newPalmName = document.getElementById("newPalmName").value;
    
    const bodyData = {
        label: label,
        confidence: confidence,
        palm_id: palmId === "new" ? null : palmId,
        new_palm_name: palmId === "new" ? newPalmName : null
    };

    try {
        const res = await fetch("/api/save-diagnosis/", {
            method: "POST",
            headers: { 
                "Content-Type": "application/json",
                "X-CSRFToken": getCsrfToken() 
            },
            body: JSON.stringify(bodyData)
        });
        
        const data = await res.json();
        if (data.success) {
            alert("تم الحفظ بنجاح! يمكنك رؤيتها في سجل التشخيصات.");
        } else {
            alert("عذراً، يجب تسجيل الدخول أولاً لحفظ النتائج.");
        }
    } catch (err) {
        alert("حدث خطأ أثناء الحفظ.");
    }
};

// مراقبة اختيار "نخلة جديدة" لإظهار حقل الاسم
document.addEventListener('change', function(e){
    if(e.target && e.target.id == 'palmSelectResult'){
        const inputDiv = document.getElementById("newPalmInput");
        inputDiv.style.display = (e.target.value === "new") ? "block" : "none";
    }
});

function notPalmCard() {
    return `
        <div class="res-card danger">
            <div class="res-icon">🌴❌</div>
            <div class="res-heading">الصورة ليست نخلة</div>
            <p class="res-desc">الرجاء رفع صورة سعف نخيل واضحة.</p>
            <div class="retry-box">
                <button class="retry-btn" onclick="retryCamera()">إعادة التصوير 📷</button>
                <button class="retry-btn" onclick="retryUpload()">إعادة رفع صورة 📁</button>
            </div>
        </div>
    `;
}

function errorCard(msg) {
    return `
        <div class="res-card danger">
            <div class="res-icon">⚠️</div>
            <div class="res-heading">خطأ في التحليل</div>
            <p class="res-desc">${msg}</p>
            <div class="retry-box">
                <button class="retry-btn" onclick="retryCamera()">إعادة التصوير 📷</button>
                <button class="retry-btn" onclick="retryUpload()">إعادة رفع صورة 📁</button>
            </div>
        </div>
    `;
}

/* =============================================================
   تنظيف قبل التحليل
============================================================= */

function cleanAll() {
    document.querySelector(".result-modal")?.remove();
    fileInput.value = "";
    cameraInput.value = "";

    fileInput.type = "text"; fileInput.type = "file";
    cameraInput.type = "text"; cameraInput.type = "file";
}

/* =============================================================
   رفع الصورة للباك-إند
============================================================= */

async function uploadForAnalysis(file) {
    const fd = new FormData();
    fd.append("image", file);

    const res = await fetch("/api/analyze/", {
        method: "POST",
        headers: { "X-CSRFToken": getCsrfToken() },
        body: fd
    });

    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(data.error || "تعذر التحليل.");
    return data;
}

/* =============================================================
   تشغيل التحليل
============================================================= */

async function runAnalysis(file) {
    cleanAll();
    const modal = buildResultModal();
    const imgURL = await fileToDataURL(file);

    try {
        const result = await uploadForAnalysis(file);

        if (result.not_palm) {
            renderResultModal(modal, imgURL, notPalmCard());
            // لا نحتاج لكود إخفاء هنا لأن الزر افتراضياً مخفي في renderResultModal
            return;
        }
        
        // أولاً: نعرض محتوى النجاح
        renderResultModal(modal, imgURL, successCard(result));

        // ثانياً: الآن الزر موجود في الصفحة، يمكننا إظهاره
        const saveBtn = document.getElementById("mainSaveBtn");
        if (saveBtn) {
            saveBtn.style.display = "flex"; // إظهار الزر الآن
        }

    } catch (err) {
        renderResultModal(modal, imgURL, errorCard(err.message));
        // الزر سيبقى مخفياً تلقائياً
    }
}

/* =============================================================
   الكاميرا
============================================================= */

async function openCamera() {
    if (!navigator.mediaDevices) return cameraInput.click();

    const modal = document.createElement("div");
    modal.className = "cam-modal";

    modal.innerHTML = `
        <div class="cam-dialog">
            <video autoplay muted playsinline></video>
            <div class="cam-actions">
                <button class="cam-btn" data-close>إلغاء</button>
                <button class="cam-btn primary" data-capture>التقاط</button>
            </div>
        </div>
    `;

    document.body.appendChild(modal);
    const video = modal.querySelector("video");

    const stream = await navigator.mediaDevices.getUserMedia({ video: true }).catch(() => null);
    if (!stream) return cameraInput.click();

    video.srcObject = stream;

    modal.querySelector("[data-close]").onclick = () => {
        stream.getTracks().forEach(t => t.stop());
        modal.remove();
    };

    modal.querySelector("[data-capture]").onclick = () => {
        const canvas = document.createElement("canvas");
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.getContext("2d").drawImage(video, 0, 0);

        canvas.toBlob(b => runAnalysis(new File([b], "camera.jpg")), "image/jpeg");
        stream.getTracks().forEach(t => t.stop());
        modal.remove();
    };
}

/* =============================================================
   إعادة رفع / إعادة التصوير
============================================================= */

window.retryUpload = function () {
    cleanAll();
    fileInput.click();
};

window.retryCamera = function () {
    cleanAll();
    openCamera();
};


// /* ===========================
//    عناصر الشات
// =========================== */
// const chatBtn = document.getElementById("openChatbot");
// const chatPanel = document.getElementById("chatbotPanel");
// const chatClose = document.getElementById("closeChatbot");

// const chatForm = document.getElementById("chatbotForm");
// const chatInput = document.getElementById("chatbotText");
// const chatMessages = document.getElementById("chatbotMessages");


// /* ===========================
//    فتح / إغلاق الشات
// =========================== */
// chatBtn?.addEventListener("click", () => {
//     chatPanel.classList.add("open");
// });

// chatClose?.addEventListener("click", () => {
//     chatPanel.classList.remove("open");
// });

// chatPanel?.addEventListener("click", (e) => {
//     if (e.target === chatPanel) {
//         chatPanel.classList.remove("open");
//     }
// });


// /* ===========================
//    إضافة رسالة
// =========================== */
// function addMessage(text, sender = "user") {
//     const div = document.createElement("div");
//     div.className = `chat-msg ${sender}`;
//     div.innerHTML = `<div class="msg-bubble">${text}</div>`;
//     chatMessages.appendChild(div);
//     chatMessages.scrollTop = chatMessages.scrollHeight;
// }


// /* ===========================
//    إرسال السؤال للـ API
// =========================== */
// chatForm.addEventListener("submit", async (e) => {
//     e.preventDefault();

//     const text = chatInput.value.trim();
//     if (!text) return;

//     // رسالة المستخدم
//     addMessage(text, "user");
//     chatInput.value = "";

//     // رسالة انتظار
//     addMessage("⏳ جاري التحليل...", "bot");

//     try {
//         const res = await fetch("/api/chatbot/", {
//             method: "POST",
//             headers: {
//                 "Content-Type": "application/json",
//                 "X-CSRFToken": getCsrfToken()
//             },
//             body: JSON.stringify({ message: text })
//         });

//         const data = await res.json();
//         // حذف رسالة الانتظار
//         // حذف رسالة الانتظار
//         chatMessages.lastChild.remove();

//         // هل عندنا رد من الخادم؟
//         if (data.answer) {
//             addMessage(data.answer, "bot");
//         } else if (data.error) {
//             addMessage(`❌ خطأ: ${data.error}`, "bot");
//         } else {
//             addMessage("⚠️ لم يتم استلام رد واضح من المساعد.", "bot");
//         }

//     } catch (err) {
//         console.error(err);
//         chatMessages.lastChild.remove();
//         addMessage("❌ حدث خطأ أثناء الاتصال بالمساعد.", "bot");
//     }
// });

// دالة لجلب رمز الحماية من الكوكيز (ضروري جداً للجانجو)
function getCsrfToken() {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, 10) === 'csrftoken=') {
                cookieValue = decodeURIComponent(cookie.substring(10));
                break;
            }
        }
    }
    return cookieValue;
}

// دالة تأكيد الحفظ التي يتم استدعاؤها من الزر
window.confirmFinalSave = async function(label, confidence) {
    const palmSelect = document.getElementById("palmSelectResult");
    const newPalmInput = document.getElementById("newPalmName");
    const popup = document.getElementById("savePopup");
    
    if (!palmSelect) return;

    const palmId = palmSelect.value;
    const newPalmNameValue = newPalmInput ? newPalmInput.value : "";

    if (!palmId && !newPalmNameValue) {
        alert("⚠️ يرجى اختيار نخلة أو إدخال اسم نخلة جديدة.");
        return;
    }

    const bodyData = {
        label: label,
        confidence: confidence,
        palm_id: palmId === "new" ? null : palmId,
        new_palm_name: palmId === "new" ? newPalmNameValue : null
    };

    try {
        const response = await fetch("/api/save-diagnosis/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCsrfToken()
            },
            body: JSON.stringify(bodyData)
        });

        const data = await response.json();

        if (data.success) {
            // إخفاء نافذة الحفظ أولاً
            if (popup) popup.style.display = "none";
            
            // إظهار رسالة النجاح بشكل مؤكد
            setTimeout(() => {
                alert("✅ تم الحفظ بنجاح! يمكنك مراجعة السجل الآن.");
            }, 100); 
            
        } else {
            alert("❌ فشل الحفظ: " + (data.error || "خطأ غير معروف"));
        }
    } catch (error) {
        alert("❌ حدث خطأ فني، يرجى التأكد من اتصال الإنترنت.");
    }
};
/* =============================================================
   الأحداث
============================================================= */

cameraBtn.onclick = () => openCamera();
uploadBtn.onclick = () => fileInput.click();
fileInput.onchange = () => fileInput.files[0] && runAnalysis(fileInput.files[0]);
cameraInput.onchange = () => cameraInput.files[0] && runAnalysis(cameraInput.files[0]);

});
