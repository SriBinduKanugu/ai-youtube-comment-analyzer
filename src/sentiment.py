import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


# ============================================================
# SENTIMENT ANALYSIS
# ============================================================

def analyze_sentiment():

    # Load cleaned comments
    df = pd.read_csv(
        "data/youtube_comments_clean.csv"
    )

    # Create sentiment analyzer
    analyzer = SentimentIntensityAnalyzer()

    # Function to find sentiment
    def get_sentiment(comment):

        score = analyzer.polarity_scores(
            str(comment)
        )

        compound = score["compound"]

        if compound >= 0.05:

            return "Positive"

        elif compound <= -0.05:

            return "Negative"

        else:

            return "Neutral"

    # Apply sentiment analysis
    df["Sentiment"] = df["Comment"].apply(
        get_sentiment
    )

    # Save result
    df.to_csv(
        "data/youtube_comments_sentiment.csv",
        index=False
    )

    return df