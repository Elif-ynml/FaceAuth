document.addEventListener("DOMContentLoaded", function() {
    const loginButton = document.getElementById("login-btn");
    const registerButton = document.getElementById("register-btn");
  
    loginButton.addEventListener("click", function() {
      window.location.href = "login.html"; // Giriş sayfasına yönlendirme
    });
  
    registerButton.addEventListener("click", function() {
      window.location.href = "register.html"; // Kayıt sayfasına yönlendirme
    });
  });
  