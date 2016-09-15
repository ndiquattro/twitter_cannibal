from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=False)
    twitterid = db.Column(db.Integer, index=True, unique=True)
    token = db.Column(db.String(120), unique=True)
    token_secret = db.Column(db.String(120), unique=True)
    clicks = db.relationship('Clicks', backref='twuser', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.name

    @staticmethod
    def add_user(uinfo):
        db.session.add(User(**uinfo))
        db.session.commit()

        return User.query.filter_by(twitterid=uinfo.id).first()

    @staticmethod
    def lookup_user(uid):
        return User.query.filter_by(twitterid=uid).first()

    @staticmethod
    def users_list():
        # Query DB
        ausers = User.query.with_entities(User.twitterid)

        # Return list
        return [uid[0] for uid in ausers]


class Clicks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subname = db.Column(db.String(400))
    userid = db.Column(db.Integer, db.ForeignKey('user.twitterid'))

    @staticmethod
    def add_click(subname, uobject):
        db.session.add(Clicks(subname=subname, twuser=uobject))
        db.session.commit()
