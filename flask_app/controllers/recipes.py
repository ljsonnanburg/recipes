from flask import render_template, redirect, request, session, flash
from flask_app import app

from flask_bcrypt import Bcrypt  # Only needed on routes related to login/reg
bcrypt = Bcrypt(app)

# Import Your Models as Classes into the Controller to use their Classmethods

# from flask_app.models.table_model import classname
from flask_app.models.user import User
from flask_app.models.recipe import Recipe

# ====================================
#    Create Routes
#    Show Form Route, Submit Form Route
# ====================================
@app.route('/recipes/new')
def create_recipe():

    
    return render_template('create_recipe.html')

@app.route('/recipes/create', methods=['POST'])
def actually_create_recipe_for_real_this_time_i_promise():
    if Recipe.validate_recipe(request.form):
        recipe_data = {
            'name': request.form['name'],
            'description': request.form['description'],
            'instruction': request.form['instruction'],
            'date_cooked': request.form['date_cooked'],
            'under_30': request.form['under_30'],
            'user_id': session['user_id']
        }
        # recipe_data = {**request.form}
        # recipe_data['user_id'] = session['user_id']
        Recipe.save(recipe_data)
        session['description'] = ''
    else:
        session['description'] = request.form['description']
        return redirect('/recipes/new')

    return redirect('/dashboard')

@app.route('/recipes/<int:recipe_id>/add_comment', methods=['POST'])
def add_comment(recipe_id):
    comment_data = {
        'comment': request.form['comment'],
        'user_id': session['user_id'],
        'recipe_id': recipe_id,

    }
    Recipe.save_comment(comment_data)
    return redirect('/recipes/{}'.format(recipe_id))
# ====================================
# Log In Validations Route
# ====================================


# ====================================
#    Read Routes
#    Show Routes (Get All and Get One)
# ====================================
@app.route('/recipes/<int:recipe_id>')
def show_recipe(recipe_id):
    data = {
        'id': recipe_id
    }
    recipe = Recipe.get_one(data)
    comments = Recipe.get_comments(data)
    print('check it out, this should be comments:{}'.format(comments))
    return render_template("show_recipe.html", recipe = recipe, comments=comments)
# ====================================
#    Update Routes
#    Update Form Route, Submit Update Form Route
# ====================================


# ====================================
#    Delete Routes
# ====================================
