from . import db

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)

    def __repr__(self):
        return '<User %r>' % self.username

class UploadFile(db.Model):
    __tablename__ = 'uploadfile'
    tfsname = db.Column(db.String(64), unique=True, index=True, primary_key=True)
    md5 = db.Column(db.String(64), unique=True, index=True)
    filename = db.Column(db.String(64), index=True)
    mtime = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<UploadFile %r>' % self.tfsname
