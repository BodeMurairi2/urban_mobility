/* =====================================
   NYC METROPOLIS TAXI ANALYTICS
   INTERACTION SCRIPT (FINAL VERSION)
   ===================================== */

// ---------- Smooth scroll navigation ----------
function scrollToSection(id) {
  const section = document.getElementById(id);
  if (section) section.scrollIntoView({ behavior: "smooth" });
}

// ---------- Download PDF ----------
const downloadBtn = document.getElementById("downloadBtn");
if (downloadBtn) {
  downloadBtn.addEventListener("click", () => {
    const link = document.createElement("a");
    link.href = "NYC_Taxi_Analytics_Report.pdf";
    link.download = "NYC_Taxi_Analytics_Report.pdf";
    link.click();
  });
}

// ---------- Scroll-to-top button ----------
const scrollBtn = document.getElementById("scrollTopBtn");
if (scrollBtn) {
  window.addEventListener("scroll", () => {
    scrollBtn.style.display = window.scrollY > 300 ? "block" : "none";
  });
  scrollBtn.addEventListener("click", () =>
    window.scrollTo({ top: 0, behavior: "smooth" })
  );
}

// ---------- Report frame control (preview modal) ----------
const reportFrameBox = document.getElementById("reportFrameBox");
const openReportBtn = document.getElementById("openReportBtn");
const closeReportBtn = document.getElementById("closeReportBtn");

if (openReportBtn && reportFrameBox) {
  openReportBtn.addEventListener("click", () => {
    reportFrameBox.style.display = "flex";
    setTimeout(() => (reportFrameBox.style.opacity = "1"), 50);
  });
}

if (closeReportBtn && reportFrameBox) {
  closeReportBtn.addEventListener("click", () => {
    reportFrameBox.style.opacity = "0";
    setTimeout(() => (reportFrameBox.style.display = "none"), 300);
  });
}

// ---------- Image Gallery (Horizontal, Non-looping, Draggable) ----------
const carousel = document.querySelector(".image-carousel");
const track = document.querySelector(".carousel-track");

if (carousel && track) {
  let isDragging = false;
  let startX;
  let scrollLeft;
  let autoScrollInterval;
  let autoScrollSpeed = 0.5;

  // Set gallery in a straight horizontal line
  track.style.display = "flex";
  track.style.gap = "1.2rem";
  track.style.transition = "transform 0.2s ease-out";

  // Auto-scroll function
  function startAutoScroll() {
    stopAutoScroll();
    autoScrollInterval = setInterval(() => {
      carousel.scrollLeft += autoScrollSpeed;
      // stop at the end smoothly
      if (
        carousel.scrollLeft >=
        track.scrollWidth - carousel.clientWidth - 1
      ) {
        carousel.scrollLeft = 0; // reset to start smoothly
      }
    }, 16);
  }

  // Stop auto-scroll
  function stopAutoScroll() {
    clearInterval(autoScrollInterval);
  }

  startAutoScroll();

  // Pause on hover
  carousel.addEventListener("mouseenter", stopAutoScroll);
  carousel.addEventListener("mouseleave", () => {
    if (!isDragging) startAutoScroll();
  });

  // Mouse drag control
  carousel.addEventListener("mousedown", (e) => {
    isDragging = true;
    carousel.classList.add("dragging");
    startX = e.pageX - carousel.offsetLeft;
    scrollLeft = carousel.scrollLeft;
    stopAutoScroll();
  });

  carousel.addEventListener("mouseleave", () => {
    if (isDragging) {
      isDragging = false;
      carousel.classList.remove("dragging");
      startAutoScroll();
    }
  });

  window.addEventListener("mouseup", () => {
    if (isDragging) {
      isDragging = false;
      carousel.classList.remove("dragging");
      startAutoScroll();
    }
  });

  carousel.addEventListener("mousemove", (e) => {
    if (!isDragging) return;
    e.preventDefault();
    const x = e.pageX - carousel.offsetLeft;
    const walk = (x - startX) * 1.5;
    carousel.scrollLeft = scrollLeft - walk;
  });

  // Touch (mobile drag)
  carousel.addEventListener("touchstart", (e) => {
    isDragging = true;
    startX = e.touches[0].pageX - carousel.offsetLeft;
    scrollLeft = carousel.scrollLeft;
    stopAutoScroll();
  });

  carousel.addEventListener("touchmove", (e) => {
    if (!isDragging) return;
    const x = e.touches[0].pageX - carousel.offsetLeft;
    const walk = (x - startX) * 1.5;
    carousel.scrollLeft = scrollLeft - walk;
  });

  carousel.addEventListener("touchend", () => {
    isDragging = false;
    startAutoScroll();
  });
}

// ---------- Fade-in on scroll ----------
const fadeElements = document.querySelectorAll(".fade-in");
if (fadeElements.length > 0) {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) entry.target.classList.add("visible");
      });
    },
    { threshold: 0.1 }
  );

  fadeElements.forEach((el) => observer.observe(el));
}

const track = document.getElementById('gallery-track');
let isDragging = false;
let startX, scrollLeft;
let autoScrollSpeed = 1; // pixels per frame
let autoScrollFrame;

// Duplicate content for seamless infinite loop
function duplicateImages() {
  const images = [...track.children];
  images.forEach(img => {
    const clone = img.cloneNode(true);
    track.appendChild(clone);
  });
}
duplicateImages();

// Auto-scroll in an infinite loop
function startAutoScroll() {
  cancelAnimationFrame(autoScrollFrame);

  function scroll() {
    track.scrollLeft += autoScrollSpeed;
    if (track.scrollLeft >= track.scrollWidth / 2) {
      track.scrollLeft = 0; // reset to start
    }
    autoScrollFrame = requestAnimationFrame(scroll);
  }

  autoScrollFrame = requestAnimationFrame(scroll);
}

function stopAutoScroll() {
  cancelAnimationFrame(autoScrollFrame);
}

// Mouse interactions
track.addEventListener('mousedown', (e) => {
  isDragging = true;
  startX = e.pageX - track.offsetLeft;
  scrollLeft = track.scrollLeft;
  stopAutoScroll();
});

track.addEventListener('mouseleave', () => {
  if (isDragging) {
    isDragging = false;
    startAutoScroll();
  }
});

track.addEventListener('mouseup', () => {
  isDragging = false;
  startAutoScroll();
});

track.addEventListener('mousemove', (e) => {
  if (!isDragging) return;
  e.preventDefault();
  const x = e.pageX - track.offsetLeft;
  const walk = (x - startX) * 1.5; // drag sensitivity
  track.scrollLeft = scrollLeft - walk;
});

// Touch interactions (mobile)
track.addEventListener('touchstart', (e) => {
  isDragging = true;
  startX = e.touches[0].pageX - track.offsetLeft;
  scrollLeft = track.scrollLeft;
  stopAutoScroll();
});

track.addEventListener('touchend', () => {
  isDragging = false;
  startAutoScroll();
});

track.addEventListener('touchmove', (e) => {
  if (!isDragging) return;
  const x = e.touches[0].pageX - track.offsetLeft;
  const walk = (x - startX) * 1.5;
  track.scrollLeft = scrollLeft - walk;
});

// Initialize on load
startAutoScroll();
