from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'SAKLVJNASDLKJVNSDAKLJN'

    from .routes.home import home
    from .routes.auth import auth
    from .routes.menus import menus
    from .routes.orders import orders
    from .routes.restaurant import restaurant
    from .routes.restaurant_type import restaurant_type
    from .routes.users import users

    app.register_blueprint(home, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(menus, url_prefix='/')
    app.register_blueprint(orders, url_prefix='/')
    app.register_blueprint(restaurant, url_prefix='/')
    app.register_blueprint(restaurant_type, url_prefix='/')
    app.register_blueprint(users, url_prefix='/')

    return app