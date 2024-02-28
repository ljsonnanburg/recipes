from flask import render_template, redirect, request, session, flash
from flask_app import app

from flask_bcrypt import Bcrypt  # Only needed on routes related to login/reg
bcrypt = Bcrypt(app)

# Import Your Models as Classes into the Controller to use their Classmethods

# from flask_app.models.table_model import classname
from flask_app.models.user import User
from flask_app.models.recipe import Recipe

@app.route('/')
def index():
    return render_template('index.html')

# ====================================
#    Create Routes
#    Show Form Route, Submit Form Route
# ====================================
@app.route('/register', methods=["POST"])
def create_user():
    
    print(request.form)
    if User.validate_register(request.form):
    # if True:
        redirect('/')
        user_data ={
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
        }
        print(user_data)
        print('saving user data')
        User.save(user_data)
        print('saved user data')
    
    return redirect('/')

# ====================================
# Log In Validations Route
# ====================================
@app.route('/login',methods=['POST'])
def login():
    print(request.form)
    user = User.get_by_email(request.form)
    if not user:
        flash("Invalid Email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session['user_id'] = user.id
    session['first_name'] = user.first_name
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
# ====================================
#    Read Routes
#    Show Routes (Get All and Get One)
# ====================================
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template("dashboard.html", user=User.get_by_id(data), 
                        recipes = Recipe.get_all())

# ====================================
#    Update Routes
#    Update Form Route, Submit Update Form Route
# ====================================


# ====================================
#    Delete Routes
# ====================================
