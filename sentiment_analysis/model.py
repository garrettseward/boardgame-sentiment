import sqlalchemy as sa


from sentiment_analysis.database import Model


class GameReview(Model):
    """
    A board game review.
    """
    __tablename__ = 'game_review'
    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer)
    game_id = sa.Column(sa.Integer)
    rating = sa.Column(sa.Numeric(3))
    comment = sa.Column(sa.Text)

class SigWord(Model):
    """
    Significant Word Table.
    """
    __tablename__ = 'sig_word'
    id = sa.Column(sa.Integer, primary_key=True)
    word = sa.Column(sa.String(255), unique=True)
    count = sa.Column(sa.Integer)
    median = sa.Column(sa.types.Numeric(3))
    median_grouped = sa.Column(sa.types.Numeric(3))
    median_high = sa.Column(sa.types.Numeric(3))
    median_low = sa.Column(sa.types.Numeric(3))
    mode = sa.Column(sa.types.Numeric(3))
    mean = sa.Column(sa.types.Numeric(3))
    stdev = sa.Column(sa.types.Numeric(3))
    pstdev = sa.Column(sa.types.Numeric(5))
    variance = sa.Column(sa.types.Numeric(5))
    pvariance = sa.Column(sa.types.Numeric(5))


class Rating(Model):
    """
    Ratings Table
    """
    __tablename__ = 'rating'
    id = sa.Column(sa.Integer, primary_key=True)
    rating = sa.Column(sa.Numeric(3), unique=True)