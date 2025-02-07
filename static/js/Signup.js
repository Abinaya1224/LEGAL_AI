function validateInput(inputId, hintId, regex, minLength, successMessage, errorMessage, minLengthMessage) {
  document.getElementById(inputId).addEventListener("input", function () {
    let value = this.value.trim();
    let hintElement = document.getElementById(hintId);

    if (value.length < minLength) {
      hintElement.textContent = minLengthMessage;
      hintElement.classList.remove("success");
      hintElement.classList.add("error");
    } else if (!regex.test(value)) {
      hintElement.textContent = errorMessage;
      hintElement.classList.remove("success");
      hintElement.classList.add("error");
    } else {
      hintElement.textContent = successMessage;
      hintElement.classList.remove("error");
      hintElement.classList.add("success");
    }
  });
}
validateInput(
  "designation",
  "designation-hint",
  /^[A-Za-z]+(?:\s[A-Za-z]+)*$/,
  3,
  "Designation looks good!",
  "Please enter a valid designation."
);

validateInput(
  "organisation",
  "organisation-hint",
  /^[A-Za-z]+(?:\s[A-Za-z]+)*$/,
  3,
  "Organisation looks good!",
  "Please enter a valid organisation."
);
document.getElementById("name").addEventListener("input", function() {
  let name = this.value.trim();
  let nameRegex = /^[A-Za-z]+(?:\s[A-Za-z]+)*$/;
  let hintElement = document.getElementById("name-hint");

  if (!nameRegex.test(name)) {
    hintElement.textContent = "Name must only contain letters and spaces.";
    hintElement.classList.remove("success");
    hintElement.classList.add("error");
  } else {
    hintElement.textContent = "Looks good!";
    hintElement.classList.remove("error");
    hintElement.classList.add("success");
  }
});

document.getElementById("email").addEventListener("input", function() {
  let email = this.value.trim();
  let emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  let hintElement = document.getElementById("email-hint");

  if (!emailRegex.test(email)) {
    hintElement.textContent = "Please enter a valid email address.";
    hintElement.classList.remove("success");
    hintElement.classList.add("error");
  } else {
    hintElement.textContent = "Email looks good!";
    hintElement.classList.remove("error");
    hintElement.classList.add("success");
  }
});

document.getElementById("password").addEventListener("input", function() {
  let password = this.value.trim();
  let passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*?&]{8,}$/;
  let hintElement = document.getElementById("password-hint");

  if (!passwordRegex.test(password)) {
    hintElement.textContent = "Password must be at least 8 characters long, with one letter and one number.";
    hintElement.classList.remove("success");
    hintElement.classList.add("error");
  } else {
    hintElement.textContent = "Strong password!";
    hintElement.classList.remove("error");
    hintElement.classList.add("success");
  }
});

document.getElementById("confirm-password").addEventListener("input", function() {
  let password = document.getElementById("password").value.trim();
  let confirmPassword = this.value.trim();
  let hintElement = document.getElementById("confirm-password-hint");

  if (password !== confirmPassword) {
    hintElement.textContent = "Passwords do not match.";
    hintElement.classList.remove("success");
    hintElement.classList.add("error");
  } else {
    hintElement.textContent = "Passwords match!";
    hintElement.classList.remove("error");
    hintElement.classList.add("success");
  }
});


const flashMessage = "{{ get_flashed_messages()|join(', ') }}"; 

if (flashMessage) {
  const flashMessageContainer = document.getElementById('flash-message-container');
  flashMessageContainer.innerHTML = `
    <div class="flash-message">
      <p>${flashMessage}</p>
    </div>
  `;
}