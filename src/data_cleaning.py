import pandas as pd


# ============================================================
# CLEAN COMMENTS
# ============================================================

def clean_comments():

    # Read fresh comments
    df = pd.read_csv(
        "data/youtube_comments.csv"
    )

    # Convert Published column to datetime
    df["Published"] = pd.to_datetime(
        df["Published"]
    )

    # Create comment length
    df["Comment_Length"] = (
        df["Comment"].str.len()
    )

    # Create word count
    df["Word_Count"] = (
        df["Comment"].str.split().str.len()
    )

    # Save cleaned dataset
    df.to_csv(
        "data/youtube_comments_clean.csv",
        index=False
    )

    return df