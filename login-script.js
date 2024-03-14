document.addEventListener("DOMContentLoaded", function() {
    const loginForm = document.getElementById("login-form");
    const errorMessage = document.getElementById("error-message");
    const videoContainer = document.getElementById("video-container");
    const startCameraButton = document.getElementById("start-camera-btn");
    const registerButton = document.getElementById("register-btn");
    registerButton.addEventListener("click", function() {
        window.location.href = "register.html"; // Kayıt sayfasına yönlendirme
      });
    });


    let videoStream;

  startCameraButton.addEventListener("click", function() {
    startCamera();
  

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
        videoContainer.innerHTML = "";
        videoContainer.appendChild(video);
      })
      .catch(function(err) {
        console.error("Kamera erişimi reddedildi: ", err);
      });
  }

    
    
    loginForm.addEventListener("submit", function(event) {
      event.preventDefault();
  
      const username = document.getElementById("username").value;
      const password = document.getElementById("password").value;
      const faceData = document.getElementById("face").files[0];
  
      
      if (username === "doğru_kullanıcı_adı" && password === "doğru_şifre" && yüz_verisi_doğru_mu) {
         // Giriş başarılı
         window.location.href = "anasayfa.html";
      } else {
        errorMessage.textContent = "Kullanıcı adı, şifre veya yüz verisi yanlış.";
       }
  
    
      errorMessage.textContent = "Kullanıcı adı, şifre veya yüz verisi yanlış.";
    });
  });