document.querySelectorAll(".btn-delete").forEach(btn => {
    btn.addEventListener("click", () => {
        if (confirm("هل أنت متأكد من حذف هذا التشخيص؟")) {
            // fetch delete api لاحقاً
        }
    });
});
