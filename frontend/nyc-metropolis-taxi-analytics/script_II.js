const API_BASE = "http://127.0.0.1:8000/api";

// Example: Fetch and display most visited places
async function renderMostVisitedChart() {
  try {
    const response = await fetch(`${API_BASE}/visit/most_trips`);
    const data = await response.json();

    // Assume data looks like: 
    // [{ place: "Manhattan", trips: 1200 }, { place: "Brooklyn", trips: 800 }]
    const labels = data.map(item => item.place);
    const values = data.map(item => item.trips);

    const ctx = document.getElementById("mostVisitedChart").getContext("2d");

    new Chart(ctx, {
      type: "bar", // can be "pie", "line", etc.
      data: {
        labels: labels,
        datasets: [{
          label: "Number of Trips",
          data: values,
          backgroundColor: "rgba(54, 162, 235, 0.7)"
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { display: true },
          title: { display: true, text: "Most Visited Places by Trips" }
        }
      }
    });
  } catch (error) {
    console.error("Error rendering chart:", error);
  }
}

// Run when page loads
document.addEventListener("DOMContentLoaded", renderMostVisitedChart);
