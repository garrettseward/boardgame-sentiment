#!/usr/bin/env python
import os
import statistics as stats
from datetime import datetime

import numpy as np
import pandas as pd
from collections import Counter
from nltk.corpus import stopwords

from sentiment_analysis.database import db_session
from sentiment_analysis.model import GameReview, SigWord, Rating

dir_path = os.path.dirname(os.path.realpath(__file__))

df = pd.read_csv('%s/../../sample.csv' % dir_path)

average_ratings = dict(word=[], count=[], ratings=[], median=[], mode=[], mean=[], std=[])

remove_words = ['game', 'game.', 'game,', 'I', 'it', '_', "I'd", 'The', '-', 'This', 'It', 'A', "It's", "I'm" , 'play']
sw = set(stopwords.words('english') + remove_words)

words = Counter([w for w in " ".join(df.comment).split() if w not in sw])

print('Processing %d words' % len(words))
start = datetime.now()
for word, count in words.items():
    ratings = [g.rating for g in GameReview.query.filter(GameReview.comment.like('%' + word + '%'))]
    if len(ratings) == 0:
        print('No reviews found for %s' % word)
        continue
    sig_word = SigWord(
        word=word,
        count=count,
        mean=round(stats.mean(ratings), 3),
    )
    try: sig_word.mode = stats.mode(ratings)
    except: pass
    try: sig_word.median = stats.median(ratings)
    except: pass
    try: sig_word.median_grouped = stats.median_grouped(ratings)
    except: pass
    try: sig_word.median_high = stats.median_high(ratings)
    except: pass
    try: sig_word.median_low = stats.median_low(ratings)
    except: pass
    try: sig_word.variance = stats.variance(ratings)
    except: pass
    try: sig_word.pvariance = stats.pvariance(ratings)
    except: pass
    sig_word.save(False)
SigWord.db_session.commit()
print('Processing took %s' % (datetime.now() - start))
