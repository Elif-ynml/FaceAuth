from flask import Flask, render_template, request, app

app=Flask(__name__)

#anasayfa
@app.route('/anasayfa')
def anasayfa():
    return render_template("index.html")

#giriş yap
@app.route('/giris')
def giris():
    return render_template("login.html")

#kayıt ol
@app.route('/kayit')
def kayit():
    return render_template("register.html")

if __name__ =="__main__":
    app.run(debug=True)
