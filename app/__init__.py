from flask import Flask, render_template

app = Flask(__name__)
app.config.from_pyfile('config.py')

from app.models.models import db
db.init_app(app)
with app.app_context():
    db.create_all()

from app.utils.migration import migrate
migrate.init_app(app, db)

from app.utils.sessions import session
session.init_app(app)

from app.utils.bcrypt import bcrypt
bcrypt.init_app(app)

from app.routes.auth import auth_bp
app.register_blueprint(auth_bp)

from app.routes.base import base_bp
app.register_blueprint(base_bp)


# Creating Error Pages
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title='404 ERROR'), 404
