from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)
username = 'Jon'
users = ['Karolina', 'Abdi', 'Rammi']


@app.get('/')
def index():
    return render_template("index.html")


@app.get('/user')
def user_get():
    return render_template("user.html", name=username, friends=users)


@app.post('/user')
def user_post():
    user_add = request.form['user_name']
    users.append(user_add)
    return redirect(url_for('user_get'))


@app.get('/mango')
def mango():
    return render_template("mango.html")

@app.get('/test')
def test():
    return render_template("mango.html")

if __name__ == '__main__':
    app.run()
