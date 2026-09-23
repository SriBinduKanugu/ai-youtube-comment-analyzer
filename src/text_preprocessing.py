import pandas as pd
import string
import emoji
import re
import nltk
from nltk.tokenize import word_tokenize
import nltk

nltk.download("punkt")
nltk.download("punkt_tab")

# Download tokenizer (Run only once, then it will use the local copy)
nltk.download("punkt")

# Read cleaned dataset
df = pd.read_csv("data/youtube_comments_clean.csv")

print("========== BEFORE PREPROCESSING ==========\n")
print(df["Comment"].head())

# -----------------------------------------
# Convert to Lowercase
# -----------------------------------------
df["Comment"] = df["Comment"].str.lower()

# -----------------------------------------
# Remove Punctuation
# -----------------------------------------
def remove_punctuation(text):
    for char in string.punctuation:
        text = text.replace(char, "")
    return text

df["Comment"] = df["Comment"].apply(remove_punctuation)

# -----------------------------------------
# Remove Emojis
# -----------------------------------------
def remove_emojis(text):
    return emoji.replace_emoji(text, replace="")

df["Comment"] = df["Comment"].apply(remove_emojis)

# -----------------------------------------
# Remove URLs
# -----------------------------------------
def remove_urls(text):
    return re.sub(r"http\S+|www\S+", "", text)

df["Comment"] = df["Comment"].apply(remove_urls)

# -----------------------------------------
# Remove Extra Spaces
# -----------------------------------------
def remove_extra_spaces(text):
    return " ".join(text.split())

df["Comment"] = df["Comment"].apply(remove_extra_spaces)

# -----------------------------------------
# Tokenization
# -----------------------------------------
def tokenize_text(text):
    return word_tokenize(text)

df["Tokens"] = df["Comment"].apply(tokenize_text)

print("\n========== AFTER PREPROCESSING ==========\n")
print(df[["Comment", "Tokens"]].head())

# Save preprocessed dataset
df.to_csv("data/youtube_comments_preprocessed.csv", index=False)

print("\nText Preprocessing Completed Successfully!")