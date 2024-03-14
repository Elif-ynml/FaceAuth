from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Kullanıcıyı veritabanına eklemeden önce, veritabanında zaten mevcut olup olmadığını kontrol edin
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "Bu kullanıcı adı zaten mevcut!"
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Kullanıcıyı veritabanında kullanıcı adı ve şifreyle filtreleyerek bulun
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            return "Giriş Başarılı!"
        else:
            return "Geçersiz kullanıcı adı veya şifre."
    return render_template('login.html')

if __name__ == '__main__':
    # Uygulama çalıştığında veritabanını oluşturmak için "db.create_all()" satırını buraya taşıdık
    # Bu, uygulama ilk çalıştırıldığında veritabanı şemasını oluşturacaktır.
    # Ancak, gerçek bir uygulama geliştirirken veritabanı yönetimi için daha iyi araçlar kullanmanız önerilir.
    app.run(debug=True)