"""
read_rss_default_analysis.py

An RSS reader in Python that does sentiment analysis using the NLKT default sentiment analysis, and stores the results in Deephaven.

This file is meant to run through Deephaven's Application Mode as part of several Python scripts. Because of this, some
variables may not be defined in here, but instead in helper_functions.py or read_rss.py.
"""
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer

def build_default_sia_classifier_func(classifier):
    def a(strn):
        sentiment = classifier.polarity_scores(strn)
        return [sentiment["pos"], sentiment["neu"], sentiment["neg"], sentiment["compound"]]
    return a

classifier = build_default_sia_classifier_func(SentimentIntensityAnalyzer())

rss_feed_urls = ["https://www.reddit.com/r/wallstreetbets/new/.rss"]
built_in_sia_wsb = read_rss_continual(rss_feed_urls, rss_attributes_method=rss_attributes_method_reddit, rss_datetime_converter=datetime_converter_reddit)

rss_feed_urls = ["https://www.reddit.com/r/all/new/.rss"]
built_in_sia_all = read_rss_continual(rss_feed_urls, rss_attributes_method=rss_attributes_method_reddit, rss_datetime_converter=datetime_converter_reddit, sleep_time=1)

reddit_all_wsb = read_rss_continual(["https://www.reddit.com/r/all/new/.rss", "https://www.reddit.com/r/wallstreetbets/new/.rss"], rss_attributes_method=rss_attributes_method_reddit, rss_datetime_converter=datetime_converter_reddit, sleep_time=1)

rss_feed_urls = ["https://hnrss.org/newest"]
built_in_sia_hackernews = read_rss_continual(rss_feed_urls, rss_attributes_method=rss_attributes_method_hackernews, rss_datetime_converter=datetime_converter_hackernews, sleep_time=60)

rss_feed_urls = ["https://seekingalpha.com/feed.xml"]
built_in_sia_seeking_alpha = read_rss_continual(rss_feed_urls, rss_attributes_method=rss_attributes_seeking_alpha, rss_datetime_converter=datetime_converter_seeking_alpha, sleep_time=120)

built_in_sia_wsb = built_in_sia_wsb.update("Sentiment = (org.jpy.PyListWrapper)classifier(RssEntryTitle)")\
    .update("Positive = (double)Sentiment[0]")\
    .update("Neutral = (double)Sentiment[1]")\
    .update("Negative = (double)Sentiment[2]")\
    .update("Compound = (double)Sentiment[3]")
built_in_sia_all = built_in_sia_all.update("Sentiment = (org.jpy.PyListWrapper)classifier(RssEntryTitle)")\
    .update("Positive = (double)Sentiment[0]")\
    .update("Neutral = (double)Sentiment[1]")\
    .update("Negative = (double)Sentiment[2]")\
    .update("Compound = (double)Sentiment[3]")
built_in_sia_hackernews = built_in_sia_hackernews.update("Sentiment = (org.jpy.PyListWrapper)classifier(RssEntryTitle)")\
    .update("Positive = (double)Sentiment[0]")\
    .update("Neutral = (double)Sentiment[1]")\
    .update("Negative = (double)Sentiment[2]")\
    .update("Compound = (double)Sentiment[3]")
built_in_sia_seeking_alpha = built_in_sia_seeking_alpha.update("Sentiment = (org.jpy.PyListWrapper)classifier(RssEntryTitle)")\
    .update("Positive = (double)Sentiment[0]")\
    .update("Neutral = (double)Sentiment[1]")\
    .update("Negative = (double)Sentiment[2]")\
    .update("Compound = (double)Sentiment[3]")
