"""
helper_functions.py

A file that defines some shared helper functions and imports for the RSS readers.
"""
from deephaven.time import to_datetime

from dateutil import parser

from datetime import datetime

def datetime_converter_reddit(entry):
    dt = datetime.fromisoformat(entry["updated"])
    dts = dt.strftime("%Y-%m-%dT%H:%M:%S") + " UTC"
    return to_datetime(dts)

def datetime_converter_hackernews(entry):
    dt = parser.parse(entry["published"])
    dts = dt.strftime("%Y-%m-%dT%H:%M:%S") + " UTC"
    return to_datetime(dts)

def datetime_converter_seeking_alpha(entry):
    dt = parser.parse(entry["published"])
    dts = dt.strftime("%Y-%m-%dT%H:%M:%S") + " NY"
    return to_datetime(dts)

def rss_attributes_method_reddit(entry):
    return (entry["title"], datetime_converter_reddit(entry), entry["title_detail"]["base"])

def rss_attributes_method_hackernews(entry):
    return (entry["title"], datetime_converter_hackernews(entry), entry["title_detail"]["base"])

def rss_attributes_seeking_alpha(entry):
    return (entry["title"], datetime_converter_seeking_alpha(entry), entry["title_detail"]["base"])
