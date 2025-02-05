document.addEventListener("DOMContentLoaded", () => {
  const slides = document.querySelectorAll(".slide");
  const dots = document.querySelectorAll(".dot");
  let currentSlide = 0;
  const intervalTime = 4000; // Rotation time in milliseconds
  let slideInterval;

  const showSlide = (index) => {
    slides.forEach((slide, i) => {
      slide.classList.toggle("active", i === index);
      dots[i].classList.toggle("active", i === index);
    });
  };

  const nextSlide = () => {
    currentSlide = (currentSlide + 1) % slides.length;
    showSlide(currentSlide);
  };

  const startSlideInterval = () => {
    slideInterval = setInterval(nextSlide, intervalTime);
  };

  const stopSlideInterval = () => {
    clearInterval(slideInterval);
  };

  dots.forEach((dot, i) => {
    dot.addEventListener("click", () => {
      currentSlide = i;
      showSlide(currentSlide);
      stopSlideInterval(); // Stop auto-rotation when the user interacts
      startSlideInterval(); // Restart auto-rotation
    });
  });

  // Start the slider rotation
  startSlideInterval();
});



document.querySelector(".form").addEventListener("submit", function(event) {
    let email = document.getElementById("email").value;
    let password = document.getElementById("password").value;
    let emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/; // Basic email format validation
    let passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*?&]{8,}$/; // Min 8 chars, 1 letter, 1 number

    if (!emailRegex.test(email)) {
        alert("Please enter a valid email address.");
        event.preventDefault(); // Stop form submission
    } else if (!passwordRegex.test(password)) {
        alert("Password must be at least 8 characters long and include at least one letter and one number.");
        event.preventDefault(); // Stop form submission
    }
});

// Get the elements for both password fields and eye icons
document.addEventListener("DOMContentLoaded", function () {
  // Add event listener for both the 'New Password' and 'Confirm Password' fields
  document.querySelectorAll(".toggle-password").forEach((toggle) => {
      toggle.addEventListener("click", function () {
          // Get the associated password input field
          const passwordInput = this.previousElementSibling;  

          // Toggle the password visibility
          if (passwordInput.type === "password") {
              passwordInput.type = "text";  // Show password
              this.classList.replace("fa-eye", "fa-eye-slash");  // Change icon to 'eye-slash'
          } else {
              passwordInput.type = "password";  // Hide password
              this.classList.replace("fa-eye-slash", "fa-eye");  // Change icon back to 'eye'
          }
      });
  });
});




