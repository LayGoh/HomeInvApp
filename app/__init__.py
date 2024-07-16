from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Initialize the Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Temporary key for development

# Initialize the database and migration tools
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initialize the login manager
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

# Import and register the blueprints
from app import routes, models, auth_routes
from app.auth_routes import auth_bp
app.register_blueprint(auth_bp, url_prefix='/auth')

# Define the user loader function
@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))

# Capitalize the first letter on Home Page
@app.template_filter('capitalize_first')
def capitalize_first(s):
    return s.capitalize()

app.jinja_env.filters['capitalize_first'] = capitalize_first