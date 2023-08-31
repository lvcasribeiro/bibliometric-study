// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

var year_json_file = JSON.parse(document.getElementById("year_json").dataset.thetargets);

// Bar Chart Example
var ctx = document.getElementById("year_chart");
var myLineChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: Object.keys(year_json_file),
        datasets: [{
            label: "Publitacions",
            backgroundColor: "rgba(2,117,216,1)",
            borderColor: "rgba(2,117,216,1)",
            data: Object.values(year_json_file),
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
                    maxTicksLimit: 6,
                    autoSkip: false
                }
            }],
            yAxes: [{
                ticks: {
                    min: 0,
                    max: Math.max(...Object.values(year_json_file)),
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
