from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(400), unique=False)
    twitterid = db.Column(db.String(400), index=True, unique=True)
    token = db.Column(db.String(400))
    token_secret = db.Column(db.String(400))
    redtoken = db.Column(db.String(400))
    redrefresh = db.Column(db.String(400))
    clicks = db.relationship('Clicks', backref='twuser', lazy='dynamic')
    stats = db.relationship('Stats', backref='twuser', lazy='dynamic')
    subscriptions = db.relationship('Subscriptions', backref='twuser',
                                    lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.name

    @staticmethod
    def add_user(uinfo):
        db.session.add(User(**uinfo))
        db.session.commit()

        return User.query.filter_by(twitterid=uinfo['twitterid']).first()

    @staticmethod
    def add_reddit_info(uobj, rinfo):
        uobj.redtoken = rinfo['access_token']
        uobj.redrefresh = rinfo['refresh_token']

        db.session.commit()

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
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))

    @staticmethod
    def add_click(subname, uobject):
        db.session.add(Clicks(subname=subname, twuser=uobject))
        db.session.commit()


class Stats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    term = db.Column(db.String(400))
    num_results = db.Column(db.Integer)
    num_matches = db.Column(db.Integer)

    @staticmethod
    def add_data(res_data, uobject):
        db.session.add(Stats(term=res_data['term'],
                             num_results=res_data['num_results'],
                             num_matches=res_data['num_matches'],
                             twuser=uobject))
        db.session.commit()


class Subscriptions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    subreddit = db.Column(db.String(400))

    @staticmethod
    def rec_sub(sub, uobject):
        db.session.add(Subscriptions(subreddit=sub, twuser=uobject))
        db.session.commit()
