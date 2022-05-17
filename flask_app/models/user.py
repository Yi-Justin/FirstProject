from unittest import result
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import food
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash 

class User:
    def __init__(self,data):
        self.id = data["id"]
        self.username = data["username"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        # self.foods = []

    @classmethod
    def save (cls,data):
        query = "INSERT INTO users(username, email, password) VALUES ( %(username)s, %(email)s, %(password)s);"
        return connectToMySQL("foodiesAdventure").query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL("foodiesAdventure").query_db(query)
        users = []
        for row in results:
            users.append(cls(row))
        return users

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('foodiesAdventure').query_db(query,data)
        return cls(results[0])

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL("foodiesAdventure").query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    # @classmethod
    # def get_users_with_foods(cls, data):
    #     query = "SELECT * FROM users LEFT JOIN foods ON foods.user_id = users.id WHERE users.id = %(id)s;"
    #     results = connectToMySQL("foodiesadventure").query_db(query, data)
    #     user = cls(results[0])
    #     for row in results:
    #         food_data = {
    #             'id' : row["foods.id"],
    #             'state':row['state'],
    #             'city':row['city'],
    #             'restaraunt':row['restaraunt'],
    #             'dish': row['dish'],
    #             'descRev': row['descRev'],
    #             "rating": row ['rating'],
    #             'created_at': row ['foods.created_at'],
    #             'updated_at': row ['foods.updated_at']
    #         }
    #         user.foods.append(food.Food(food_data))
    #         return user

    @staticmethod
    def validate_reg(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL("foodiesAdventure").query_db(query,user)
        if len(results) >=1:
            flash("Email already taken","register")
            is_valid = False
        if len(user['username']) < 3:
            flash('Username must be at least 3 characters.', 'register')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email address", 'register')
            is_valid = False
        if len(user['password']) < 8:
            flash('Password must be at least 8 characters.', 'register')
            is_valid = False
        if user['password'] != user['confirm']:
            flash('Passwords do not match', 'register')
        return is_valid