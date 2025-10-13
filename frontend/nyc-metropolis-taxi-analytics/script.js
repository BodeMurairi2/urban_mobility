// Initialize map
const map = L.map("map").setView([40.7128, -74.006], 11);
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: "© OpenStreetMap",
}).addTo(map);

// Fake taxi trip data
let taxiData = Array.from({ length: 50 }, () => ({
  fare: Math.random() * 80,
  distance: Math.random() * 25,
  pickup: [40.7 + Math.random() * 0.1, -74 + Math.random() * 0.1],
}));

// Show map markers
taxiData.forEach(t => {
  L.circleMarker(t.pickup, { radius: 4, color: "#007a7a" }).addTo(map);
});

// Update statistics
function updateStats(data) {
  const total = data.length;
  const avgFare = (data.reduce((s, d) => s + d.fare, 0) / total).toFixed(2);
  const avgDist = (data.reduce((s, d) => s + d.distance, 0) / total).toFixed(2);
  document.getElementById("totalTrips").innerText = total;
  document.getElementById("avgFare").innerText = `$${avgFare}`;
  document.getElementById("avgDistance").innerText = `${avgDist} km`;
}
updateStats(taxiData);

// Draw chart
const ctx = document.getElementById("fareChart");
let chart = new Chart(ctx, {
  type: "bar",
  data: {
    labels: ["0-10", "10-20", "20-30", "30-40", "40+"],
    datasets: [
      {
        label: "Trips by Fare Range ($)",
        data: [10, 15, 20, 8, 5],
        backgroundColor: "#007a7a",
      },
    ],
  },
  options: { responsive: true },
});

// Filter interactions
document.getElementById("applyFilters").addEventListener("click", () => {
  const fareMax = parseInt(document.getElementById("fareFilter").value, 10);
  const distMax = parseInt(document.getElementById("distanceFilter").value, 10);
  const filtered = taxiData.filter(t => t.fare <= fareMax && t.distance <= distMax);
  updateStats(filtered);
});

// --- Header Icon Logic ---
const menuToggle = document.getElementById("menuToggle");
const navLinks = document.getElementById("navLinks");
const searchIcon = document.getElementById("searchIcon");
const settingsIcon = document.getElementById("settingsIcon");
const searchPopup = document.getElementById("searchPopup");
const settingsPopup = document.getElementById("settingsPopup");

menuToggle.addEventListener("click", () => {
  navLinks.classList.toggle("open");
  if (navLinks.classList.contains("open")) {
    navLinks.style.display = "flex";
  } else {
    navLinks.style.display = "none";
  }
});

searchIcon.addEventListener("click", () => {
  searchPopup.style.display = searchPopup.style.display === "block" ? "none" : "block";
  settingsPopup.style.display = "none";
});

settingsIcon.addEventListener("click", () => {
  settingsPopup.style.display = settingsPopup.style.display === "block" ? "none" : "block";
  searchPopup.style.display = "none";
});

// --- Scroll to Top ---
const scrollBtn = document.getElementById("scrollTopBtn");
window.onscroll = function() {
  if (document.body.scrollTop > 100 || document.documentElement.scrollTop > 100) {
    scrollBtn.style.display = "block";
  } else {
    scrollBtn.style.display = "none";
  }
};
scrollBtn.addEventListener("click", () => {
  window.scrollTo({ top: 0, behavior: "smooth" });
});
