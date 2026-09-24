# AI YouTube Comment Analyzer

A Python-based application that analyzes YouTube comments and helps understand audience sentiment and feedback.

## Features

- Fetch YouTube comments using YouTube Data API
- Clean and process comment data
- Analyze comment length and word count
- Perform sentiment analysis using VADER
- View Positive, Neutral, and Negative comments
- Analyze likes and comment length
- Interactive Streamlit dashboard
- Analyze different YouTube videos using their URLs

## Technologies Used

- Python
- Pandas
- Streamlit
- Matplotlib
- VADER Sentiment
- YouTube Data API

## How It Works

YouTube Video URL  
↓  
Fetch Comments  
↓  
Data Cleaning  
↓  
Feature Creation  
↓  
Sentiment Analysis  
↓  
Interactive Dashboard

## Project Structure

AI-Youtube-comment-analyzer/
│
├── app.py
├── main.py
├── src/
├── data/
├── .gitignore
└── README.md

## How to Run

1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/ai-youtube-comment-analyzer.git

Open the project folder
cd ai-youtube-comment-analyzer
3. Install the required libraries
pip install -r requirements.txt
4. Create a .env file

Create a .env file in the project folder and add your YouTube API key:

YOUTUBE_API_KEY=your_api_key_here

Do not upload the .env file to GitHub.

5. Run the application
streamlit run app.py
6. Analyze a YouTube video

Enter a YouTube video URL in the application and click Send.

Future Improvements
Fetch more comments using YouTube API pagination
Improve sentiment analysis for slang and emojis
Add keyword and topic analysis
Add more interactive visualizations
Deploy the application online
Author

Sri Bindu Kanugu

B.Tech – Computer Science and Engineering (Data Science)
