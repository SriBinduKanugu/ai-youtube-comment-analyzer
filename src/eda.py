
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# 1. LOAD DATA
# ============================================================

df = pd.read_csv("data/youtube_comments_sentiment.csv")

print("\n" + "=" * 60)
print("YOUTUBE COMMENT ANALYSIS - EDA")
print("=" * 60)

print("\nFirst 5 rows:")
print(df.head())


# ============================================================
# 2. BASIC INFORMATION
# ============================================================

print("\nDataset Shape:")
print(df.shape)

print("\nMissing Values:")
print(df.isnull().sum())


# ============================================================
# 3. DESCRIPTIVE STATISTICS
# ============================================================

print("\nDescriptive Statistics:")
print(df.describe())


# ============================================================
# 4. BASIC ANALYSIS
# ============================================================

print("\nBasic Analysis")

print("Maximum Likes:", df["Likes"].max())
print("Minimum Likes:", df["Likes"].min())
print("Average Likes:", round(df["Likes"].mean(), 2))


# ------------------------------------------------------------
# Most Liked Comment
# ------------------------------------------------------------

most_liked = df.loc[df["Likes"].idxmax()]

print("\nMost Liked Comment:")
print("Author:", most_liked["Author"])
print("Comment:", most_liked["Comment"])
print("Likes:", most_liked["Likes"])


# ------------------------------------------------------------
# Longest Comment
# ------------------------------------------------------------

longest_comment = df.loc[df["Comment_Length"].idxmax()]

print("\nLongest Comment:")
print("Author:", longest_comment["Author"])
print("Comment:", longest_comment["Comment"])
print("Comment Length:", longest_comment["Comment_Length"])


# ============================================================
# 5. TOP 10 LONGEST COMMENTS
# ============================================================

top_longest = df.sort_values(
    by="Comment_Length",
    ascending=False
).head(10)

print("\nTop 10 Longest Comments:")
print(
    top_longest[
        ["Author", "Comment_Length", "Likes"]
    ]
)


# ============================================================
# 6. TOP COMMENT AUTHORS
# ============================================================

author_counts = df["Author"].value_counts().head(10)

print("\nTop 10 Comment Authors:")
print(author_counts)


# ============================================================
# 7. CORRELATION
# ============================================================

correlation = df["Comment_Length"].corr(df["Likes"])

print("\nCorrelation between Comment Length and Likes:")
print(round(correlation, 3))


# ============================================================
# 8. SENTIMENT ANALYSIS
# ============================================================

sentiment_counts = df["Sentiment"].value_counts()

print("\nSentiment Distribution:")
print(sentiment_counts)


sentiment_likes = df.groupby("Sentiment")["Likes"].mean()

print("\nAverage Likes by Sentiment:")
print(sentiment_likes.round(2))


# ============================================================
# 9. PREPARE DASHBOARD DATA
# ============================================================

# Top 10 most liked comments
top_likes = df.sort_values(
    by="Likes",
    ascending=False
).head(10)


# ============================================================
# 10. CREATE EDA DASHBOARD
# ============================================================

fig, axes = plt.subplots(
    2,
    3,
    figsize=(16, 9)
)

fig.suptitle(
    "YouTube Comment Analysis Dashboard",
    fontsize=20,
    fontweight="bold"
)


# ============================================================
# GRAPH 1: TOP 10 MOST LIKED COMMENTS
# ============================================================

axes[0, 0].bar(
    range(len(top_likes)),
    top_likes["Likes"]
)

axes[0, 0].set_title(
    "Top 10 Most Liked Comments",
    fontsize=13,
    fontweight="bold"
)

axes[0, 0].set_xlabel("Comment Rank")
axes[0, 0].set_ylabel("Likes")

axes[0, 0].set_xticks(range(len(top_likes)))
axes[0, 0].set_xticklabels(
    range(1, len(top_likes) + 1)
)


# ============================================================
# GRAPH 2: COMMENT LENGTH DISTRIBUTION
# ============================================================

axes[0, 1].hist(
    df["Comment_Length"],
    bins=20
)

axes[0, 1].set_title(
    "Comment Length Distribution",
    fontsize=13,
    fontweight="bold"
)

axes[0, 1].set_xlabel("Comment Length (Characters)")
axes[0, 1].set_ylabel("Number of Comments")


# ============================================================
# GRAPH 3: WORD COUNT DISTRIBUTION
# ============================================================

axes[0, 2].hist(
    df["Word_Count"],
    bins=20
)

axes[0, 2].set_title(
    "Word Count Distribution",
    fontsize=13,
    fontweight="bold"
)

axes[0, 2].set_xlabel("Number of Words")
axes[0, 2].set_ylabel("Number of Comments")


# ============================================================
# GRAPH 4: COMMENT LENGTH VS LIKES
# ============================================================

axes[1, 0].scatter(
    df["Comment_Length"],
    df["Likes"],
    alpha=0.7
)

axes[1, 0].set_title(
    "Comment Length vs Likes",
    fontsize=13,
    fontweight="bold"
)

axes[1, 0].set_xlabel("Comment Length (Characters)")
axes[1, 0].set_ylabel("Likes")


# ============================================================
# GRAPH 5: SENTIMENT DISTRIBUTION
# ============================================================

axes[1, 1].bar(
    sentiment_counts.index,
    sentiment_counts.values
)

axes[1, 1].set_title(
    "Sentiment Distribution",
    fontsize=13,
    fontweight="bold"
)

axes[1, 1].set_xlabel("Sentiment")
axes[1, 1].set_ylabel("Number of Comments")


# ============================================================
# GRAPH 6: AVERAGE LIKES BY SENTIMENT
# ============================================================

axes[1, 2].bar(
    sentiment_likes.index,
    sentiment_likes.values
)

axes[1, 2].set_title(
    "Average Likes by Sentiment",
    fontsize=13,
    fontweight="bold"
)

axes[1, 2].set_xlabel("Sentiment")
axes[1, 2].set_ylabel("Average Likes")


# ============================================================
# 11. FINAL DASHBOARD FORMATTING
# ============================================================

plt.tight_layout(
    rect=[0, 0, 1, 0.95]
)

plt.show()


# ============================================================
# 12. COMPLETION MESSAGE
# ============================================================

print("\n" + "=" * 60)
print("EDA Dashboard completed successfully!")
print("=" * 60)

