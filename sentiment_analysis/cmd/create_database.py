#!/usr/bin/env python
import os
import pandas as pd

from sentiment_analysis.database import engine, db_session
from sentiment_analysis.entities import Entity, GameReview


Entity.metadata.create_all(bind=engine)

dir_path = os.path.dirname(os.path.realpath(__file__))
df = pd.read_csv('%s/../../data/raw/sample.csv' % dir_path)

for _, row in df.iterrows():
    GameReview(
        user_id=row.userID,
        game_id=row.gameID,
        rating=row.rating,
        comment=row.comment,
        comment_lower=row.comment.lower(),
    ).save(False)
db_session.commit()