document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("rechargeForm");
    const amountInput = document.getElementById("rechargeAmount");
    const errorMessage = document.getElementById("errorMessage");

    form.addEventListener("submit", function (event) {
        const amount = parseFloat(amountInput.value);

        if (isNaN(amount) || amount <= 0) {
            event.preventDefault();  // Зупиняємо сабміт форми
            errorMessage.textContent = "Proszę wprowadzić prawidłową kwotę większą niż 0.";  // Встановлюємо текст помилки
            errorMessage.classList.add("error-visible");  // Додаємо клас для відображення помилки
            console.log("Помилка: введена некоректна сума");  // Лог для перевірки
        } else {
            errorMessage.classList.remove("error-visible");  // Якщо сума правильна, видаляємо помилку
            event.preventDefault();  // Зупиняємо сабміт для тестів
            alert("Doładowanie zakończone sukcesem! Przekierowanie na stronę główną...");
            window.location.pathname = "/";
        }
    });
});
