from pprint import pprint
from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.post import Post
from flask_app.models.post import Comment

def datetime_format(value, format="%B %-d"):
    return value.strftime(format)

app.add_template_filter(datetime_format)


@app.get('/wall')
def wall():
    if 'user_id' not in session:
        flash('Please log in or register.', 'login_error')
        return redirect('/')

    data = {
        'user_id': session['user_id']
    }
    user = User.get_one(data)
    posts = Post.get_all_with_users_and_comments()
    return render_template('wall.html', user=user, posts=posts)

@app.post('/posts/create')
def create_post():
    if not Post.validate(request.form):
        return redirect('/wall')

    Post.save(request.form)
    return redirect('/wall')

@app.post('/comments/create')
def create_comment():
    print('********')
    pprint(request.form)
    print('********')
    if not Comment.validate(request.form):
        return redirect('/wall')
    
    Comment.save(request.form)
    return redirect('/wall')
