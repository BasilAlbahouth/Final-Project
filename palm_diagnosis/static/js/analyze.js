// analyze.js
document.addEventListener("DOMContentLoaded", () => {

    /* =============================================================
       عناصر الواجهة
    ============================================================= */
    const cameraBtn = document.getElementById("cameraBtn");
    const uploadBtn = document.getElementById("uploadBtn");
    const cameraInput = document.getElementById("cameraInput");
    const fileInput = document.getElementById("fileInput");

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

    function getCsrfToken() {
        const match = document.cookie.match(/csrftoken=([^;]+)/i);
        return match ? match[1] : "";
    }

    function percent(value) {
        return `${Math.round(value * 100)}%`;
    }

    /* =============================================================
       مودال النتيجة
    ============================================================= */
    function buildResultModal() {
        const wrap = document.createElement("div");
        wrap.className = "result-modal";
        wrap.innerHTML = `
            <div class="result-dialog">
                <button class="result-close" aria-label="إغلاق">✕</button>
                <div id="resultContent">
                    <div class="modal-loading">
                        <span class="dot"></span><span class="dot"></span><span class="dot"></span>
                        <span>جاري التحليل…</span>
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(wrap);

        wrap.querySelector(".result-close").addEventListener("click", () => wrap.remove());
        wrap.addEventListener("click", (e) => { if (e.target === wrap) wrap.remove(); });

        return wrap;
    }

    function renderResultModal(wrap, imageURL, html) {
        wrap.querySelector("#resultContent").innerHTML = `
            <div class="result-grid">
                <div class="result-left">
                    <h3 class="res-title">الصورة المرفوعة</h3>
                    <div class="res-image"><img src="${imageURL}"></div>
                </div>
                <div class="result-right">${html}</div>
            </div>
        `;
    }

    /* =============================================================
       بطاقات النتيجة
    ============================================================= */

    function classTable(classes = []) {
        if (!classes.length) return `<div class="res-row">لا توجد بيانات</div>`;

        return classes
            .map((c, i) => `
                <div class="res-row ${i === 0 ? "primary" : ""}">
                    <span>${c.name}</span>
                    <span>${percent(c.confidence)}</span>
                </div>
            `)
            .join("");
    }

    function successCard(result) {
        return `
            <div class="res-card success">
                <div class="res-icon">🌴</div>
                <div class="res-heading">${result.predicted_class}</div>
                <p class="res-desc">تم التحليل باستخدام نموذج تعلّم عميق متخصص في تشخيص أمراض وآفات النخيل.</p>

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

    function errorCard(msg) {
        return `
            <div class="res-card danger">
                <div class="res-icon">⚠️</div>
                <div class="res-heading">فشل التحليل</div>
                <p class="res-desc">${msg}</p>
            </div>
        `;
    }

    /* =============================================================
       الطلب إلى الـ API
    ============================================================= */
async function uploadForAnalysis(file) {
    const formData = new FormData();
    formData.append("image", file);

    const response = await fetch("/api/analyze/", {
        method: "POST",
        body: formData,
        headers: {
            "X-CSRFToken": getCsrfToken()
        },
        credentials: "same-origin"
    });

    const json = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(json.error || "تعذر تحليل الصورة.");

    return json;
}

    /* =============================================================
       تشغيل التحليل
    ============================================================= */
    async function runAnalysis(file) {
        const modal = buildResultModal();
        const imageURL = await fileToDataURL(file);

        try {
            const result = await uploadForAnalysis(file);
            renderResultModal(modal, imageURL, successCard(result));
        } catch (err) {
            renderResultModal(modal, imageURL, errorCard(err.message));
        }
    }

    /* =============================================================
       الكاميرا
    ============================================================= */
    function buildCameraModal() {
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
        return modal;
    }

    function stopStream(stream) {
        stream?.getTracks().forEach(t => t.stop());
    }

    async function openCamera() {
        if (!navigator.mediaDevices?.getUserMedia) return cameraInput.click();

        const modal = buildCameraModal();
        const video = modal.querySelector("video");
        const closeBtn = modal.querySelector("[data-close]");
        const captureBtn = modal.querySelector("[data-capture]");

        let stream;
        try {
            stream = await navigator.mediaDevices.getUserMedia({
                video: { facingMode: "environment" }
            });
            video.srcObject = stream;
        } catch {
            modal.remove();
            return cameraInput.click();
        }

        function close() {
            stopStream(stream);
            modal.remove();
        }

        closeBtn.addEventListener("click", close);
        modal.addEventListener("click", e => { if (e.target === modal) close(); });

        captureBtn.addEventListener("click", () => {
            const canvas = document.createElement("canvas");
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            canvas.getContext("2d").drawImage(video, 0, 0);
            canvas.toBlob(blob => {
                runAnalysis(new File([blob], "camera.jpg"));
                close();
            }, "image/jpeg", 0.9);
        });
    }

    /* =============================================================
       الأحداث
    ============================================================= */
    cameraBtn?.addEventListener("click", e => { e.preventDefault(); openCamera(); });
    uploadBtn?.addEventListener("click", e => { e.preventDefault(); fileInput.click(); });
    cameraInput?.addEventListener("change", () => { if (cameraInput.files[0]) runAnalysis(cameraInput.files[0]); });
    fileInput?.addEventListener("change", () => { if (fileInput.files[0]) runAnalysis(fileInput.files[0]); });

});
