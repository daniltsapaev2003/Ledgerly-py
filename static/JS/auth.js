(() => {
    function initializeAuth() {
        const card = document.getElementById("auth-card");

        if (!card) return;

        // Переключение между входом и регистрацией.
        document.querySelectorAll("[data-auth-toggle]").forEach(button => {
            button.addEventListener("click", () => {
                card.classList.toggle("auth-flipped");
            });
        });

        // Плавное скрытие ошибки входа.
        const message = document.getElementById("login-error-message");

        if (message) {
            setTimeout(() => {
                message.style.opacity = "0";

                setTimeout(() => {
                    message.remove();
                }, 500);
            }, 2000);
        }
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initializeAuth);
    } else {
        initializeAuth();
    }
})();