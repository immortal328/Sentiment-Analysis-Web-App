import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from file import fetch_data
model = SentimentIntensityAnalyzer()

# Helper functions


# VADER Prediction
def sentiment_score(text):
    scores = model.polarity_scores(text)
    if scores['compound'] == 0:
        sentiment = 'Neutral'
    elif scores['compound'] > 0:
        sentiment = 'Positive'
    else:
        sentiment = 'Negative'
    score = scores['compound']
    return sentiment, score

# Visualisation function


def lexicon_retings():
    def return_ratings(word):
        if word in model.lexicon.keys():
            return model.lexicon[word]
        else:
            return 0.01
    text = fetch_data()
    words = text.split()
    ratings = list(map(return_ratings, words))
    series = [{'name': x, 'data': [y]} for x, y in zip(words, ratings)]
    return series


def result_analysis():
    text = fetch_data()
    words = text.split()
    results = list(map(model.polarity_scores, words))
    results = [word['compound'] for word in results]
    return words, results
