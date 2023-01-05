from flask_app import app

# import models here
from flask_app.models.user import User
from flask_app.models.post import Post
from flask_app.models.comment import Comment

# import controllers here
from flask_app.controllers import users, posts

if __name__ == '__main__':
    app.run(debug=True)
