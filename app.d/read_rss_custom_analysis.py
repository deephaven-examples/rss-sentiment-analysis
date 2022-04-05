"""
read_rss_custom_analysis.py

An RSS analyzer that uses a custom Naive Bayes Classifier.

This file is meant to run through Deephaven's Application Mode as part of several Python scripts. Because of this, some
variables may not be defined in here, but instead in helper_functions.py or read_rss.py.
"""
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews

def _word_feats(words):
    """
    NLTK word feature generator for the NaiveBayesClassifier
    """
    return dict([(word, True) for word in words])

def _word_feats_string(strn):
    """
    NLTK word feature generator for the NaiveBayesClassifier that
    takes a string
    """
    return dict([(word, True) for word in strn.split(" ")])

def build_model():
    """
    Builds the NaiveBayesClassifier model
    """
    nltk.download('movie_reviews')

    negids = movie_reviews.fileids('neg')
    posids = movie_reviews.fileids('pos')

    negfeats = [(_word_feats(movie_reviews.words(fileids=[f])), "negative") for f in negids]
    posfeats = [(_word_feats(movie_reviews.words(fileids=[f])), "positive") for f in posids]

    trainfeats = negfeats + posfeats

    return NaiveBayesClassifier.train(trainfeats)

def build_model_func(classifier):
    """
    Generates a method that classifies a string using the given classifier
    """
    def a(strn):
        return classifier.classify(_word_feats_string(strn))
    return a

classifier = build_model_func(build_model())

rss_feed_urls = ["https://www.reddit.com/r/wallstreetbets/new/.rss"]
custom_sia_wsb = read_rss_continual(rss_feed_urls, rss_attributes_method=rss_attributes_method_reddit, rss_datetime_converter=datetime_converter_reddit)

rss_feed_urls = ["https://www.reddit.com/r/all/new/.rss"]
custom_sia_all = read_rss_continual(rss_feed_urls, rss_attributes_method=rss_attributes_method_reddit, rss_datetime_converter=datetime_converter_reddit, sleep_time=1)

rss_feed_urls = ["https://hnrss.org/newest"]
custom_sia_hackernews = read_rss_continual(rss_feed_urls, rss_attributes_method=rss_attributes_method_hackernews, rss_datetime_converter=datetime_converter_hackernews, sleep_time=60)

rss_feed_urls = ["https://seekingalpha.com/feed.xml"]
custom_sia_seeking_alpha = read_rss_continual(rss_feed_urls, rss_attributes_method=rss_attributes_seeking_alpha, rss_datetime_converter=datetime_converter_seeking_alpha, sleep_time=120)

custom_sia_wsb = custom_sia_wsb.update(["Sentiment = classifier(RssEntryTitle)"])
custom_sia_all = custom_sia_all.update(["Sentiment = classifier(RssEntryTitle)"])
custom_sia_hackernews = custom_sia_hackernews.update(["Sentiment = classifier(RssEntryTitle)"])
custom_sia_seeking_alpha = custom_sia_seeking_alpha.update(["Sentiment = classifier(RssEntryTitle)"])
