# Simple statistics of each sentiment
from deephaven import Aggregation as agg, as_list

built_in_sia_hackernews_averages = built_in_sia_hackernews.aggBy(as_list([agg.AggAvg("Positive", "Negative", "Neutral", "Compound")]))
built_in_sia_hackernews_medians = built_in_sia_hackernews.aggBy(as_list([agg.AggMed("Positive", "Negative", "Neutral", "Compound")]))
built_in_sia_hackernews_deviations = built_in_sia_hackernews.aggBy(as_list([agg.AggStd("Positive", "Negative", "Neutral", "Compound")]))

# Positive percent of built in analysis
built_in_sia_hackernews_positive_percent = built_in_sia_hackernews.update("PositiveCount = Positive > Negative ? 1 : 0")\
    .aggBy(as_list([agg.AggSum("PositiveCount"), agg.AggCount("TotalCount")]))\
    .update("PositivePercent = PositiveCount / TotalCount")

# Positive percent of custom analysis
custom_sia_hackernews_positive_percent = custom_sia_hackernews.update("PositiveCount = Sentiment.equals(`positive`)")\
    .aggBy(as_list([agg.AggSum("PositiveCount"), agg.AggCount("TotalCount")]))\
    .update("PositivePercent = PositiveCount / TotalCount")

# Join 2 tables on the unique datetime and sentence combination
hackernews_joined = built_in_sia_hackernews.join(custom_sia_hackernews, "PublishDatetime, RssEntryTitle", "TextSentiment = Sentiment")
