from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
from flask_app.models.user import User
bcrypt = Bcrypt(app)


@app.get('/')
def index():
    return render_template('index.html')


@app.post('/users/login')
def login():
    if not User.validate_login(request.form):
        return redirect('/')
    data = {
        'email': request.form['log_email']
    }
    user = User.get_by_email(data)
    if not user:
        flash('Email not found.', 'log_email')
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['log_password']):
        flash('Password invalid.', 'log_password')
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/wall')


@app.post('/users/register')
def register():
    if not User.validate_registration(request.form):
        return redirect('/')
    hashed = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': hashed
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect('/wall')


@app.get('/users/logout')
def logout():
    session.clear()
    return redirect('/')
