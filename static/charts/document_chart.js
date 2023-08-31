// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

var document_json_file = JSON.parse(document.getElementById("document_json").dataset.thetargets);

// Bar Chart Example
var ctx = document.getElementById("document_chart");
var myLineChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: Object.keys(document_json_file),
        datasets: [{
            label: "Documents",
            backgroundColor: "#9b59b6",
            borderColor: "#9b59b6",
            data: Object.values(document_json_file),
        }],
    },
    options: {
        scales: {
            xAxes: [{
                time: {
                    unit: 'month'
                },
                gridLines: {
                    display: false
                },
                ticks: {
                    maxTicksLimit: 6,
                    autoSkip: false
                }
            }],
            yAxes: [{
                ticks: {
                    min: 0,
                    max: Math.max(...Object.values(document_json_file)),
                    maxTicksLimit: 5
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
