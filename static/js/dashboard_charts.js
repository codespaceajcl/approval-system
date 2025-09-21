// Dashboard charts for request trends and department bar chart
window.addEventListener('DOMContentLoaded', function() {
  // Data from Jinja2 context
  const trendData = JSON.parse(document.getElementById('trend-data').textContent);
  const deptData = JSON.parse(document.getElementById('dept-data').textContent);

  // Request Trend (date-wise)
  const ctxTrend = document.getElementById('trendChart').getContext('2d');
  new Chart(ctxTrend, {
    type: 'line',
    data: {
      labels: trendData.labels,
      datasets: [{
        label: 'Requests per Day',
        data: trendData.counts,
        borderColor: '#2575fc',
        backgroundColor: 'rgba(56,189,248,0.2)',
        fill: true,
        tension: 0.3
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } }
    }
  });

  // Department Bar Chart
  const ctxDept = document.getElementById('deptChart').getContext('2d');
  new Chart(ctxDept, {
    type: 'bar',
    data: {
      labels: deptData.labels,
      datasets: [{
        label: 'Requests by Department',
        data: deptData.counts,
        backgroundColor: '#38bdf8',
        borderRadius: 8
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: { y: { beginAtZero: true } }
    }
  });
});
