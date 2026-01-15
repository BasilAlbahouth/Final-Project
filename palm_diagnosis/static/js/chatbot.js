document.addEventListener("DOMContentLoaded", () => {
  const chatBox = document.getElementById("chatBox");
  const form = document.getElementById("chatForm");
  const input = document.getElementById("chatInput");

  // ===== رسالة ترحيب تلقائية =====
  const welcomeMsg = `
    <div class="msg bot">
      👋 أهلاً بك!<br>
      أنا مساعد النخيل الذكي 🌴<br><br>
      أقدر أساعدك في:
      <ul>
        <li>تشخيص أمراض النخيل</li>
        <li>شرح نتائج التحليل</li>
        <li>طرق العناية والوقاية</li>
      </ul>
    </div>
  `;
  chatBox.innerHTML += welcomeMsg;

  // ===== إرسال رسالة =====
  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const text = input.value.trim();
    if (!text) return;

    // رسالة المستخدم
    chatBox.innerHTML += `
      <div class="msg user">أنت: ${text}</div>
    `;
    input.value = "";

    // طلب API
    const res = await fetch("/chatbot-api/", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({message: text})
    });

    const data = await res.json();

    // رد المساعد
    chatBox.innerHTML += `
      <div class="msg bot">🌴 المساعد: ${data.answer}</div>
    `;

    chatBox.scrollTop = chatBox.scrollHeight;
  });
});

document.addEventListener("DOMContentLoaded", () => {

function getCsrfToken() {
    const match = document.cookie.match(/csrftoken=([^;]+)/i);
    return match ? match[1] : "";
}

const chatForm = document.getElementById("chatbotForm");
const chatInput = document.getElementById("chatbotText");
const chatMessages = document.getElementById("chatbotMessages");

function addMessage(text, sender = "user") {
    const div = document.createElement("div");
    div.className = `chat-msg ${sender}`;
    div.innerHTML = `<div class="msg-bubble">${text}</div>`;
    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

chatForm?.addEventListener("submit", async (e) => {
    e.preventDefault();

    const text = chatInput.value.trim();
    if (!text) return;

    addMessage(text, "user");
    chatInput.value = "";

    const loading = document.createElement("div");
    loading.className = "chat-msg bot";
    loading.innerHTML = `<div class="msg-bubble">⏳ جاري الكتابة...</div>`;
    chatMessages.appendChild(loading);

    try {
        const res = await fetch("/api/chatbot/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCsrfToken()
            },
            body: JSON.stringify({ message: text })
        });

        const data = await res.json();
        loading.remove();

        if (data.answer) {
            addMessage(data.answer, "bot");
        } else {
            addMessage("⚠️ لم يتم استلام رد واضح.", "bot");
        }

    } catch (err) {
        loading.remove();
        addMessage("❌ خطأ في الاتصال بالمساعد.", "bot");
    }
});

});
