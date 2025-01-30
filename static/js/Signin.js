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
