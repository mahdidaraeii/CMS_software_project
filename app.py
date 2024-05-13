from flask import Flask
from Controllers.controllers import bp as controllers_bp
from Models.models import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'

app.register_blueprint(controllers_bp)

db.init_app(app)


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()
