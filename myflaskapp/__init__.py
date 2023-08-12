from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# initialize the database, login_manager and migrate
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # your database URI might be different depending on your setup
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
    
    # Set the secret key
    app.secret_key = 'key1'

    # initialize database, login_manager and migrate with app
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # set login_view (the name of the route that logs users in)
    login_manager.login_view = 'views.login'
    
    # import and register blueprints
    from .views import views
    app.register_blueprint(views)

    return app
