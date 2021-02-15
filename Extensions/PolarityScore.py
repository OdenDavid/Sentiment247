import nltk
#nltk.download('vader_lexicon')

from nltk.sentiment.vader import SentimentIntensityAnalyzer


sid = SentimentIntensityAnalyzer()

def sentiment(message_text):
    scores = sid.polarity_scores(message_text)
    return scores