odoo.define('class_room.website_form_validation', function (require) {
    'use strict';

    var ajax = require('web.ajax');
    var core = require('web.core');
    var qweb = core.qweb;

    $(document).ready(function () {
        // ... Your existing code ...

        // Validate email format
        $('#email').on('blur', function () {
            var email = $(this).val();
            var emailError = $('#email-error');

            if (!isValidEmail(email)) {
                emailError.text('Invalid email format. Please write the email in the correct format.');
            } else {
                emailError.text('');
            }
        });

        // Validate phone number format
        $('#phone').on('blur', function () {
            var phone = $(this).val();
            var phoneError = $('#phone-error');

            if (!isValidPhoneNumber(phone)) {
                phoneError.text('Invalid phone number format (10 digits). Please write the phone number in the correct format.');
            } else {
                phoneError.text('');
            }
        });

        // ... Your existing code ...

        function isValidEmail(email) {
            // ... Your existing email validation code ...
        }

        function isValidPhoneNumber(phone) {
            // ... Your existing phone validation code ...
        }
    });
});

//function validateForm() {
//  var phoneNumber = document.getElementById("phone").value;
//  var email = document.getElementById("email").value;
//
//  // Regular expression for validating phone number
//  var phonePattern = /^\d{10}$/;
//
//  // Regular expression for validating email address
//  var emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
//
//  if (!phonePattern.test(phone)) {
//    alert("Invalid phone number");
//    return;
//  }
//
//  if (!emailPattern.test(email)) {
//    alert("Invalid email address");
//    return;
//  }
//
//  // Validation successful, proceed to save the data
//  saveData();
//}
//
//function saveData() {
//  var formData = {
//    name: document.getElementById("name").value,
//    phone: document.getElementById("phone").value,
//    email: document.getElementById("email").value,
//    dob: document.getElementById("dob").value
//  };
//
//  // Send formData to backend (e.g., using AJAX)
//  // Example: Send data to Odoo backend using REST API
//}
