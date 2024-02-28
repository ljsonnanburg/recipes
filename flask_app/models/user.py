from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
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

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class User:
    DB = 'recipes'
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def save(cls,data):
        query = """
                INSERT INTO users 
                (first_name, last_name, email, password) 
                VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s)
                """
        return connectToMySQL(cls.DB).query_db(query,data)
    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.DB).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.DB).query_db(query,data)
        return cls(results[0])
    

    
    @staticmethod
    def validate_register(user):
        is_valid = True
        # For checking if user is trying to register a taken email address
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.DB).query_db(query,user)
        if len(user['first_name']) < 2:
            flash('First name must be at least 2 characters long', 'register')
            is_valid= False
        if user['first_name'].isalpha() == False:
            flash('First name must contain letters only', 'register')
            is_valid= False        
        if len(user['last_name']) < 2:
            flash('Last name must be at least 2 characters long', 'register')
            is_valid= False
        if user['last_name'].isalpha() == False:
            flash('Last name must contain letters only', 'register')
            is_valid= False
        if len(results) >= 1:
            flash('Email already taken.','email')
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash('Provided email not in a valid format','register')
            is_valid=False
        if len(user['password']) < 8:
            flash('Password must be at least 8 characters long','register')
            is_valid = False
        if user['password'] != user['confirm']:
            flash('Passwords must match','register')
            is_valid = False
        return is_valid



