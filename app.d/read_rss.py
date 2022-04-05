"""
read_rss.py

Defines the method for reading from an RSS feed and performing sentiment analysis on the data.
"""
import feedparser
from deephaven import DynamicTableWriter
import deephaven.dtypes as dht
from deephaven import merge
from deephaven.time import to_datetime, now
from dateutil import parser

import time
import math
import threading

def _default_rss_attributes_method(entry):
    return (entry["title"], _default_rss_datetime_converter(entry), entry["title_detail"]["base"])

def _default_rss_datetime_converter(entry):
    try:
        dt = parser.parse(entry["published"])
        dts = dt.strftime("%Y-%m-%dT%H:%M:%S") + " UTC"
        return to_datetime(dts)
    except:
        return now()

def read_single_rss_entry(rss_feed_url):
    """
    This method returns a single entry from the given RSS feed. This is mostly used
    for debugging and simple testing.

    Parameters:
        rss_feed_url (str): The RSS feed URL as a string.

    Returns:
        dict: A single entry from the RSS feed.
    """
    return feedparser.parse(rss_feed_url).entries[0]

def read_rss_continual(rss_feed_urls, rss_attributes_method=None, rss_datetime_converter=None,
        sleep_time=5, column_names=None, column_types=None, thread_count=None):
    """
    This method continually reads from an RSS feed and stores its data in a Deephaven table.

    Data is only written to the Deephaven table if it's new data. This is determined by the timestamp of the entries.

    This method works best with RSS feeds that are always ordered by date-time, and update frequently. Some
    examples of this are Reddit and Hackernews RSS feeds.

    This method is highly customizeable. rss_attributes_method, column_names, and column_types define the resulting
    Deephaven table, and rss_datetime_converter allows you to define how the datetime of the entry is computed. sleep_time
    can be customized for performance (a larger value is useful for feeds that don't update often, while a smaller value
    is better for feeds that update quickly).

    thread_count can be used to run the RSS reader across multiple threads.

    Parameters:
        rss_feed_urls (list<str>): A list of RSS feed URLs to view.
        rss_attributes_method (method): A method that converts an RSS entry to a tuple of values to write.
        rss_datetime_converter (method): A method that takes an RSS feed entry and converts it to a Deephaven datetime object.
            This should be customized based on the RSS feed.
        sleep_time (int): An integer representing the number of seconds to wait between
            RSS pulls if data hasn't changed.
        column_names (list<str>): A list of column names for the resulting table.
        column_types (list<dht.type>): A list of column types for the resulting table.
        thread_count (int): How many threads to run the RSS reader in. If not set, 1 thread will be used.

    Returns:
        Table: The Deephaven table that will contain the results from the RSS feed.
    """
    def thread_function(rss_feed_urls, rss_attributes_method, rss_datetime_converter, sleep_time, table_writer):
        last_updated_list = [None for i in range(len(rss_feed_urls))]

        while True:
            rss_feed_url_index = 0
            updated = False
            while rss_feed_url_index < len(rss_feed_urls):
                rss_feed_url = rss_feed_urls[rss_feed_url_index]
                last_updated = last_updated_list[rss_feed_url_index]
                feed = feedparser.parse(rss_feed_url)

                i = 0
                while i < len(feed.entries):
                    try:
                        entry = feed.entries[i]
                        datetime_attribute = rss_datetime_converter(entry)

                        #If no datetime, break
                        if datetime_attribute is None:
                            break

                        #If data has previously been read, and the current item has a timestamp less than or equal
                        #to the last item written to the table in the previous pull, then stop writing data.
                        #RSS feeds can unpublish data, so a strict equality comparison can't work.
                        #This may result in lost data if the RSS feed can publish multiple items with the same timestamp.
                        if not (last_updated is None) and datetime_attribute <= last_updated:
                            break

                        write_row = rss_attributes_method(entry)
                        table_writer.write_row(write_row)
                    except Exception as e:
                        #Swallow exceptions for now if things go wrong, the RSS feeds aren't 100% the same format
                        print(f"Error on reading RSS feed {rss_feed_url}")
                        print(e)

                    i += 1

                if not i == 0: #If feed has been updated, set last updated time to the newest item in the feed
                    updated = True
                    last_updated_list[rss_feed_url_index] = rss_datetime_converter(feed.entries[0])

                rss_feed_url_index += 1
            #Sleep after going through the entire list if no feeds were updated
            if not updated:
                time.sleep(sleep_time)

    if column_names is None:
        column_names = [
            "RssEntryTitle",
            "PublishDatetime",
            "RssFeedUrl"
        ]
    if column_types is None:
        column_types = [
            dht.string,
            dht.DateTime,
            dht.string
        ]

    dynamic_table_writer_columns = dict(zip(column_names, column_types))

    if rss_attributes_method is None:
        rss_attributes_method = _default_rss_attributes_method
    if rss_datetime_converter is None:
        rss_datetime_converter = _default_rss_datetime_converter

    if thread_count is None:
        table_writer = DynamicTableWriter(dynamic_table_writer_columns)
        thread = threading.Thread(target=thread_function, args=[rss_feed_urls, rss_attributes_method, rss_datetime_converter, sleep_time, table_writer])
        thread.start()
        return table_writer.table
    else:
        tables = []
        thread_index = 0
        urls_per_thread = math.ceil(len(rss_feed_urls)/thread_count)
        while thread_index < thread_count:
            table_writer = DynamicTableWriter(dynamic_table_writer_columns)
            start_index = thread_index * urls_per_thread
            #Python doesn't check index bounds on list splices [:], so this works without needing any index checks
            thread = threading.Thread(target=thread_function, args=[rss_feed_urls[start_index:start_index + urls_per_thread], rss_attributes_method, rss_datetime_converter, sleep_time, table_writer])
            thread.start()
            thread_index += 1
            tables.append(table_writer.table)
        return merge(tables) 
