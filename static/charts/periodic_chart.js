// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

var periodic_json_file = JSON.parse(document.getElementById("periodic_json").dataset.thetargets);
console.log(Object.keys(periodic_json_file)[1]);
console.log(Object.values(periodic_json_file)[1]);

// Bar Chart Example
var ctx = document.getElementById("periodic_chart");
var myLineChart = new Chart(ctx, {
    type: 'horizontalBar',
    data: {
        labels: Object.keys(periodic_json_file),
        datasets: [{
            label: "Occurrences",
            backgroundColor: "rgba(219, 142, 8,1)",
            borderColor: "rgba(219, 142, 8,1)",
            data: Object.values(periodic_json_file),
        }],
    },
    options: {
        scales: {
            xAxes: [{
                time: {
                    unit: 'year'
                },
                gridLines: {
                    display: false
                },
                ticks: {
                    maxTicksLimit: 6
                }
            }],
            yAxes: [{
                ticks: {
                    min: 0,
                    max: Math.max(...Object.values(periodic_json_file)),
                    maxTicksLimit: 5,
                    autoSkip: false
                },
                gridLines: {
                    display: true
                }
            }],
        },
        legend: {
            display: false
        }
    }
});
