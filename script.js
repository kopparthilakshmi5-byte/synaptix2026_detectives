let labels = [];
let hrData = [];
let tempData = [];
let spo2Data = [];
let rrData = [];
let chart;

function initChart() {
    const ctx = document.getElementById("riskChart").getContext("2d");

    chart = new Chart(ctx, {
        type: "line",
        data: {
            labels: labels,
            datasets: [
                { label: "❤️ Heart Rate", data: hrData },
                { label: "🌡️ Temperature", data: tempData },
                { label: "🩸 SpO2", data: spo2Data },
                { label: "💨 Respiration", data: rrData }
            ]
        },
        options: {
            responsive: true
        }
    });
}

function showPopup(title, message) {
    document.getElementById("popupTitle").innerText = title;
    document.getElementById("popupMessage").innerText = message;
    document.getElementById("popup").style.display = "block";
}

function closePopup() {
    document.getElementById("popup").style.display = "none";
}

async function fetchData() {
    const response = await fetch("/api/data");
    const data = await response.json();

    document.getElementById("hr").innerText = "❤️ " + data.heart_rate;
    document.getElementById("spo2").innerText = "🩸 " + data.spo2;
    document.getElementById("temp").innerText = "🌡️ " + data.temperature;
    document.getElementById("rr").innerText = "💨 " + data.respiratory_rate;
    document.getElementById("risk").innerText = "⚠️ " + data.risk_score;

    document.getElementById("alertBox").innerText =
        data.alert + ": " + data.alert_message;

    if (data.alert_level !== "low") {
        showPopup(data.alert, data.alert_message);
    }

    // Multi-line graph update
    labels.push(new Date().toLocaleTimeString());
    hrData.push(data.heart_rate);
    tempData.push(data.temperature);
    spo2Data.push(data.spo2);
    rrData.push(data.respiratory_rate);

    if (labels.length > 20) {
        labels.shift();
        hrData.shift();
        tempData.shift();
        spo2Data.shift();
        rrData.shift();
    }

    chart.update();
}

initChart();
setInterval(fetchData, 3000);
fetchData();