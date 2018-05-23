from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_utils import ChoiceType

from app import db

class User(UserMixin, db.Model):
    ACCESS = [
    (0, 'guest'),
    (1, 'user'),
    (2, 'admin'),
    (3, 'super_admin')]

    ROLES =  [(0, 'annotator'), (1, 'validator')]


    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    auth_provider = db.Column(db.String(256))
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    family_name = db.Column(db.String(60), index=True)
    picture_url = db.Column(db.String(128), index=True)
    access_level= db.Column(ChoiceType(ACCESS), default=0)
    role =db.Column(ChoiceType(ROLES), nullable = True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    tree_id = db.Column(db.Integer, db.ForeignKey('trees.id'))
    created_date = db.Column(db.DateTime)
    last_seen = db.Column(db.DateTime) 
    # is_admin = db.Column(db.Boolean, default=False)

    def is_admin(self):
        return self.access == ACCESS['admin'] or ACCESS['super_admin']

    def is_super(self): ##Might not be necessary eventually
        ##check emails in preset email array
        return self.access == ACCESS['super_admin']
    
    def allowed(self, level):
        return self.access >= level

    def __repr__(self):
        return '<user: {}>'.format(self.username)

    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))





class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(150))
    users = db.relationship('User', backref='project',lazy='dynamic')
    text = db.Column(db.Integer, db.ForeignKey('texts.id'))



class Text(db.Model):
    __tablename__ = 'texts'
    
    id = db.Column(db.Integer, primary_key=True)
    project = db.relationship('Project', backref='text', lazy=True)
    textname = db.Column(db.Text, unique=True)
    nrtokens = db.Column(db.Integer)
    sentences = db.relationship('Sentence', backref='text', lazy=True)

class Sentence(db.Model):
    __tablename__ = 'sentences'

    id = db.Column(db.Integer, primary_key=True)    
    nr = db.Column(db.Integer)
    sentence = db.Column(db.Text)
    textid = db.Column(db.Integer, db.ForeignKey('texts.id'), nullable=False)

class SentenceSearch(db.Model):
    __tablename__ = 'sentencesearch'
    
    id = db.Column(db.Integer, primary_key=True)
    nr = db.Column(db.Integer)
    sentence = db.Column(db.Text)
    textid = db.Column(db.Integer, db.ForeignKey('texts.id'), nullable=False)

class Tree(db.Model):
    __tablename__ = 'trees'
    
    id = db.Column(db.Integer, primary_key=True)
    sentenceid = db.Column(db.Integer, db.ForeignKey('sentences.id'), primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('users.id'),primary_key=True)
    status = db.Column(db.Text)
    comment = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)

class Feature(db.Model):
    __tablename__ = 'features'

    treeid = db.Column(db.Integer, db.ForeignKey('trees.id'), primary_key=True)
    nr = db.Column(db.Integer, primary_key=True)
    attr = db.Column(db.Text, primary_key=True)
    value = db.Column(db.Text)

class SentenceFeature(db.Model):
    __tablename__ = 'sentencefeatures'

    sentenceid= db.Column(db.Integer, db.ForeignKey('trees.id'), primary_key=True)
    attr = db.Column(db.Text)
    value = db.Column(db.Text)

class Link(db.Model):
    __tablename__ = 'links'

    treeid = db.Column(db.Integer, db.ForeignKey('trees.id'), primary_key=True)
    depid = db.Column(db.Integer)
    govid = db.Column(db.Integer)
    function = db.Column(db.Text)

class Todo(db.Model):
    __tablename__ = 'todos'

    userid = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True))
    textid = db.Column(db.Integer, db.ForeignKey('texts.id'), primary_key=True))
    type = db.Column(db.Text)
    status = db.Column(db.Text)
    comment = db.Column(db.Text)

class Exo(db.Model):
    __tablename__ = 'exo'

    textid = db.Column(db.Integer, db.ForeignKey('texts.id'), primary_key=True))##foregn key lol
    type = db.Column(db.Integer)
    exotoknum = db.Column(db.Integer)
    status = db.Column(db.Text)
    comment = db.Column(db.Text)

class ExoUserSentence(db.model):
    textid = db.Column(db.Integer, db.ForeignKey('texts.id'), primary_key=True))
    userid = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True))
    sentenceid = db.Column(db.Integer, db.ForeignKey('sentences.id'), primary_key=True))

