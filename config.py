import os
basedir=os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED=True
SECRET_KEY='asdadasdqwd121'

SQLALCHEMY_DATABASE_URI='sqlite:///'+os.path.join(basedir,'app.db')
SQLALCHEMY_MIGRATE_REPO=os.path.join(basedir,'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True
