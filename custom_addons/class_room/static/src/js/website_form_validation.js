function validateForm() {
                var phoneNumber = document.getElementById("phone").value;
                var emailFormat = document.getElementById("email").value;


                var phonePattern = /^\d{10}$/;


                var emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

                var phoneError = document.getElementById("phoneError");
                var emailError = document.getElementById("emailError");

                if (!phonePattern.test(phoneNumber)) {
                    phoneError.textContent = "Invalid phone number Format..";
                    return false;
                } else {
                    phoneError.textContent = "";
                }

                if (!emailPattern.test(emailFormat)) {
                    emailError.textContent = "Invalid email Format.. ";
                    return false;
                } else {
                    emailError.textContent = "";
                }


                return true;
            }

            function saveData() {
                var formData = {
                    name: document.getElementById("name").value,
                    phone: document.getElementById("phone").value,
                    email: document.getElementById("email").value,
                    dob: document.getElementById("dob").value
                };



            }