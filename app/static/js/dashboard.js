document.addEventListener("DOMContentLoaded", function () {
    const dataFromServer = JSON.parse(document.getElementById("chart-data").textContent);

    const ingresos = {};
    const egresos = {};

    for (const key in dataFromServer) {
        const [tipo, categoria] = key.split("_");
        if (tipo === "ingreso") {
            ingresos[categoria] = dataFromServer[key];
        } else {
            egresos[categoria] = dataFromServer[key];
        }
    }

    const pieLabels = Object.keys(egresos);
    const pieValues = Object.values(egresos);

    new Chart(document.getElementById("pieChart"), {
        type: "pie",
        data: {
            labels: pieLabels,
            datasets: [{
                label: "Egresos por Categoría",
                data: pieValues,
                backgroundColor: [
                    "#ff6384", "#36a2eb", "#ffcd56", "#4bc0c0", "#9966ff", "#ff9f40"
                ]
            }]
        }
    });

    const categoriasSet = new Set([...Object.keys(ingresos), ...Object.keys(egresos)]);
    const categoriasTotales = Array.from(categoriasSet);

    const ingresosData = categoriasTotales.map(cat => ingresos[cat] || 0);
    const egresosData = categoriasTotales.map(cat => egresos[cat] || 0);

    new Chart(document.getElementById("barChart"), {
        type: "bar",
        data: {
            labels: categoriasTotales,
            datasets: [
                {
                    label: "Ingresos",
                    backgroundColor: "#36a2eb",
                    data: ingresosData
                },
                {
                    label: "Egresos",
                    backgroundColor: "#ff6384",
                    data: egresosData
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});