from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

DATABASE = 'cd_wall'


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.posts = []
        self.comments = []

    @staticmethod
    def validate_registration(form):
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        is_valid = True
        if len(form['first_name']) < 2:
            flash('First name must be at least two characters.', 'first_name')
            is_valid = False
        if len(form['last_name']) < 1:
            flash('Last name must be at least two characters.', 'last_name')
            is_valid = False
        if len(form['email']) < 1:
            flash('Please enter your email.', 'email')
            is_valid = False
        if not EMAIL_REGEX.match(form['email']):
            flash('Please enter a valid email.', 'email')
            is_valid = False
        if len(form['password']) < 8:
            flash('Please enter a password of at least eight characters.', 'password')
            is_valid = False
        if form['password'] != form['confirm_pw']:
            flash('Passwords do not match.', 'confirm_pw')
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login(form):
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        is_valid = True
        if len(form['log_email']) < 1:
            flash('Please enter your email.', 'log_email')
            is_valid = False
        if not EMAIL_REGEX.match(form['log_email']):
            flash('Please enter a valid email.', 'log_email')
            is_valid = False
        if len(form['log_password']) < 8:
            flash('Please enter a password of at least eight characters.',
                  'log_password')
            is_valid = False
        return is_valid

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);'
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_one(cls, data):
        query = 'SELECT * FROM users WHERE id = %(user_id)s;'
        results = connectToMySQL(DATABASE).query_db(query, data)
        user = User(results[0])
        return user

    @classmethod
    def get_by_email(cls, data):
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        results = connectToMySQL(DATABASE).query_db(query, data)
        if len(results) < 1:
            return None
        user = User(results[0])
        return user
