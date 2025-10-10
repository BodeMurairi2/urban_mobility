async function fetchData() {
  try {
    const response = await fetch("http://127.0.0.1:8000/dashboard");
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Fetch error:", error);
    return null;
  }
}

async function updateParagraph() {
  const data = await fetchData();
  if (data) {
    document.getElementById("bode").textContent = data.message;
  }
}
window.onload = updateParagraph;
