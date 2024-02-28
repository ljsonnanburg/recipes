from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
# Have import from mysqlconnection on every model for DB interactions
# Import the model's python file as a module, not the class directly so you avoid circular import errors!
# For example: from flask_app.models import table2_model

'''
! Note: If you are working with tables that are related to each other, 
!       you'll want to import the other table's class here for when you need to create objects with that class. 

! Example: importing pets so we can make pet objects for our users that own them.

Class should match the data table exactly that's in your DB.

REMEMBER TO PARSE DATA INTO OBJECTS BEFORE SENDING TO PAGES!

'''
class Recipe:
    DB = 'recipes'
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instruction = data['instruction']
        self.date_cooked = data['date_cooked']
        self.under_30 = data['under_30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user_name = data['first_name']

    @classmethod
    def save(cls,data):
        query = """
                INSERT INTO recipes 
                (name, description, instruction, under_30, user_id) 
                VALUES(%(name)s, %(description)s, %(instruction)s, %(under_30)s, %(user_id)s);
                """
        return connectToMySQL(cls.DB).query_db(query,data)
    
    @classmethod
    def save_comment(cls,data):
        query = """
                INSERT INTO comments
                (user_id, recipe_id, comment)
                VALUES (%(user_id)s, %(recipe_id)s, %(comment)s);
                """
        return connectToMySQL(cls.DB).query_db(query,data)
    @classmethod
    def get_all(cls):
        query = """
                SELECT * FROM recipes
                JOIN users 
                ON recipes.user_id = users.id;
                """
        recipes = []
        results = connectToMySQL(cls.DB).query_db(query)
        for row in results:
            recipes.append(cls(row))
        return recipes
    
    @classmethod
    def get_one(cls, data):
        query = """
                SELECT * FROM recipes
                JOIN users
                ON recipes.user_id = users.id
                WHERE recipes.id = %(id)s;
                """
        result = connectToMySQL(cls.DB).query_db(query, data)
        print(result)
        return cls(result[0])  # here result is a list.
    
    @classmethod
    def get_comments(cls, data):
        query = """
                SELECT * FROM recipes
                JOIN comments
                ON recipes.id = comments.recipe_id
                JOIN users
                ON users.id = comments.user_id
                WHERE recipes.id = %(id)s;
                """
        comments = []
        results = connectToMySQL(cls.DB).query_db(query, data)
        for row in results:
            comments.append(row)
        return comments
    
    @classmethod
    def obliterate_comments(cls, data):
        query = """
                DELETE FROM comments 
                WHERE recipe_id = %(id)s;
                """
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def delete_recipe(cls, data):
        query = """
                DELETE FROM recipes
                WHERE id = %(id)s;
                """
        return connectToMySQL(cls.DB).query_db(query, data)
    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        print(recipe)
        # For checking if user is trying to register a taken email address
        query = "SELECT * FROM recipes WHERE name = %(name)s;"
        results = connectToMySQL(Recipe.DB).query_db(query,recipe)
        if len(results) >= 1:
            flash('There is already a recipe with that name what are you trying to pull get out of here')
            is_valid = False

    
        return is_valid