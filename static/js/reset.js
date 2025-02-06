document.addEventListener('DOMContentLoaded', function () {
  const passwordField = document.getElementById('password');
  const confirmPasswordField = document.getElementById('confirm_password');
  const form = document.querySelector('form'); // Assuming there's only one form

  // Toggle password visibility
  document.getElementById('toggle-password').addEventListener('click', function () {
      togglePasswordVisibility(passwordField);
  });

  document.getElementById('toggle-confirm-password').addEventListener('click', function () {
      togglePasswordVisibility(confirmPasswordField);
  });

  // Form submit event to validate the fields
  form.addEventListener('submit', function (event) {
      const password = passwordField.value.trim();
      const confirmPassword = confirmPasswordField.value.trim();

      let valid = true;

      // Clear previous error messages
      document.getElementById('password-hint').textContent = '';
      document.getElementById('confirm-password-hint').textContent = '';

      // Validate password strength
      const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*?&]{8,}$/;
      if (!password.match(passwordRegex)) {
          document.getElementById('password-hint').textContent = "Password must be at least 8 characters long, contain both letters and numbers.";
          valid = false;
      }

      // Validate passwords match
      if (password !== confirmPassword) {
          document.getElementById('confirm-password-hint').textContent = "Passwords do not match.";
          valid = false;
      }

      // Prevent form submission if invalid
      if (!valid) {
          event.preventDefault();
      }
  });

  // Function to toggle password visibility
  function togglePasswordVisibility(field) {
      if (field.type === 'password') {
          field.type = 'text';
      } else {
          field.type = 'password';
      }
  }
});
