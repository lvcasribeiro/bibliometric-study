// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

var evolution_json_file = JSON.parse(document.getElementById("evolution_json").dataset.thetargets);

// Area Chart Example
var ctx = document.getElementById("evolution_chart");
var myLineChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: Object.keys(evolution_json_file),
    datasets: [{
      label: "Publications",
      lineTension: 0.3,
      backgroundColor: "rgba(168, 16, 0,0.2)",
      borderColor: "rgba(168, 16, 0,1)",
      pointRadius: 5,
      pointBackgroundColor: "rgba(168, 16, 0,1)",
      pointBorderColor: "rgba(255,255,255,0.8)",
      pointHoverRadius: 5,
      pointHoverBackgroundColor: "rgba(168, 16, 0,1)",
      pointHitRadius: 50,
      pointBorderWidth: 2,
      data: Object.values(evolution_json_file),
    }],
  },
  options: {
    scales: {
      xAxes: [{
        time: {
          unit: 'year'
        },
        gridLines: {
          display: true
        },
        ticks: {
          maxTicksLimit: 7,
          autoSkip: false
        }
      }],
      yAxes: [{
        ticks: {
          min: 0,
          max: Math.max(...Object.values(evolution_json_file)),
          maxTicksLimit: 5
        },
        gridLines: {
          color: "rgba(0, 0, 0, .125)",
        }
      }],
    },
    legend: {
      display: false
    }
  }
});
