from flask import Flask, render_template, Response, request
import sqlite3
import cv2

app = Flask(__name__)

# Veritabanını oluştur
def create_database():
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT NOT NULL,
                    email TEXT NOT NULL,
                    password TEXT NOT NULL,
                    faceData BLOB NOT NULL
                     )''')

    connection.commit()
    connection.close()

# Veritabanına verileri eklemek için
def insert_data(username, email, password, faceData):
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    cursor.execute("INSERT INTO users (username, email, password, faceData) VALUES (?, ?, ?, ?)", (username, email, password, faceData))

    connection.commit()
    connection.close()

# Kullanıcıyı doğrula
def authenticate_user(username, password, faceData):
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM users WHERE username=? AND password=? AND faceData=?", (username, password, faceData))
    user = cursor.fetchone()

    connection.close()

    return user

@app.route('/anasayfa')
def anasayfa():
    return render_template("index.html")

@app.route('/giris')
def giris():
    return render_template("login.html")

@app.route('/kayit')
def kayit():
    return render_template("register.html")

@app.route('/video_feed')
def video_feed():
    camera = cv2.VideoCapture(0)

    def generate_frames():
        while True:
            success, frame = camera.read()
            if not success:
                break
            else:
                # Yüz tespiti için OpenCV kullanarak kameradan alınan görüntüyü işle
                face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)

                # Tespit edilen yüzlerin etrafına dikdörtgen çiz
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

                # Görüntüyü JPEG formatında encode et
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()

                # Flask'a göndermek için frame'i yield et
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    # Flask'a görüntü verilerini döndürmek için Response objesi kullan
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/form', methods=['GET', 'POST'])
def form_verileri():
    if request.method == 'POST':
        # POST isteği ile gönderilen form verilerini alın
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        face_data = request.form['faceData']  # Eğer yüz verisi de gönderiliyorsa, bu şekilde alınabilir
        
        # Bu verileri bir HTML sayfasında göstermek için render_template fonksiyonunu kullanın
        return render_template('form.html', username=username, password=password, email=email, face_data=face_data)
    elif request.method == 'GET':
        # GET isteği ile erişildiğinde, boş bir form gösterilebilir veya başka bir işlem yapılabilir
        return render_template('form.html')  # Örnek olarak form.html'i gösteriyoruz

if __name__ =="__main__":
    create_database()  # Uygulama başlatıldığında veritabanını oluştur
    app.run(debug=True)
