from code.app_flask_restful import app
from code.db import db

db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()
