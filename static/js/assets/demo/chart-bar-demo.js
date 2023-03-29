let x = [];
let y = [];
fetch('/chart-nb-phase')
    .then(response => response.json())
    .then(data => {
        const labels = data.map(row => row._id);
        const values = data.map(row => parseInt(row.count));
        for (let i = 0; i < labels.length; i++) {
            x.push(String(labels[i]));
            y.push(parseInt(values[i]));
        }
    });



// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';




// Bar Chart Example
window.onload = function() {
    setTimeout(function() {
        const ctx = document.getElementById("myBarChart");
        const myLineChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: x,
                datasets: [{
                    axis: 'y',
                    label: "Essai",
                    backgroundColor: "rgb(0,35,175)",
                    borderColor: "rgb(0,8,152)",
                    data: y
                }]
            },
            options: {
                scales: {
                    xAxes: [{
                        gridLines: {
                            display: true
                        },
                        ticks: {
                            maxTicksLimit: 20
                        }
                    }],
                    yAxes: [{
                        ticks: {
                            min: 0,
                            max: 1100,
                            maxTicksLimit: 10
                        },
                        gridLines: {
                            display: true
                        }
                    }],
                },
                legend: {
                    display: false
                }, maxBarThickness: 50 // number (pixels) or 'flex'
            }
        });
    }, 1500);
};


