from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

@app.route('/signup', methods=['GET', 'POST'])
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'], method='pbkdf2:sha256')

        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            error = 'Username already exists, please choose a different one.'
        else:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))

    return render_template('signup.html', error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        return 'Invalid username or password'
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return 'Welcome to your dashboard!'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creates the database tables within the app context
    app.run(debug=True, host='0.0.0.0', port=5000)
