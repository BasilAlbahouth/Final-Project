let map;

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 24.7136, lng: 46.6753 }, // السعودية افتراضياً
    zoom: 6,
  });

  // رسم النخيل
  PALMS_DATA.forEach(palm => {
    const marker = new google.maps.Marker({
      position: { lat: palm.lat, lng: palm.lng },
      map,
      title: palm.name,
      icon: "https://maps.google.com/mapfiles/ms/icons/green-dot.png"
    });

    const info = new google.maps.InfoWindow({
      content: `
        <strong>${palm.name}</strong><br>
        <a href="/palm/${palm.id}/">عرض التفاصيل</a>
      `
    });

    marker.addListener("click", () => info.open(map, marker));
  });

  // إضافة نخلة جديدة
  map.addListener("click", (e) => {
    addPalmPrompt(e.latLng);
  });
}

function addPalmPrompt(latLng) {
  const name = prompt("🌴 أدخل اسم النخلة:");
  if (!name) return;

  fetch("/api/add-palm/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCsrfToken()
    },
    body: JSON.stringify({
      name: name,
      lat: latLng.lat(),
      lng: latLng.lng()
    })
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) location.reload();
    else alert("خطأ أثناء الإضافة");
  });
}

function getCsrfToken() {
  return document.querySelector("[name=csrfmiddlewaretoken]").value;
}
