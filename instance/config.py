
import os


SECRET_KEY = 'p9Bv<3Eid9%$i01jge87rt32trig87'
basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
