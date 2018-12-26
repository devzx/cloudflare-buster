from flask import Flask

from src.views.site import site_blueprint


app = Flask(__name__)
app.config.from_object('config')
app.register_blueprint(site_blueprint)
