from pprint import pprint
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User
from flask_app.models.comment import Comment

DATABASE = 'cd_wall'


class Post:
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.poster = data['poster']
        self.comments = []

    @staticmethod
    def validate(form):
        is_valid = True
        if len(form['content']) < 5:
            flash('Post must be at least five characters.', 'post_content')
            is_valid = False
        return is_valid

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO posts (user_id, content) VALUES (%(user_id)s, %(content)s);'
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_all_with_users_and_comments(cls):
        query = 'SELECT id from posts;'
        post_ids = connectToMySQL(DATABASE).query_db(query)
        # pprint(post_ids)
        posts = []
        for post_id in post_ids:
            data = {
                'post_id': post_id['id']
            }
            post = Post.get_one_with_poster_and_comments(data)
            posts.append(post)
        return posts

    @classmethod
    def get_one_with_poster_and_comments(cls, data):
        # print(f'******** DATA: {data} ********')
        query = 'SELECT * FROM posts JOIN users ON posts.user_id = users.id LEFT JOIN comments ON posts.id = comments.post_id WHERE posts.id = %(post_id)s;'
        results = connectToMySQL(DATABASE).query_db(query, data)
        
        # get the poster
        poster_data = {
            'user_id': results[0]['user_id']
        }
        poster = User.get_one(poster_data)

        # create post data
        post_data = {
            'id': results[0]['id'],
            'user_id': results[0]['user_id'],
            'content': results[0]['content'],
            'created_at': results[0]['created_at'],
            'updated_at': results[0]['updated_at'],
            'poster': poster
        }
        post = Post(post_data)

        # are there comments for this post?
        if results[0]['comments.id']:
            for result in results:
                data = {
                    'comment_id': result['comments.id']
                }
                comment = Comment.get_one_with_commenter(data)
                post.comments.append(comment)

        return post
