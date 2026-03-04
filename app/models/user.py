from app.extensions import db
from app.utils.security import hash_password, check_password

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default="user")

    def set_password(self, raw_password):
        self.password = hash_password(raw_password)

    def verify_password(self, raw_password):
        return check_password(raw_password, self.password)