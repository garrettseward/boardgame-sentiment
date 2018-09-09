#!/usr/bin/env python
import os
import pandas as pd
from sklearn.model_selection import train_test_split

from sentiment_analysis.database import engine, db_session
from sentiment_analysis.entities import Entity, GameReview


Entity.metadata.create_all(bind=engine)

dir_path = os.path.dirname(os.path.realpath(__file__))
df = pd.read_csv('%s/../../data/raw/sample.csv' % dir_path)
train, test = train_test_split(df, test_size=0.33, random_state=42)
for _, row in train.iterrows():
    GameReview(
        user_id=row.userID,
        game_id=row.gameID,
        rating=row.rating,
        comment=row.comment,
        comment_lower=row.comment.lower(),
        train=True,
    ).save(False)
for _, row in test.iterrows():
    GameReview(
        user_id=row.userID,
        game_id=row.gameID,
        rating=row.rating,
        comment=row.comment,
        comment_lower=row.comment.lower(),
        train=False,
    ).save(False)
db_session.commit()