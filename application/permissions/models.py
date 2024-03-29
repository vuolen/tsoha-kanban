from sqlalchemy import UniqueConstraint

from application import db
from application.models import Base

class Permission(Base):
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"),
                           nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("account.id"),
                        nullable=False)
    admin = db.Column(db.Boolean, nullable=False)

    __table_args__ = (UniqueConstraint("project_id", "user_id", name="project_user_uc"),)


    def __init__(self, project_id, user_id, admin):
        self.project_id = project_id
        self.user_id = user_id
        self.admin = admin
