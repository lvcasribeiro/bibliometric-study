// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

var language_json_file = JSON.parse(document.getElementById("language_json").dataset.thetargets);

// Pie Chart Example
var ctx = document.getElementById("language_chart");
var myPieChart = new Chart(ctx, {
  type: 'doughnut',
  data: {
    labels: Object.keys(language_json_file),
    datasets: [{
      data: Object.values(language_json_file),
      backgroundColor: ['#3498db', '#2ecc71', '#e74c3c', '#9b59b6', '#e67e22', '#1abc9c', '#e91e63', '#3f51b5', '#cddc39', '#00bcd4', '#673ab7', '#ff5722', '#87ceeb', '#8bc34a', '#ff7961', '#d1c4e9', '#fdd835', '#ffca28', '#f06292', '#4dd0e1'],
    }],
  },
});
