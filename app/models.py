

from app import db

ACCESS = {
    'guest': 0,
    'user': 1,
    'admin': 2,
    'super_admin': 3,
}

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    family_name = db.Column(db.String(60), index=True)
    picture_url = db.Column(db.String(128), index=True)
    role= db.Column(db.String(10), default=ACCESS['guest'])
    # is_admin = db.Column(db.Boolean, default=False)

    def is_admin(self):
        return self.access == ACCESS['admin']

    def is_super(self): ##Might not be necessary eventually
        return self.access == ACCESS['super_admin']
    
    def allowed(self, access_level):
        return self.access >= access_level

    def __repr__(self):
        return '<user: {}>'.format(self.username)