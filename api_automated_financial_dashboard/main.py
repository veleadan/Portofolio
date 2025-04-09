from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as dates
from matplotlib.ticker import MaxNLocator
import feedparser
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from urllib.parse import quote


#Get a FREE key from the alphavantage API(get it from https://www.alphavantage.co/)
api_key = "8NLJ22XJJW2C3J85" # replace key with yours

# Initialize TimeSeries
ts = TimeSeries(key=api_key, output_format='pandas')

symbol = "AMZN" # insert a company code to extract info

data, meta_data = ts.get_daily(symbol=symbol, outputsize="compact")

print(data.head())

data.to_csv(f"{symbol}_daily_data.csv")

#### Plot graph ##########
data = pd.read_csv(f"{symbol}_daily_data.csv")  # Replace with your downloaded file

data['date'] = pd.to_datetime(data['date'], errors='coerce')

plt.plot(data["date"], data["4. close"])
plt.title(f"{symbol} Stock Price", fontsize=14)
plt.xlabel("Date", fontsize=12)
plt.ylabel("Close Price", fontsize=12)

ax = plt.gca()  # Get the current axis
ax.xaxis.set_major_locator(MaxNLocator(nbins=6))  # Show 6 date ticks by default

# Format X-axis as dates
ax.xaxis.set_major_formatter(dates.DateFormatter("%Y-%m-%d"))  # Format dates as 'YYYY-MM-DD'

# Rotate and format the x-ticks
plt.xticks(rotation=45, fontsize=10)
plt.legend(loc="upper left", fontsize=10)
plt.tight_layout()

plt.savefig(f"{symbol}_plot_image.png", dpi=300)

# Search query (e.g., Apple news) #
query = f"{symbol} stock"
encoded_query = quote(query)  # Properly encode the query
rss_url = f"https://news.google.com/rss/search?q={encoded_query}"
feed_data = feedparser.parse(rss_url)

# Initialize VADER for Sentiment Analysis #
analyzer = SentimentIntensityAnalyzer()
news_data = []

# Analyze sentiment for each news headline
for entry in feed_data.entries:
    title = entry.title
    sentiment = analyzer.polarity_scores(title)

    # Extract compound sentiment score (overall sentiment)
    compound_score = sentiment["compound"]

    if compound_score >= 0.10: # set above what sentiment score would you like too see articles
        # Print the title and sentiment score
        print(f"Title: {title}")
        print(f"Sentiment Score (Compound): {compound_score}")
        print(f"Published: {entry.published}")
        print(f"Link: {entry.link}\n")
        # Populate sentiment data
        news_data.append({
            "Title": title,
            "Published": entry.published,
            "Link": entry.link,
            "Sentiment": sentiment["compound"]
        })



# Convert to a DataFrame and save to CSV
news_df = pd.DataFrame(news_data)
news_df.to_csv(f"{symbol}_news_sentiment.csv", index=False)