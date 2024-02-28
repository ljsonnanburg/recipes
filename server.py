from flask_app import app

# =========================================================
# REMEMBER TO IMPORT CONTROLLERS INTO YOUR SERVER FILE!
# =========================================================

# from flask_app.controllers import
from flask_app.controllers import users
from flask_app.controllers import recipes
# RUN pipenv install PyMySQL flask flask-bcrypt
# REMEMBER TO SAVE YOUR .mwb FILE TO THE FOLDER!

if __name__ == "__main__":
    app.run(debug=True)
