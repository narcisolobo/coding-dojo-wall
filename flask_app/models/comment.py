from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User

DATABASE = 'cd_wall'


class Comment:
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.post_id = data['post_id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.commenter = data['commenter']

    @staticmethod
    def validate(form):
        is_valid = True
        if len(form['content']) < 5:
            flash('Comment must be at least five characters.', 'comment_content')
            is_valid = False
        return is_valid

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO comments (user_id, post_id, content) VALUES (%(user_id)s, %(post_id)s, %(content)s);'
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_one_with_commenter(cls, data):
        query = 'SELECT * FROM comments JOIN users ON comments.user_id = users.id WHERE comments.id = %(comment_id)s;'
        results = connectToMySQL(DATABASE).query_db(query, data)

        # get the commenter
        commenter_data = {
            'user_id': results[0]['user_id']
        }
        commenter = User.get_one(commenter_data)

        # create comment data
        comment_data = {
            'id': results[0]['id'],
            'user_id': results[0]['user_id'],
            'post_id': results[0]['post_id'],
            'content': results[0]['content'],
            'created_at': results[0]['created_at'],
            'updated_at': results[0]['updated_at'],
            'commenter': commenter
        }
        comment = Comment(comment_data)
        return comment
