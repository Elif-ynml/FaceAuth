
import tkinter as tk
from tkinter import messagebox, simpledialog
import cv2
from PIL import Image, ImageTk
import sqlite3
import hashlib
import os
import base64
import re
import ctypes

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Ana Ekran")

        # Tam ekran ayarı
        self.root.attributes('-fullscreen', True)

        # Karanlık tema renkleri
        bg_color = "#333333"  # Arka plan rengi
        button_bg_color = "#2980B9"  # Buton arka plan rengi
        button_fg_color = "#FFFFFF"  # Buton metin rengi

        # Arka plan rengini ayarla
        self.root.config(bg=bg_color)

        # Butonları düzenle
        self.button_login = tk.Button(self.root, text="Giriş Yap", command=self.open_login_window, bg=button_bg_color, fg=button_fg_color, font=("Helvetica", 20))
        self.button_login.pack(pady=(20, 10))

        self.button_register = tk.Button(self.root, text="Kayıt Ol", command=self.open_register_window, bg=button_bg_color, fg=button_fg_color, font=("Helvetica", 20))
        self.button_register.pack(pady=10)

        self.button_exit = tk.Button(self.root, text="Çıkış", command=self.root.destroy, bg=button_bg_color, fg=button_fg_color, font=("Helvetica", 20))
        self.button_exit.pack(pady=10)

        # Butonları sayfanın ortasına hizala
        self.button_login.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        self.button_register.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.button_exit.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

    def open_login_window(self):
        self.root.withdraw()  # Ana ekranı gizle
        login_window = tk.Toplevel(self.root)
        app = LoginWindow(login_window, self.root)

    def open_register_window(self):
        self.root.withdraw()  # Ana ekranı gizle
        register_window = tk.Toplevel(self.root)
        app = RegisterWindow(register_window, self.root)

    def open_login_window(self):
        self.root.withdraw()  # Ana ekranı gizle
        login_window = tk.Toplevel(self.root)
        app = LoginWindow(login_window, self.root)

    def open_register_window(self):
        self.root.withdraw()  # Ana ekranı gizle
        register_window = tk.Toplevel(self.root)
        app = RegisterWindow(register_window, self.root)

class RegisterWindow:
    def __init__(self, root, main_window):
        self.root = root
        self.root.title("Kayıt Ekranı")
        self.main_window = main_window

        # Tam ekran ayarı
        self.root.attributes("-fullscreen", True)
        self.root.bind("<F11>", lambda event: self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen")))
        self.root.bind("<Escape>", lambda event: self.root.attributes("-fullscreen", False))

        # Ekranın ortasına yerleştir
        window_width = 400
        window_height = 400
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_coordinate = (screen_width - window_width) // 2
        y_coordinate = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

        # Arka plan rengi ve metin renkleri
        bg_color = "#1f1f1f"  # Karanlık tema için arka plan rengi
        text_color = "#FFFFFF"  # Beyaz renkli metinler
        button_bg_color = "#2980B9"  # Mavi tonlarında düğme arka plan rengi
        button_fg_color = "#FFFFFF"  # Beyaz renkli düğme metinleri

        # Arka plan rengini ayarla
        self.root.config(bg=bg_color)

        self.label_username = tk.Label(self.root, text="Kullanıcı Adı:", bg=bg_color, fg=text_color)
        self.label_username.pack(pady=10)
        self.entry_username = tk.Entry(self.root)
        self.entry_username.pack(pady=10)

        self.label_email = tk.Label(self.root, text="E-Posta:", bg=bg_color, fg=text_color)
        self.label_email.pack(pady=10)
        self.entry_email = tk.Entry(self.root)
        self.entry_email.pack(pady=10)

        self.label_password = tk.Label(self.root, text="Parola:", bg=bg_color, fg=text_color)
        self.label_password.pack(pady=10)
        self.entry_password = tk.Entry(self.root, show="*")
        self.entry_password.pack(pady=10)

        self.button_register = tk.Button(self.root, text="Kayıt Ol", command=self.register, bg="blue")
        self.button_register.pack(pady=10)

        self.label_photo = tk.Label(self.root)
        self.label_photo.pack(pady=10)

        self.camera = cv2.VideoCapture(0)
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.start_camera()  # Kamerayı başlat

        # Veritabanı bağlantısını oluştur
        self.conn = sqlite3.connect('users.db')
        self.cur = self.conn.cursor()
        self.create_table()


    def create_table(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY,
                            username TEXT,
                            email TEXT,
                            password TEXT,
                            face_photo_path TEXT)''')
        self.conn.commit()

    def register(self):
        # Kayıt işlemleri
        username = self.entry_username.get()
        email = self.entry_email.get()
        password = self.entry_password.get()

        if not username or not email or not password:
            messagebox.showerror("Hata", "Lütfen kullanıcı adı, e-posta ve parola girin.")
            return

        # E-posta formatını kontrol et
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Hata", "Geçersiz e-posta adresi.")
            return

        # Parolanın uzunluğunu ve karakter kullanımını kontrol et
        if len(password) < 8 or not re.search("[a-z]", password) or not re.search("[A-Z]", password) or not re.search("[0-9]", password):
            messagebox.showerror("Hata", "Parola en az 8 karakter uzunluğunda olmalı ve en az bir büyük harf, bir küçük harf ve bir rakam içermelidir.")
            return

        # Şifreyi hashle
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Kullanıcı adının veritabanında daha önce kaydedilip kaydedilmediğini kontrol et
        self.cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        existing_username = self.cur.fetchone()
        if existing_username:
            messagebox.showerror("Hata", "Bu kullanıcı adı zaten mevcut. Lütfen farklı bir kullanıcı adı seçin.")
            return

        # E-postanın veritabanında daha önce kaydedilip kaydedilmediğini kontrol et
        self.cur.execute("SELECT * FROM users WHERE email = ?", (email,))
        existing_email = self.cur.fetchone()
        if existing_email:
            messagebox.showerror("Hata", "Bu e-posta adresi zaten mevcut. Lütfen farklı bir e-posta adresi girin.")
            return

        ret, frame = self.camera.read()
        if ret:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray_frame, 1.3, 5)
            if len(faces) == 0:
                messagebox.showerror("Hata", "Lütfen yüzünüzü kameraya gösterin.")
                return

            # Yeni kullanıcıya ait fotoğrafı kaydet
            face_photo_path = f"faces/{username}.jpg"
            cv2.imwrite(face_photo_path, gray_frame)

            # Yüz resminin daha önce kaydedilip kaydedilmediğini kontrol et
            self.cur.execute("SELECT * FROM users")
            users = self.cur.fetchall()
            for user in users:
                saved_face_photo_path = user[4]
                if saved_face_photo_path == face_photo_path:
                    messagebox.showerror("Hata", "Bu yüz resmi zaten kullanımda. Lütfen farklı bir resim seçin.")
                    os.remove(face_photo_path)  # Kaydedilen resmi sil
                    return

            # Yüz resminin yolunu şifrele
            encrypted_path = self.encrypt_path(face_photo_path)

            # Kullanıcıyı veritabanına kaydet
            self.cur.execute("INSERT INTO users (username, email, password, face_photo_path) VALUES (?, ?, ?, ?)",
                            (username, email, hashed_password, encrypted_path))
            self.conn.commit()
            messagebox.showinfo("Bilgi", "Kayıt Başarıyla Gerçekleştirildi.")
            self.close_window()  # Kayıt penceresini kapat ve ana ekranı dön

    def encrypt_path(self, path):
        # Yolun base64 kodlamasını yap ve şifrelenmiş haliyle döndür
        encrypted_path = base64.b64encode(path.encode()).decode()
        return encrypted_path

    def close_window(self):
            self.root.destroy()
            self.main_window.deiconify()  # Ana ekranı göster

    def start_camera(self):
        ret, frame = self.camera.read()
        if ret:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray_frame, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                photo = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                photo.thumbnail((400, 400))
                photo = ImageTk.PhotoImage(photo)
                self.label_photo.config(image=photo)
                self.label_photo.image = photo
            self.root.after(10, self.start_camera)


class LoginWindow:
    def __init__(self, root, main_window):
        self.root = root
        self.root.title("Giriş Ekranı")
        self.main_window = main_window

        # Ekran boyutunu al
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Ekranın ortasına yerleştir
        window_width = 400
        window_height = 300
        x_coordinate = (screen_width - window_width) // 2
        y_coordinate = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

        self.label_username = tk.Label(self.root, text="Kullanıcı Adı:")
        self.label_username.pack(pady=10)
        self.entry_username = tk.Entry(self.root)
        self.entry_username.pack(pady=10)

        self.label_password = tk.Label(self.root, text="Parola:")
        self.label_password.pack(pady=10)
        self.entry_password = tk.Entry(self.root, show="*")
        self.entry_password.pack(pady=10)

        self.button_login = tk.Button(self.root, text="Giriş Yap", command=self.login, bg="red")
        self.button_login.pack(pady=10)

        self.label_photo = tk.Label(self.root)
        self.label_photo.pack(pady=10)

        self.camera = cv2.VideoCapture(0)
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.start_camera()  # Kamerayı başlat

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if not username or not password:
            messagebox.showerror("Hata", "Lütfen kullanıcı adı ve parola girin.")
            return

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Kullanıcı adı ve parolayı veritabanında kontrol et
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cur.fetchone()
        conn.close()

        if user:
            if hashed_password == user[3]:
                messagebox.showinfo("Başarılı", f"Hoş Geldiniz, {username}!")
                self.close_window()
                self.open_welcome_window(username)
            else:
                messagebox.showerror("Hata", "Kullanıcı adı veya parola hatalı.")
        else:
            messagebox.showerror("Hata", "Kullanıcı adı veya parola hatalı.")

    def open_welcome_window(self, username):
        welcome_window = tk.Toplevel(self.root)
        welcome_window.title("Hoş Geldiniz")
        label_welcome = tk.Label(welcome_window, text=f"Hoş Geldiniz, {username}!")
        label_welcome.pack(padx=20, pady=20)
        button_close = tk.Button(welcome_window, text="Ana Ekrana Dön", command=welcome_window.destroy)
        button_close.pack(pady=10)

    def close_window(self):
        self.root.destroy()
        self.main_window.deiconify()  # Ana ekranı göster

    def start_camera(self):
        ret, frame = self.camera.read()
        if ret:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray_frame, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                photo = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                photo.thumbnail((400, 400))
                photo = ImageTk.PhotoImage(photo)
                self.label_photo.config(image=photo)
                self.label_photo.image = photo
            self.root.after(10, self.start_camera)

if __name__ == "__main__":
    os.makedirs('faces', exist_ok=True)

    # Ana ekran boyutunu al
    user32 = ctypes.windll.user32
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)

    root = tk.Tk()
    root.geometry(f"{screen_width}x{screen_height}+0+0")
    main_window = MainWindow(root)
    root.mainloop()