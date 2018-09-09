import pandas as pd
import sqlalchemy as sa


from sentiment_analysis.database import Entity, engine


class GameReview(Entity):
    """
    A board game review.
    """
    __tablename__ = 'game_review'
    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer)
    game_id = sa.Column(sa.Integer)
    rating = sa.Column(sa.Float(3))
    comment = sa.Column(sa.Text)
    comment_lower = sa.Column(sa.Text)

    def __repr__(self):
        return '<GameReview %d %d %.2f "%s">' % (self.user_id, self.game_id,
            self.rating, self.comment[:15])

class SigWord(Entity):
    """
    Significant Word Table.
    """
    __tablename__ = 'sig_word'
    id = sa.Column(sa.Integer, primary_key=True)
    word = sa.Column(sa.String(255), unique=True)
    count = sa.Column(sa.Integer)
    game_count = sa.Column(sa.Integer)
    median = sa.Column(sa.Float(3))
    median_q25 = sa.Column(sa.Float(4))
    median_q50 = sa.Column(sa.Float(4))
    median_q75 = sa.Column(sa.Float(4))
    mode = sa.Column(sa.Float(3))
    mean = sa.Column(sa.Float(4))
    stdev = sa.Column(sa.Float(5))
    pstdev = sa.Column(sa.Float(5))
    variance = sa.Column(sa.Float(5))
    pvariance = sa.Column(sa.Float(5))

    @classmethod
    def get_by_word(cls, word):
        return cls.query.filter(cls.word==word).first()

    @property
    def ratings(self):
        ratings = []
        for usage in self.usages:
            ratings += ([usage.game_review.rating] * usage.count)
        return ratings

    def __repr__(self):
        return '<SigWord %s [%.3f, %.3f, %.3f] %d>' % (
            self.word, self.median_q25, self.median_q50, self.median_q75, self.count)


class SigWordUse(Entity):
    """
    Usage of a significant word in a review.
    """
    __tablename__ = 'sig_word_use'
    id = sa.Column(sa.Integer, primary_key=True)
    sig_word_id = sa.Column(sa.Integer, sa.ForeignKey('sig_word.id'))
    sig_word = sa.orm.relationship('SigWord', backref='usages')
    game_review_id = sa.Column(sa.Integer, sa.ForeignKey('game_review.id'))
    game_review = sa.orm.relationship('GameReview', backref='sig_word_usages')
    count = sa.Column(sa.Integer)

    @classmethod
    def onehot(cls):
        df = pd.read_sql("""
            SELECT gr.rating as _rating, gr.game_id as game_id, gr.user_id as user_id, sw.word as word
            FROM sig_word_use AS swu
            LEFT JOIN game_review AS gr ON gr.id=swu.game_review_id
            LEFT JOIN sig_word AS sw on sw.id=swu.sig_word_id
            ORDER BY word ASC
        """, engine)
        dummies = pd.get_dummies(df.word, prefix=None)
        id_cols = df[['game_id', 'user_id', '_rating']]
        oh = pd.concat([id_cols, dummies], axis=1)
        return oh.groupby(['game_id', 'user_id', '_rating']).sum().reset_index()

    def __repr__(self):
        return '<SigWordUse %s %.2f %d>' % (
            self.sig_word.word, self.game_review.rating, self.count)
