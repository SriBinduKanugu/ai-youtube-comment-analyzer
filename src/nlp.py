
import pandas as pd
import matplotlib.pyplot as plt
import re
import warnings

from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from wordcloud import WordCloud

warnings.filterwarnings("ignore")


# ==========================================
# 1. LOAD DATASET
# ==========================================

df = pd.read_csv("data/youtube_comments_clean.csv")

print("Dataset Loaded Successfully!")
print(df.head())


# ==========================================
# 2. DOWNLOAD NLTK RESOURCES
# ==========================================

import nltk

nltk.download("punkt")
nltk.download("punkt_tab")
nltk.download("stopwords")


# ==========================================
# 3. TEXT CLEANING
# ==========================================

def clean_text(text):

    text = str(text)

    # Convert to lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(r"http\S+|www\S+", "", text)

    # Remove punctuation, numbers and special characters
    text = re.sub(r"[^a-z\s]", "", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


df["Clean_Comment"] = df["Comment"].apply(clean_text)


print("\nOriginal vs Cleaned Comments:")
print(df[["Comment", "Clean_Comment"]].head(10))


# ==========================================
# 4. TOKENIZATION + STOPWORD REMOVAL
# ==========================================

stop_words = set(stopwords.words("english"))


def tokenize_text(text):

    tokens = word_tokenize(text)

    # Remove stopwords
    tokens = [
        word for word in tokens
        if word not in stop_words
    ]

    return tokens


df["Tokens"] = df["Clean_Comment"].apply(tokenize_text)


print("\nTokenized Comments:")
print(df[["Clean_Comment", "Tokens"]].head(10))


# ==========================================
# 5. WORD FREQUENCY ANALYSIS
# ==========================================

all_words = []

for tokens in df["Tokens"]:
    all_words.extend(tokens)


word_counts = Counter(all_words)

top_words = word_counts.most_common(20)


print("\nTop 20 Most Common Words:")

for word, count in top_words:
    print(word, ":", count)


# ==========================================
# 6. TOP 20 WORDS BAR CHART
# ==========================================

words = [item[0] for item in top_words]
counts = [item[1] for item in top_words]


plt.figure(figsize=(10, 6))

plt.bar(words, counts)

plt.title("Top 20 Most Common Words")
plt.xlabel("Words")
plt.ylabel("Frequency")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()


# ==========================================
# 7. WORD CLOUD
# ==========================================

wordcloud = WordCloud(
    width=1000,
    height=500,
    background_color="white"
).generate(" ".join(all_words))


plt.figure(figsize=(12, 6))

plt.imshow(wordcloud, interpolation="bilinear")

plt.axis("off")

plt.title("YouTube Comments Word Cloud")

plt.show()


# ==========================================
# 8. BIGRAM ANALYSIS
# ==========================================

bigrams = []

for tokens in df["Tokens"]:

    for i in range(len(tokens) - 1):

        bigram = tokens[i] + " " + tokens[i + 1]

        bigrams.append(bigram)


bigram_counts = Counter(bigrams)

top_bigrams = bigram_counts.most_common(10)


print("\nTop 10 Bigrams:")

for phrase, count in top_bigrams:

    print(phrase, ":", count)


# ==========================================
# 9. TRIGRAM ANALYSIS
# ==========================================

trigrams = []

for tokens in df["Tokens"]:

    for i in range(len(tokens) - 2):

        trigram = (
            tokens[i]
            + " "
            + tokens[i + 1]
            + " "
            + tokens[i + 2]
        )

        trigrams.append(trigram)


trigram_counts = Counter(trigrams)

top_trigrams = trigram_counts.most_common(10)


print("\nTop 10 Trigrams:")

for phrase, count in top_trigrams:

    print(phrase, ":", count)


# ==========================================
# 10. SAVE NLP DATASET
# ==========================================

df.to_csv(
    "data/youtube_comments_nlp.csv",
    index=False
)


print("\nNLP analysis completed successfully!")

print("Saved file:")
print("data/youtube_comments_nlp.csv")

