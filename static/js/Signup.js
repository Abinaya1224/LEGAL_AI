document.querySelector('.form').addEventListener('submit', function (event) {
    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm-password').value;
    
  
    if (!name || !email || !password || !confirmPassword || !terms) {
      alert('Please fill out all fields and agree to the terms.');
      event.preventDefault(); // Prevent form submission
    } else if (password !== confirmPassword) {
      alert('Passwords do not match.');
      event.preventDefault(); // Prevent form submission
    }
  });
  