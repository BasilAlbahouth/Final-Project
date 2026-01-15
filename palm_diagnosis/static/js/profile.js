function addClickEffect(buttonId) {
    const btn = document.getElementById(buttonId);
    if (!btn) return;

    btn.addEventListener("mousedown", () => {
        btn.style.transform = "scale(0.96)";
    });

    btn.addEventListener("mouseup", () => {
        btn.style.transform = "";
    });

    btn.addEventListener("mouseleave", () => {
        btn.style.transform = "";
    });
}

document.addEventListener("DOMContentLoaded", () => {

    const changeBtn = document.getElementById("changeImageBtn");
    const input = document.getElementById("avatarInput");
    const form = document.getElementById("avatarForm");

    if (!changeBtn || !input || !form) {
        console.error("Avatar elements not found");
        return;
    }

    changeBtn.addEventListener("click", () => {
        input.click();
    });

    input.addEventListener("change", () => {
        if (input.files.length === 0) return;
        form.submit();
    });

});
addClickEffect("changeImageBtn");

