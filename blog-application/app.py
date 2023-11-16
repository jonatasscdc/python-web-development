from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(_name_)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), unique=True, nullable=False)
  password = db.Column(db.String(120), nullable=False)

@app.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
    name = request.form['name']
    password = generate_password_hash(request.form['password'])
    user = User(name=name, password=password)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('login'))
return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    user = User.query.filter_by(name=request.form['name']).first()
    if user and check_password_hash(user.password, request.form['password']):
      return redirect(url_for('home'))
    return render_template('login.html')

if __name__ == '__main__':
  db.create_all()
  app.run(debug=True)
