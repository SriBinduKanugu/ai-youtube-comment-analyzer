
from googleapiclient.discovery import build
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qs
import os
import pandas as pd


# LOAD API KEY

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

if not API_KEY:
    raise ValueError("YouTube API key not found in .env file")


# CONNECT TO YOUTUBE API

youtube = build(
    "youtube",
    "v3",
    developerKey=API_KEY
)


# EXTRACT VIDEO ID

def get_video_id(url):

    parsed_url = urlparse(url)

    if "youtube.com" in parsed_url.netloc:

        video_id = parse_qs(
            parsed_url.query
        ).get("v", [None])[0]

    elif "youtu.be" in parsed_url.netloc:

        video_id = parsed_url.path.strip("/")

    else:

        video_id = None

    return video_id


# FETCH COMMENTS WITH PAGINATION

def fetch_comments(url):

    video_id = get_video_id(url)

    if not video_id:
        raise ValueError("Invalid YouTube URL")

    comments_data = []
    next_page_token = None

    while True:

        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,
            pageToken=next_page_token
        )

        response = request.execute()

        for item in response.get("items", []):

            snippet = item[
                "snippet"
            ][
                "topLevelComment"
            ][
                "snippet"
            ]

            comments_data.append({

                "Author": snippet["authorDisplayName"],

                "Comment": snippet["textOriginal"],

                "Likes": snippet["likeCount"],

                "Published": snippet["publishedAt"]

            })

        next_page_token = response.get("nextPageToken")

        if not next_page_token:
            break

    if not comments_data:

        raise ValueError(
            "No comments found for this video."
        )

    df = pd.DataFrame(comments_data)

    # CREATE DATA FOLDER IF NEEDED

    os.makedirs("data", exist_ok=True)

    # SAVE COMMENTS

    df.to_csv(
        "data/youtube_comments.csv",
        index=False
    )

    print("Total comments fetched:", len(df))

    return df
