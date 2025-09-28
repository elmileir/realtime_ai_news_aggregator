import feedparser
import pandas as pd
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import concurrent.futures
import re
from transformers import pipeline

classifier = pipeline("zero-shot-classification",
                      model="facebook/bart-large-mnli")

CATEGORIES = ["Finance and Markets", "Law, Policy and Regulation", "Technology and Science",
              "Economy and Trade", "Business and Strategy", "Climate", "Arts"]


def fetch_single_feed(link_source_tuple):
    link, source = link_source_tuple
    entries = {"Title": [], "Link": [], "Published": [], "Description": [], "Source": []}
    try:
        feed = feedparser.parse(link)
        for entry in feed.entries:
            entries["Title"].append(entry.get("title", "No Title"))
            entries["Link"].append(entry.get("link", "No Link"))
            entries["Published"].append(entry.get("published", "No Date"))
            entries["Description"].append(entry.get("description", "No Description"))
            entries["Source"].append(source)

    except Exception as e:
        print(f"Error fetching {link}: {e}")
    return entries

def fetch_feed(links):
    all_entries = {"Title": [], "Link": [], "Published": [], "Description": [], "Source": []}
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_link = {executor.submit(fetch_single_feed, (link, source)): (link, source) 
                          for link, source in links.items()}
        for future in concurrent.futures.as_completed(future_to_link):
            result = future.result()
            for key in all_entries:
                all_entries[key].extend(result[key])
    return pd.DataFrame(all_entries)

def clean_html(text):
    try:
        soup = BeautifulSoup(text, "html.parser")
        return soup.get_text()
    except:
        return text


def extract_date(date_str):
    try:
        pattern1 = r'(?:\w+,\s+)?(\d{1,2}\s+\w{3}\s+\d{4})'
        match = re.search(pattern1, date_str)
        if match:
            return pd.to_datetime(match.group(1), format='%d %b %Y')
        return pd.to_datetime(date_str, errors='coerce')
    except:
        return pd.NaT

def categorise_article(text):
    try:
        result = classifier(text, candidate_labels=CATEGORIES)
        return result['labels'][0]
    except:
        return "Other"
    

def extract_and_clean_data(df):
    if df.empty:
        return df
    df['date'] = df['Published'].apply(extract_date)
    df = df.dropna(subset=['date'])
    df.drop(columns=['Published'], inplace=True)
    df['Description'] = df['Description'].apply(lambda x: clean_html(x)[:500])
    # AI categorisation
    df['Category'] = df['Description'].apply(categorise_article)
    return df


def main():
    links = {
        "https://feeds.content.dowjones.io/public/rss/mw_topstories":"MARKET WATCH REALTIME",
        "https://feeds.content.dowjones.io/public/rss/mw_topstories":"MARKET WATCH TOP STORIES",
        "https://www.ft.com/rss/home":"FINANCIAL TIMES",
        "https://feeds.bloomberg.com/markets/news.rss": "BLOOMBERG",
        "https://feeds.bloomberg.com/markets/news.rss":"SCIENCE DAILY",
        "https://news.mit.edu/rss/feed":"MIT NEWS",
        "https://techxplore.com/rss-feed/":"TECHXPLOER",
        "https://news.mit.edu/rss/topic/economics":"MIT ECONOMICS",
        "http://feeds.bbci.co.uk/news/world/rss.xml ": "BBC",
        "https://www.forbes.com/static_html/rss/rsshelp_header.html":"FORBES",
        "https://fortune.com/feed/":"FORTUNE",
        "https://www.theguardian.com/world/rss":"THE GUARDIAN",
        "https://ir.thomsonreuters.com/rss/news-releases.xml?items=15":"REUTERS FINANCIAL NEWS",
        "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml":"NYT",
        "https://rss.nytimes.com/services/xml/rss/nyt/Arts.xml":"NYT ARTS"
    }
    df = fetch_feed(links)
    df_clean = extract_and_clean_data(df)
    return df_clean






