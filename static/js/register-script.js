document.addEventListener("DOMContentLoaded", function() {
  const registerForm = document.getElementById("register-form");
  const errorMessage = document.getElementById("error-message");
  const successMessage = document.getElementById("success-message");
  const loginButton = document.getElementById("login-btn");

  loginButton.addEventListener("click", function() {
      window.location.href = "/giris"; // Giriş sayfasına yönlendirme
  });

  let videoStream;
  let canvas = document.getElementById("canvas");
  let context = canvas.getContext("2d");

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

              detectFace();
          })
          .catch(function(err) {
              console.error("Kamera erişimi reddedildi: ", err);
          });
  }

  function detectFace() {
      const video = document.getElementById("video");
      const faceDataInput = document.getElementById("faceData");
      const inputWidth = video.videoWidth;
      const inputHeight = video.videoHeight;

      canvas.width = inputWidth;
      canvas.height = inputHeight;

      context.clearRect(0, 0, canvas.width, canvas.height);
      context.drawImage(video, 0, 0, inputWidth, inputHeight);

      const faceData = canvas.toDataURL("image/jpeg");

      // Yüz verisini form alanına ekleyin
      faceDataInput.value = faceData;

      requestAnimationFrame(detectFace);
  }

  registerForm.addEventListener("submit", function(event) {
      event.preventDefault();

      const username = document.getElementById("username").value;
      const password = document.getElementById("password").value;
      const email = document.getElementById("email").value;
      const faceData = document.getElementById("faceData").value;

      // Kayıt formunu gönder
      fetch('/kayit', {
          method: 'POST',
          body: new FormData(registerForm), // Form verilerini direkt olarak gönder
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
      errorMessage.textContent = "Kayıt başarıyla tamamlanamadı";
      successMessage.textContent = "Kayıt başarıyla tamamlandı!";
  });
});
