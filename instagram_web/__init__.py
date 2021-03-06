from app import app
from flask import render_template, session
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.sessions.views import sessions_blueprint
from instagram_web.blueprints.images.views import images_blueprint
from instagram_web.blueprints.transactions.views import transactions_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles
from models.user import User



assets = Environment(app)
assets.register(bundles)

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")
app.register_blueprint(images_blueprint, url_prefix="/images")
app.register_blueprint(transactions_blueprint, url_prefix="/images/<image_id>/transactions")

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route("/")
def home():
    #user = User.get_or_none(id=session['user_id'])
    return render_template('home.html')
