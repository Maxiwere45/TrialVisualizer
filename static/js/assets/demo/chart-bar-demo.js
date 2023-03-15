let x = [];
let y = [];
fetch('/chart1')
    .then(response => response.json())
    .then(data => {
        const labels = data.map(row => row._id);
        const values = data.map(row => parseInt(row.count));
        for (let i = 0; i < labels.length; i++) {
            x.push(String(labels[i]));
            y.push(parseInt(values[i]));
        }
        console.log(x);
        console.log(y);
    });

// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

// Bar Chart Example
window.onload = function() {
    setTimeout(function() {
        var ctx = document.getElementById("myBarChart");
        var myLineChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: x,
                datasets: [{
                    axis: 'y',
                    label: "Essai",
                    backgroundColor: "rgb(35,31,236)",
                    borderColor: "rgb(2,0,77)",
                    data: y,
                }]
            },
            options: {
                scales: {
                    xAxes: [{
                        gridLines: {
                            display: true
                        },
                        ticks: {
                            maxTicksLimit: 6
                        }
                    }],
                    yAxes: [{
                        ticks: {
                            min: 0,
                            max: 1000,
                            maxTicksLimit: 5
                        },
                        gridLines: {
                            display: true
                        }
                    }],
                },
                legend: {
                    display: false
                },maxBarThickness: 50 // number (pixels) or 'flex'
            }
        });
    }, 1500);};


