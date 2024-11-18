document.addEventListener("DOMContentLoaded", function () {
    const transactionForm = document.getElementById("transactionForm");
    const nameInput = document.getElementById("transactionName");
    const dateInput = document.getElementById("transactionDate");
    const amountInput = document.getElementById("transactionAmount");
    const nameError = document.getElementById("nameError");
    const dateError = document.getElementById("dateError");
    const amountError = document.getElementById("amountError");

    transactionForm.addEventListener("submit", function (event) {
        let isValid = true;

        if (nameInput.value.trim() === "") {
            nameError.textContent = "Proszę wprowadzić nazwę.";
            nameError.style.display = "block";
            isValid = false;
        } else {
            nameError.style.display = "none";
        }

        if (dateInput.value === "") {
            dateError.textContent = "Proszę wybrać datę.";
            dateError.style.display = "block";
            isValid = false;
        } else {
            dateError.style.display = "none";
        }

        const amount = parseFloat(amountInput.value);
        if (isNaN(amount) || amount <= 0) {
            amountError.textContent = "Proszę wprowadzić poprawną sumę większą ніж 0.";
            amountError.style.display = "block";
            isValid = false;
        } else {
            amountError.style.display = "none";
        }

        if (!isValid) {
            event.preventDefault();
        } else {
            event.preventDefault();
            alert("Form submitted successfully! Redirecting to the main page...");
            window.location.href = "/";
        }
    });
});