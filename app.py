from flask import Flask, render_template, Response, request
import sqlite3
import cv2
from cryptography.fernet import Fernet

app = Flask(__name__)

# Veritabanını oluştur
def create_database():
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    email TEXT NOT NULL,
                    password TEXT NOT NULL,
                    faceData BLOB NOT NULL
                     )''')

    connection.commit()
    connection.close()

# Anahtar oluştur
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Veritabanına verileri eklemek için
def insert_data(username, email, password, faceData):
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    # Verileri şifrele
    encrypted_password = cipher_suite.encrypt(password.encode())
    encrypted_face_data = cipher_suite.encrypt(faceData.encode())

    cursor.execute("INSERT INTO users (username, email, password, faceData) VALUES (?, ?, ?, ?)",
                   (username, email, encrypted_password, encrypted_face_data))

    connection.commit()
    connection.close()

# Kullanıcıyı doğrula
def authenticate_user(username, password, faceData):
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    if user:
        stored_password = cipher_suite.decrypt(user[3]).decode()
        stored_face_data = cipher_suite.decrypt(user[4]).decode()
        if stored_password == password and stored_face_data == faceData:
            return user

    connection.close()
    return None

@app.route('/anasayfa')
def anasayfa():
    return render_template("index.html")

@app.route('/giris', methods=['GET', 'POST'])
def giris():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        face_data = request.form['faceData']
        
        user = authenticate_user(username, password, face_data)
        if user:
            return "Giriş başarılı! Kullanıcı adı: {}".format(username)
        else:
            return "Giriş başarısız! Kullanıcı adı, şifre veya yüz verisi yanlış!"
    else:
        return render_template("login.html")

@app.route('/kayit', methods=['GET', 'POST'])
def kayit():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        face_data = request.form['faceData']
        
        insert_data(username, email, password, face_data)
        return "Kullanıcı başarıyla kaydedildi!"
    else:
        return render_template("register.html")

# Yüz tanıma route'u
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

# Diğer route'lar devam ediyor...

if __name__ =="__main__":
    create_database()  # Uygulama başlatıldığında veritabanını oluştur
    app.run(debug=True)
