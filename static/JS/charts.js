(() => {
    const colors = [
        "#344563",
        "#989EA8",
        "#6B91BD",
        "#92C7E0",
        "#D99A61",
        "#79A883"
    ];

    const numberFormatter = new Intl.NumberFormat("ru-RU", {
        maximumFractionDigits: 2
    });

    function formatMoney(value) {
        if (value == null) return "—";

        const number = Number(value);

        if (!Number.isFinite(number)) return "—";

        const units = [
            { limit: 1e12, label: "трлн" },
            { limit: 1e9, label: "млрд" },
            { limit: 1e6, label: "млн" },
            { limit: 1e3, label: "тыс." }
        ];

        const unit = units.find(
            item => Math.abs(number) >= item.limit
        );

        const result = unit ? number / unit.limit : number;
        const formatted = numberFormatter.format(result);

        return unit ? `${formatted} ${unit.label}` : formatted;
    }

    function prepareChartData(source) {
        return {
            labels: source.data.map(item => item.label),

            datasets: source.series.map((series, index) => ({
                label: series.label,

                data: source.data.map(item => {
                    const value = item[series.key];

                    return value == null ? null : Number(value);
                }),

                backgroundColor: colors[index % colors.length],
                borderWidth: 0
            }))
        };
    }

    function initializeChart(canvas) {
        if (Chart.getChart(canvas)) return;

        const dataElement = document.getElementById(
            canvas.dataset.chartData
        );

        const periodSelect = document.getElementById(
            canvas.dataset.chartPeriod
        );

        if (!dataElement || !periodSelect) return;

        const source = JSON.parse(dataElement.textContent);

        const chart = new Chart(canvas, {
            type: "bar",

            data: prepareChartData(source),

            options: {
                responsive: true,
                maintainAspectRatio: false,

                scales: {
                    x: {
                        stacked: false
                    },

                    y: {
                        beginAtZero: true,

                        ticks: {
                            callback: value => formatMoney(value)
                        }
                    }
                },

                plugins: {
                    legend: {
                        position: "bottom"
                    },

                    tooltip: {
                        callbacks: {
                            label(context) {
                                const label = context.dataset.label || "";
                                const value = formatMoney(context.parsed.y);

                                return label
                                    ? `${label}: ${value}`
                                    : value;
                            }
                        }
                    }
                }
            }
        });

        let loadedMode = periodSelect.value;

        periodSelect.addEventListener("change", async function () {
            const mode = this.value;

            const url = new URL(
                canvas.dataset.chartUrl,
                window.location.origin
            );

            url.searchParams.set("mode", mode);
            this.disabled = true;

            try {
                const response = await fetch(url);

                if (!response.ok) {
                    throw new Error(
                        `Не удалось загрузить график: HTTP ${response.status}`
                    );
                }

                const newData = await response.json();

                chart.data = prepareChartData(newData);
                chart.update();

                loadedMode = mode;
            } catch (error) {
                this.value = loadedMode;

                console.error(error);
                alert("Не удалось обновить график. Попробуйте ещё раз.");
            } finally {
                this.disabled = false;
            }
        });
    }

    function initializeFinancialCharts() {
        if (typeof window.Chart === "undefined") {
            console.error(
                "Chart.js не загружен. Проверь его подключение перед charts.js."
            );
            return;
        }

        document
            .querySelectorAll("canvas[data-chart-data]")
            .forEach(canvas => {
                try {
                    initializeChart(canvas);
                } catch (error) {
                    console.error(
                        `Ошибка создания графика ${canvas.id}:`,
                        error
                    );
                }
            });
    }

    // Можно вызвать после вставки панели через обычный fetch.
    window.initializeFinancialCharts = initializeFinancialCharts;

    // Запуск после вставки панели через HTMX.
    document.addEventListener(
        "htmx:load",
        initializeFinancialCharts
    );

    // Запуск при обычной загрузке страницы.
    if (document.readyState === "loading") {
        document.addEventListener(
            "DOMContentLoaded",
            initializeFinancialCharts
        );
    } else {
        initializeFinancialCharts();
    }
})();