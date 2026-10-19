(() => {
    function initializeDashboard() {
        const searchInput = document.getElementById("company-search");

        if (!searchInput) return;

        // Защита от повторной инициализации.
        if (searchInput.dataset.initialized === "true") return;
        searchInput.dataset.initialized = "true";

        const sidebar = searchInput.closest("aside");

        if (!sidebar) return;

        // Поиск по тикеру и названию компании.
        searchInput.addEventListener("input", function () {
            const searchValue = this.value.toLowerCase().trim();

            sidebar.querySelectorAll(".company-item").forEach(item => {
                const ticker = (item.dataset.ticker || "").toLowerCase();
                const name = (item.dataset.name || "").toLowerCase();

                const matches =
                    ticker.includes(searchValue) ||
                    name.includes(searchValue);

                item.style.display = matches ? "flex" : "none";
            });
        });

        // Выделение выбранной компании.
        sidebar.addEventListener("click", function (event) {
            if (!(event.target instanceof Element)) return;

            const item = event.target.closest(".company-item");

            if (!item || !sidebar.contains(item)) return;

            sidebar.querySelectorAll(".company-item").forEach(company => {
                company.classList.remove("selected");
            });

            item.classList.add("selected");
        });
    }

    // Делегирование работает и для кнопок, добавленных через HTMX.
    if (!window.dashboardPeriodClickInitialized) {
        window.dashboardPeriodClickInitialized = true;

        document.addEventListener("click", function (event) {
            if (!(event.target instanceof Element)) return;

            const button = event.target.closest(
                "#reports-section .year-button"
            );

            if (!button) return;

            // Меняем выделение только в текущей строке:
            // выбор периода не снимает выделение с года.
            const group = button.parentElement;

            if (!group) return;

            group.querySelectorAll(".year-button").forEach(item => {
                item.classList.remove("selected");
            });

            button.classList.add("selected");
        });
    }

    if (document.readyState === "loading") {
        document.addEventListener(
            "DOMContentLoaded",
            initializeDashboard
        );
    } else {
        initializeDashboard();
    }
})();