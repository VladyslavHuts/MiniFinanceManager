document.getElementById("removeForm").addEventListener("submit", function (event) {
    const nameInput = document.getElementById("removeName");
    const dateInput = document.getElementById("removeDate");
    const nameError = document.getElementById("nameError");
    const dateError = document.getElementById("dateError");

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

    if (!isValid) {
        event.preventDefault();
    }
});