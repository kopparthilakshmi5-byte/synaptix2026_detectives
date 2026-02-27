const ctx = document.getElementById('healthChart').getContext('2d');

let labels = [];
let hrData = [];
let spo2Data = [];
let tempData = [];
let rrData = [];

const healthChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: labels,
        datasets: [
            { label: 'HR', data: hrData, borderColor: 'red', fill: false },
            { label: 'SpO₂', data: spo2Data, borderColor: 'green', fill: false },
            { label: 'Temp', data: tempData, borderColor: 'orange', fill: false },
            { label: 'RR', data: rrData, borderColor: 'blue', fill: false }
        ]
    },
    options: {
        responsive: true,
        animation: false,
        scales: {
            y: { beginAtZero: false }
        }
    }
});

function fetchData() {
    fetch("/api/data")
        .then(response => response.json())
        .then(data => {
            document.getElementById('heart_rate').innerText = data.heart_rate + " bpm";
            document.getElementById('spo2').innerText = data.spo2 + " %";
            document.getElementById('temperature').innerText = data.temperature + " °C";
            document.getElementById('respiratory_rate').innerText = data.respiratory_rate + " bpm";
            document.getElementById('risk_score').innerText = data.risk_score;

            const time = new Date().toLocaleTimeString();
            labels.push(time);
            hrData.push(data.heart_rate);
            spo2Data.push(data.spo2);
            tempData.push(data.temperature);
            rrData.push(data.respiratory_rate);

            if(labels.length > 20) {
                labels.shift();
                hrData.shift();
                spo2Data.shift();
                tempData.shift();
                rrData.shift();
            }

            healthChart.update();
        });
}

setInterval(fetchData, 1000);