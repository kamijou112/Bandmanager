document.addEventListener("DOMContentLoaded", function () {
    // Get the form element
    var form = document.querySelector("form");

    // Add a submit event listener to the form
    form.addEventListener("submit", function (event) {
        var email = document.getElementById("email").value;
        var phone = document.getElementById("phone").value;

        // Validate email format
        if (!isValidEmail(email)) {
            displayErrorMessage("Please enter a valid email address.");
            event.preventDefault(); // Prevent form submission
            return;
        }

        // Validate phone number format
        if (!isValidPhone(phone)) {
            displayErrorMessage("Please enter a valid 11-digit phone number.");
            event.preventDefault(); // Prevent form submission
            return;
        }

        // You can add more validation logic for other fields if needed

        // If all validations pass, the form will be submitted
    });

    // Email validation function
    function isValidEmail(email) {
        var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    // Phone number validation function
    function isValidPhone(phone) {
        var phoneRegex = /^\d{11}$/;
        return phoneRegex.test(phone);
    }

    // Function to display error message on the page
    function displayErrorMessage(message) {
        var errorMessageElement = document.createElement("h3");
        errorMessageElement.className = "my_danger";
        errorMessageElement.textContent = message;

        // Append the error message to the card body
        var cardBody = document.querySelector(".card-body");
        cardBody.appendChild(errorMessageElement);
    }
});
