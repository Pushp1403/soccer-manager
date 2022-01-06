from config.app_config import db
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    _password = db.Column("password", db.String, nullable=False)
    team = db.relationship('Team', backref='User', lazy=True, uselist=False)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        """Store the password as a hash for security."""
        self._password = generate_password_hash(value)

    def check_password(self, value):
        return check_password_hash(self.password, value)


class UserLogin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    token = db.Column(db.String, unique=True, nullable=False)


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String, nullable=False)
    country = db.Column(db.String, nullable=False)
    available_cash = db.Column(db.Integer, nullable=False, default=5000000)
    team_owner = db.Column(db.ForeignKey(User.id), nullable=False)
    players = db.relationship('Player', backref=db.backref('Team', lazy=True))


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, unique=False, nullable=False)
    last_name = db.Column(db.String, unique=False, nullable=False)
    age = db.Column(db.Integer, nullable=False, default=12)
    country = db.Column(db.String, nullable=False)
    market_value = db.Column(db.Integer, nullable=False, default=1000000)
    player_type = db.Column(db.String, nullable=False)
    team_id = db.Column(db.ForeignKey(Team.id), nullable=False)


class Transfer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ask_price = db.Column(db.Integer, nullable=False)
    transferred = db.Column(db.Boolean, nullable=False, default=False)
    player_id = db.Column(db.ForeignKey(Player.id), nullable=False)
    transferred_from = db.Column(db.ForeignKey(Team.id), nullable=False)
    transferred_to = db.Column(db.ForeignKey(Team.id))
