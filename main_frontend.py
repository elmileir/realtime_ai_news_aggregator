import streamlit as st
import pandas as pd
from datetime import datetime
from fetch_data import main  # Import the backend function

@st.cache_data(ttl=60)  # Cache data for 60 seconds
def get_data():
    with st.spinner('Fetching articles...'):
        return main()
    

def run_dashboard():
    st.title("News Aggregator Dashboard")
    
    # Button to manually refresh data
    if st.button("Refresh Data"):

        #st.cache_data.clear()
        #st.experimental_rerun()
        
        st.cache_data.clear()
        df = main()
    
    # Load data
    df = get_data()
    
    if df.empty:
        st.error("No news data available. Try refreshing later.")
        return
    
    min_date = df['date'].min()
    max_date = df['date'].max()

    selected_dates = st.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    if len(selected_dates) == 1:
        start_date = end_date = selected_dates[0]
    else:
        start_date, end_date = selected_dates


    all_categories = sorted(df['Category'].unique().tolist())
    category_options = ["All"] + all_categories

    selected_categories = st.multiselect(
        "Select Categories",
        options=category_options,
        default=["All"]
    )

    num_articles = st.slider("Number of Articles to Display", min_value=1, max_value=50, value=10)

    # Filter by date
    df_filtered = df[(df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date))]

    # Filter by category
    if "All" not in selected_categories:
        df_filtered = df_filtered[df_filtered['Category'].isin(selected_categories)]

    # Limit number of articles
    df_filtered = df_filtered.head(num_articles)


    for idx, row in df_filtered.iterrows():
        st.markdown(f"### [{row['Title']}]({row['Link']})")
        st.write(f"**Source**: {row['Source']}")
        st.write(f"**Category**: {row['Category']}")
        st.write(f"**Date**: {row['date'].strftime('%Y-%m-%d')}")
        st.write(f"**Description**: {row['Description']}")
        st.markdown("---")

if __name__ == "__main__":
    run_dashboard()


