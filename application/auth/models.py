from application import db
from application.models import Base

class User(Base):

    __tablename__ = "account"

    username = db.Column(db.String(144), nullable=False)
    fullname = db.Column(db.String(144), nullable=False)
    password = db.Column(db.String(144), nullable=False)

    permissions = db.relationship("Permission", backref="account", lazy=True)
    
    def __init__(self, username, fullname, password):
        self.username = username
        self.fullname = fullname
        self.password = password
  
    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def get_projects(self):
        return db.engine.execute("SELECT * FROM project as P WHERE EXISTS (SELECT * FROM permission WHERE user_id=? AND project_id=P.id)", [self.get_id()])
