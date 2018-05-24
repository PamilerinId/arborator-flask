from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_utils import ChoiceType

from app import db, login_manager

class User(UserMixin, db.Model):
    ACCESS = [
    (0, 'guest'),
    (1, 'user'),
    (2, 'admin'),
    (3, 'super')]

    ROLES =  [(0, 'annotator'), (1, 'validator')]

    ## TODO: alembic migration conflict with choicetype


    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    auth_provider = db.Column(db.String(256))
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    family_name = db.Column(db.String(60), index=True)
    picture_url = db.Column(db.String(128), index=True)
    access_level= db.Column(db.Integer, default=0)
    role =db.Column(db.Integer)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    todos = db.relationship('Todo', backref='txt_todos')
    created_date = db.Column(db.DateTime)
    last_seen = db.Column(db.DateTime) 
    # is_admin = db.Column(db.Boolean, default=False)

    def is_admin(self):
        return self.access == ACCESS['admin']

    def is_super(self): ##Might not be necessary eventually
        ##check emails in preset email array
        return self.access == ACCESS['super']
    
    def allowed(self, level):
        return self.access >= level

    def __repr__(self):
        return '<user: {}>'.format(self.username)

    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


## TODO: ManytoMany reltnshp btwn user/proj


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(150))
    users = db.relationship('User', backref='project_user',lazy='dynamic')
    texts = db.relationship('Text', backref='project_text',lazy='dynamic')



class Text(db.Model):
    __tablename__ = 'texts'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    textname = db.Column(db.Text, unique=True)
    nrtokens = db.Column(db.Integer)
    sentences = db.relationship('Sentence', backref='text_sentence')
    sentencesearches = db.relationship('SentenceSearch', backref='text_search')
    todos = db.relationship('Todo', backref='text_todo')
    exos = db.relationship('Exo', backref='text_exo')


class Sentence(db.Model):
    __tablename__ = 'sentences'

    id = db.Column(db.Integer, primary_key=True) 
    text_id = db.Column(db.Integer, db.ForeignKey('texts.id'))   
    nr = db.Column(db.Integer)
    sentence = db.Column(db.Text)
    trees = db.relationship('Tree', backref='tree')
    features= db.relationship('SentenceFeature', backref='sentence_feature')
    

class SentenceSearch(db.Model):
    __tablename__ = 'sentencesearch'
    
    id = db.Column(db.Integer, primary_key=True)
    nr = db.Column(db.Integer)
    sentence = db.Column(db.Text)
    textid = db.Column(db.Integer, db.ForeignKey('texts.id'))

class Tree(db.Model):
    __tablename__ = 'trees'
    
    id = db.Column(db.Integer, primary_key=True)
    sentenceid = db.Column(db.Integer, db.ForeignKey('sentences.id'))
    status = db.Column(db.Text)
    comment = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)
    features = db.relationship('Feature', backref='tree_feature')
    links = db.relationship('Link', backref='tree_link')

class Feature(db.Model):
    __tablename__ = 'features'

    id = db.Column(db.Integer, primary_key=True)
    treeid = db.Column(db.Integer, db.ForeignKey('trees.id'))
    nr = db.Column(db.Integer, primary_key=True)
    attr = db.Column(db.Text, primary_key=True)
    value = db.Column(db.Text)

class SentenceFeature(db.Model):
    __tablename__ = 'sentencefeatures'
   
    id = db.Column(db.Integer, primary_key=True)
    sentenceid= db.Column(db.Integer, db.ForeignKey('sentences.id'), primary_key=True)
    attr = db.Column(db.Text)
    value = db.Column(db.Text)

class Link(db.Model):
    __tablename__ = 'links'

    id = db.Column(db.Integer, primary_key=True)
    treeid = db.Column(db.Integer, db.ForeignKey('trees.id'))
    depid = db.Column(db.Integer)
    govid = db.Column(db.Integer)
    function = db.Column(db.Text)

class Todo(db.Model):
    __tablename__ = 'todos'

    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('users.id'))
    textid = db.Column(db.Integer, db.ForeignKey('texts.id'))
    status = db.Column(db.Text)
    comment = db.Column(db.Text)

class Exo(db.Model):
    __tablename__ = 'exo'

    id = db.Column(db.Integer, primary_key=True)
    textid = db.Column(db.Integer, db.ForeignKey('texts.id'))
    type = db.Column(db.Integer)
    exotoknum = db.Column(db.Integer)
    status = db.Column(db.Text)
    comment = db.Column(db.Text)

# class ExoUserSentence(db.Model):
#     textid = db.Column(db.Integer, db.ForeignKey('texts.id'))
#     userid = db.Column(db.Integer, db.ForeignKey('users.id'))
#     sentenceid = db.Column(db.Integer, db.ForeignKey('sentences.id'))

