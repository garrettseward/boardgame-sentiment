#!/usr/bin/env python
import os
import re
import statistics as stats
import string
from datetime import datetime

import nltk as nl
import numpy as np
import pandas as pd
import sqlalchemy as sa
from collections import Counter
from nltk.corpus import stopwords

from sentiment_analysis.database import db_session
from sentiment_analysis.entities import GameReview, SigWord, SigWordUse


dir_path = os.path.dirname(os.path.realpath(__file__))

df = pd.read_csv('%s/../../data/raw/sample.csv' % dir_path)

sw = set(stopwords.words('english'))

def derive_tokens(raw):
    return [w for w in nl.word_tokenize(raw) if w.isalpha() and len(w) > 1]

words = set(derive_tokens(df.comment.str.cat(sep=' ').lower()))

print('Processing %d words' % len(words))
start = datetime.now()
for word in words:
    ratings = []
    game_reviews = GameReview.query.filter(sa.func.lower(GameReview.comment).like('%' + word + '%'))
    games = []
    sig_word = SigWord(word=word)
    for game_review in game_reviews:
        review_tokens = derive_tokens(game_review.comment.lower())
        count = review_tokens.count(word)
        if count == 0:
            continue
        games.append(game_review)
        swu = SigWordUse(
            sig_word=sig_word,
            game_review=game_review,
            count=count,
        )
        swu.save(False)
        ratings += ([game_review.rating] * swu.count)
    sig_word.count = len(ratings)
    sig_word.game_count = len(games)
    try: sig_word.mean = round(stats.mean(ratings), 3)
    except: pass
    sig_word.median_q25 = np.percentile(ratings, 25)
    sig_word.median_q50 = np.percentile(ratings, 50)
    sig_word.median_q75 = np.percentile(ratings, 75)
    try: sig_word.mode = stats.mode(ratings)
    except: pass
    try: sig_word.median = stats.median(ratings)
    except: pass
    try: sig_word.variance = stats.variance(ratings)
    except: pass
    try: sig_word.pvariance = stats.pvariance(ratings)
    except: pass
    try: sig_word.stdev = stats.stdev(ratings)
    except: pass
    try: sig_word.pstdev = stats.pstdev(ratings)
    except: pass
    sig_word.save(False)
SigWord.db_session.commit()
print('Processing took %s' % (datetime.now() - start))
