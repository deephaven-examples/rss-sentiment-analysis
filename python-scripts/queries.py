# Simple statistics of each sentiment
from deephaven import Aggregation as agg, as_list

agg_list = as_list([
    agg.AggAvg("Avg_Positive = Positive", "Avg_Negative = Negative", "Avg_Neutral = Neutral", "Avg_Compound = Compound"),
    agg.AggMed("Med_Positive = Positive", "Med_Negative = Negative", "Med_Neutral = Neutral", "Med_Compound = Compound"),
    agg.AggStd("Std_Positive = Positive", "Std_Negative = Negative", "Std_Neutral = Neutral", "Std_Compound = Compound"),
])

built_in_sia_hackernews_analyzed_statistics = built_in_sia_hackernews.aggBy(agg_list)

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
