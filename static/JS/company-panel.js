(() => {
    // Не добавляем обработчик повторно.
    if (window.companyPanelKeyboardInitialized) return;
    window.companyPanelKeyboardInitialized = true;

    document.addEventListener("keydown", function (event) {
        if (event.repeat || event.defaultPrevented) return;

        if (event.key !== "ArrowRight" && event.key !== "ArrowLeft") {
            return;
        }

        // Не мешаем работе с полями ввода.
        if (
            event.target instanceof Element &&
            event.target.closest(
                "input, textarea, select, [contenteditable]:not([contenteditable='false'])"
            )
        ) {
            return;
        }

        const panel = document.getElementById("company-panel");

        if (!panel) return;

        const sections = [
            panel.querySelector("#reports-section"),
            panel.querySelector("#graphs-section"),
            panel.querySelector("#analyst-forecasts-section")
        ];

        if (sections.some(section => !section)) return;

        const currentScreen = sections.findIndex(
            section => getComputedStyle(section).display !== "none"
        );

        if (currentScreen === -1) return;

        const direction = event.key === "ArrowRight" ? 1 : -1;

        const nextScreen = Math.max(
            0,
            Math.min(sections.length - 1, currentScreen + direction)
        );

        event.preventDefault();

        if (nextScreen === currentScreen) return;

        sections.forEach((section, index) => {
            section.style.display =
                index === nextScreen ? "block" : "none";
        });

        if (nextScreen === 1) {
            requestAnimationFrame(() => {
                if (
                    typeof window.initializeFinancialCharts === "function"
                ) {
                    window.initializeFinancialCharts();
                }

                if (typeof window.Chart === "undefined") return;

                sections[1].querySelectorAll("canvas").forEach(canvas => {
                    const chart = window.Chart.getChart(canvas);

                    if (chart) {
                        chart.resize();
                    }
                });
            });
        }
    });
})();