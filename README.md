=======
# realtime_news_aggregator



## 📊 Real-Time AI News Aggregator

A Streamlit-powered dashboard that fetches, cleans, and categorises live news articles from multiple sources using Hugging Face Transformers. The app enables users to filter by date range, categories, and article limits, providing an interactive and efficient way to track the latest trends in AI, business, science, finance, and more.

## 🚀 Features

🔄 Real-time data fetching from multiple RSS feeds.

⚡ Multithreading for faster retrieval of news articles in parallel.

🧠 AI-powered classification using Hugging Face zero-shot-classification.

📊 Interactive dashboard built with Streamlit (filter by date, category, number of articles).

🧹 Data cleaning & preprocessing with BeautifulSoup and Pandas.


## 🛠️ Tech Stack

Languages: Python (3.8+)

Libraries: Streamlit, Transformers, Pandas, BeautifulSoup, Feedparser

Concepts: Multithreading, Caching, Zero-Shot Classification

Tools: Git, VS Code

## ▶️ Run Locally

### 1️⃣ Clone the repository

git clone https://github.com/elmileir/realtime_ai_news_aggregator.git
cd realtime-news-aggregator


### 2️⃣ Create & activate a virtual environment

‣python -m venv your_venv_name

‣source your_venv_name/bin/activate   # Mac/Linux

‣.\your_venv_name\Scripts\activate      # Windows


### 3️⃣ Install dependencies

pip install -r requirements.txt


### 4️⃣ Run the Streamlit app

streamlit run main_frontend.py


### 🌍 Next Steps

Deploy to Streamlit Cloud for public access.

Extend classifier with custom AI models.

Add more news feeds and user authentication.


### 📑 Content Disclaimer

This application aggregates publicly available RSS feeds from third-party publishers (e.g., BBC, Bloomberg, The Guardian, New York Times, Wired, MIT News, Financial Times, Forbes).

All news articles, headlines, and descriptions are the intellectual property of their respective publishers.

This project is intended for educational and non-commercial purposes only.

If you wish to reuse or redistribute any news content, please consult the terms of service and licensing of the original publishers.
