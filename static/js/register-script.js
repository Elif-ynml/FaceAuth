document.addEventListener("DOMContentLoaded", function() {
    const registerForm = document.getElementById("register-form");
    const errorMessage = document.getElementById("error-message");
    const successMessage = document.getElementById("success-message");
    const loginButton = document.getElementById("login-btn");
    
    loginButton.addEventListener("click", function() {
        window.location.href = "/giris"; // Giriş sayfasına yönlendirme
      });
    
    let videoStream;
  
    const startCameraButton = document.getElementById("start-camera-btn");
  
    startCameraButton.addEventListener("click", function() {
      startCamera();
    });
  
    function startCamera() {
      navigator.mediaDevices.getUserMedia({ video: true })
        .then(function(stream) {
          videoStream = stream;
          const video = document.createElement("video");
          video.setAttribute("id", "video");
          video.setAttribute("width", "320");
          video.setAttribute("height", "240");
          video.srcObject = stream;
          video.autoplay = true;
          document.getElementById("video-container").innerHTML = "";
          document.getElementById("video-container").appendChild(video);
        })
        .catch(function(err) {
          console.error("Kamera erişimi reddedildi: ", err);
        });
    }
  
    registerForm.addEventListener("submit", function(event) {
      event.preventDefault();
  
      const username = document.getElementById("username").value;
      const password = document.getElementById("password").value;
      const email = document.getElementById("email").value;
      const faceData = "Yüz verisi"; // Yüz verisi olarak kabul ediyoruz
  
      
       fetch('/register', {
       method: 'POST',
       body: JSON.stringify({ username, password, email, faceData }),
       headers: {
          'Content-Type': 'application/json'
        }
       })
       .then(response => response.json())
       .then(data => {
         console.log('Kayıt başarılı:', data);
         
         window.location.href = "/giris"; // Giriş sayfasına yönlendir
       })
      .catch(error => {
         console.error('Kayıt sırasında hata:', error);
       // Kayıt sırasında hata oluştuğunda kullanıcıya bilgi verilebilir
       });
  
      console.log("Kullanıcı adı:", username);
      console.log("Şifre:", password);
      console.log("E-posta:", email);
      console.log("Yüz verisi:", faceData);
  
      // Örneğin, başarılı kayıt olduğunu varsayalım
      errorMessage.texxtContent ="Kayıt başarıyla tamamlanamadı";
      successMessage.textContent = "Kayıt başarıyla tamamlandı!";
       // Giriş sayfasına yönlendir
    });
  });