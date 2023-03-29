// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

// AJAX call to get data from the server
let xp = [];
let yp = [];

fetch("/statcltgender")
    .then(response => response.json())
    .then(data => {
        const labels = data.map(row => row._id);
        const values = data.map(row => parseInt(row.count));
        for (let i = 0; i < labels.length; i++) {
            xp.push(String(labels[i]));
            yp.push(parseInt(values[i]));
        }
        console.log(xp);
        console.log(yp);
    }
);

// Pie Chart Example
window.onload = function() {
    setTimeout(function() {
        const ctx = document.getElementById("myPieChart");
        let myPieChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: xp,
                datasets: [{
                    data: yp,
                    backgroundColor: ['#007bff', '#dc3545', '#ffc107', '#28a745'],
                }],
            },
        });
    }, 1500);
};
