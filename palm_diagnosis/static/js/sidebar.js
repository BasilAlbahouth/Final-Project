document.addEventListener("DOMContentLoaded", () => {
  const sidebar = document.getElementById("sidebar");
  const handle = document.getElementById("sidebarHandle");

  handle.addEventListener("click", () => {
    const isOpen = sidebar.classList.toggle("open");

    // هنا الحل
    document.body.classList.toggle("sidebar-open", isOpen);

    handle.innerHTML = isOpen ? "➜" : "☰";
  });
});
