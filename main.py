# main.py
from fetch_data import main as fetch_ai_news  # Import backend function

def main():
    """
    Main entry point for backend data fetching.
    Returns a cleaned DataFrame with news and categories.
    """
    df = fetch_ai_news()
    return df

# Optional test
if __name__ == "__main__":
    data = main()
    print(f"Fetched {len(data)} articles")
    print(data.head())
