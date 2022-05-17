from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

class Food:
    def __init__(self,data):
        self.id = data["id"]
        self.state = data["state"]
        self.city = data['city']
        self.restaraunt = data["restaraunt"]
        self.dish = data["dish"]
        self.descRev = data["descRev"]
        self.rating = data["rating"]
        self.user_id = data["user_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        # self.creator = None
    
    @classmethod
    def save(cls,data):
        query = "INSERT INTO foods(state, city, restaraunt, dish, descRev, rating, user_id) VALUES (%(state)s,%(city)s,%(restaraunt)s,%(dish)s,%(descRev)s,%(rating)s,%(user_id)s);"
        print("Saved!")
        return connectToMySQL("foodiesAdventure").query_db(query,data)
    
    @classmethod
    def update(cls,data):
        query = "UPDATE foods SET state = %(state)s, city = %(city)s, restaraunt = %(restaraunt)s, dish = %(dish)s, descREv = %(descRev)s, rating = %(rating)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL("foodiesAdventure").query_db(query,data)
    
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM foods where id = %(id)s;"
        return connectToMySQL("foodiesAdventure").query_db(query,data)

    @classmethod
    def show_one(cls,data):
        query = "SELECT * FROM foods WHERE id = %(id)s;"
        result = connectToMySQL("foodiesAdventure").query_db(query,data)
        return cls(result[0])
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM foods;"
        result = connectToMySQL("foodiesAdventure").query_db(query)
        all_foods = []
        for row in result:
            all_foods.append(cls(row))
        return all_foods

    @classmethod
    def get_by_state(cls,data):
        query = "SELECT * FROM foods WHERE state = %(state)s ORDER BY city ASC;"
        result = connectToMySQL("foodiesAdventure").query_db(query, data)
        food_by_state = []
        for row in result:
            food_by_state.append(cls(row))
        return food_by_state

    @staticmethod
    def validate_food(food):
        is_valid = True
        if len(food['state']) < 1:
            is_valid = False
            flash("State must be atleast 2 characters", 'foods')
        if len(food['city']) < 1:
            is_valid = False
            flash("City must be at least 2 characters long", 'foods')
        if len(food['restaraunt']) < 1:
            is_valid = False
            flash("Restaraunt must be atleast 2 characters", 'foods')
        if len(food['dish']) < 1:
            is_valid = False
            flash("Dish name must be atleast 2 characters", 'foods')
        if len(food['descRev']) < 1:
            is_valid = False
            flash("Description/Review must be atleast 2 characters", 'foods')
        return is_valid