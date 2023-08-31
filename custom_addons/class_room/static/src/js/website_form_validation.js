function validateEmail(email) {
  if (email == null || email == "") {
    return false;
  }

  let atSymbolPos = email.indexOf("@");
  if (atSymbolPos < 1) {
    return false;
  }

  let dotPos = email.indexOf(".");
  if (dotPos <= atSymbolPos + 2) {
    return false;
  }

  return dotPos !== email.length - 1;
}

function validateEmailWithRegex(email) {
  let emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  return !!email && typeof email === "string" && email.match(emailRegex);
}

function checkInputEmail(email) {
  let isValidEmail = validateEmail(email);
  let emailInput = document.getElementById("email");
  let emailErrorSpan = document.getElementById("emailError");
  if (!isValidEmail) {
    emailErrorSpan.innerText = "Invalid email!";
    emailInput.valid = false;
    return false;
  }
  emailErrorSpan.remove();
  alert("Valid email!");
  return true;
}


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
