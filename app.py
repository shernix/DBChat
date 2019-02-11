from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/contacts')
def contacts():
    return render_template('contacts.html')


@app.route('/messaging')
def messaging():
    return render_template('messaging.html')


if __name__ == '__main__':
    app.run(debug=True)


