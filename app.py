
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from src.fetch_comments import fetch_comments
from src.data_cleaning import clean_comments
from src.sentiment import analyze_sentiment


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI YouTube Comment Analyzer",
    page_icon="🎥",
    layout="wide"
)


# ============================================================
# SESSION STATE
# ============================================================

if "show_dashboard" not in st.session_state:
    st.session_state.show_dashboard = False

if "youtube_url" not in st.session_state:
    st.session_state.youtube_url = ""

if "analysis_data" not in st.session_state:
    st.session_state.analysis_data = None


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #ffd6d6 0%,
        #fff5f5 35%,
        #ffffff 65%,
        #ffd6d6 100%
    );
}

.main-title {
    text-align: center;
    color: #ff0000;
    font-size: 42px;
    font-weight: 700;
    margin-top: 70px;
    margin-bottom: 8px;
}

.subtitle {
    text-align: center;
    color: #555555;
    font-size: 18px;
    margin-top: 0px;
    margin-bottom: 25px;
}

.input-card {
    background: rgba(255, 255, 255, 0.90);
    border: 1px solid rgba(255, 120, 120, 0.35);
    border-radius: 22px;
    padding: 30px 40px 35px 40px;
    margin-top: 0px;
    box-shadow: 0 10px 35px rgba(180, 0, 0, 0.10);
}

.input-label {
    font-size: 17px;
    font-weight: 600;
    color: #222222;
    margin-bottom: 8px;
}

.stTextInput > div > div > input {
    background-color: rgba(255, 255, 255, 0.95);
    border: 2px solid #ffb3b3;
    border-radius: 12px;
    padding: 14px 16px;
    font-size: 16px;
    color: #222222;
}

.stTextInput > div > div > input:focus {
    border-color: #ff0000;
    box-shadow: 0 0 0 2px rgba(255, 0, 0, 0.12);
}

div.stButton > button {
    width: 100%;
    background-color: #ff0000;
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px;
    font-size: 16px;
    font-weight: 600;
}

div.stButton > button:hover {
    background-color: #d90000;
    color: white;
}

.dashboard-title {
    color: #ff0000;
    font-size: 36px;
    font-weight: 700;
    margin-bottom: 5px;
}

.dashboard-subtitle {
    color: #555555;
    font-size: 16px;
    margin-bottom: 25px;
}

.metric-card {
    background: rgba(255, 255, 255, 0.92);
    border-radius: 16px;
    padding: 20px;
    text-align: center;
    border: 1px solid #ffd0d0;
    box-shadow: 0 5px 20px rgba(180, 0, 0, 0.08);
}

.metric-number {
    font-size: 30px;
    font-weight: 700;
    color: #ff0000;
}

.metric-label {
    font-size: 15px;
    color: #555555;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# LANDING PAGE
# ============================================================

def show_landing_page():

    st.markdown(
        '<div class="main-title">'
        '🎥 AI YouTube Comment Analyzer'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Analyze YouTube comments and understand audience sentiment'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="input-card">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="input-label">'
        'Enter your YouTube URL'
        '</div>',
        unsafe_allow_html=True
    )

    youtube_url = st.text_input(
        "",
        placeholder="https://www.youtube.com/watch?v=...",
        label_visibility="collapsed"
    )

    # ========================================================
    # SEND BUTTON
    # ========================================================

    if st.button("Send →"):

        if youtube_url.strip() == "":

            st.warning(
                "Please enter a YouTube URL."
            )

        elif (
            "youtube.com" not in youtube_url
            and "youtu.be" not in youtube_url
        ):

            st.error(
                "Please enter a valid YouTube URL."
            )

        else:

            try:

                with st.spinner(
                    "Fetching and analyzing YouTube comments..."
                ):

                    # Step 1: Fetch fresh comments
                    fetch_comments(youtube_url)

                    # Step 2: Clean fresh comments
                    clean_comments()

                    # Step 3: Perform sentiment analysis
                    df = analyze_sentiment()

                # Store URL
                st.session_state.youtube_url = youtube_url

                # Store fresh analysis result
                st.session_state.analysis_data = df

                # Open dashboard
                st.session_state.show_dashboard = True

                st.success(
                    f"Successfully analyzed {len(df)} comments!"
                )

                st.rerun()

            except Exception as e:

                st.error(
                    f"Could not analyze video: {e}"
                )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# DASHBOARD
# ============================================================

def show_dashboard():

    # ========================================================
    # GET CURRENT ANALYSIS DATA
    # ========================================================

    df = st.session_state.analysis_data

    # ========================================================
    # DASHBOARD HEADER
    # ========================================================

    st.markdown(
        '<div class="dashboard-title">'
        '📊 YouTube Comment Analysis Dashboard'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="dashboard-subtitle">'
        f'Analyzing: {st.session_state.youtube_url}'
        '</div>',
        unsafe_allow_html=True
    )

    # ========================================================
    # BACK BUTTON
    # ========================================================

    if st.button("← Analyze another video"):

        st.session_state.show_dashboard = False
        st.session_state.youtube_url = ""
        st.session_state.analysis_data = None

        st.rerun()

    st.divider()

    # ========================================================
    # CHECK DATA
    # ========================================================

    if df is None:

        st.error(
            "No analysis data available."
        )

        return

    # ========================================================
    # BASIC DATA
    # ========================================================

    total_comments = len(df)

    total_likes = int(
        df["Likes"].sum()
    )

    # ========================================================
    # SENTIMENT COUNTS
    # ========================================================

    sentiment_counts = (
        df["Sentiment"].value_counts()
    )

    positive_count = sentiment_counts.get(
        "Positive",
        0
    )

    negative_count = sentiment_counts.get(
        "Negative",
        0
    )

    neutral_count = sentiment_counts.get(
        "Neutral",
        0
    )

    # ========================================================
    # METRIC CARDS
    # ========================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-number">
                    {total_comments}
                </div>
                <div class="metric-label">
                    Total Comments
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-number">
                    {positive_count}
                </div>
                <div class="metric-label">
                    Positive
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-number">
                    {negative_count}
                </div>
                <div class="metric-label">
                    Negative
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-number">
                    {neutral_count}
                </div>
                <div class="metric-label">
                    Neutral
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ========================================================
    # SENTIMENT ANALYSIS
    # ========================================================

    st.subheader("😊 Sentiment Analysis")

    col1, col2 = st.columns(2)

    # --------------------------------------------------------
    # PIE CHART
    # --------------------------------------------------------

    with col1:

        fig, ax = plt.subplots()

        ax.pie(
            sentiment_counts,
            labels=sentiment_counts.index,
            autopct="%1.1f%%",
            startangle=90
        )

        ax.set_title(
            "Sentiment Distribution"
        )

        st.pyplot(fig)

        plt.close(fig)

    # --------------------------------------------------------
    # BAR CHART
    # --------------------------------------------------------

    with col2:

        fig, ax = plt.subplots()

        sentiment_counts.plot(
            kind="bar",
            ax=ax
        )

        ax.set_title(
            "Number of Comments by Sentiment"
        )

        ax.set_xlabel(
            "Sentiment"
        )

        ax.set_ylabel(
            "Number of Comments"
        )

        plt.xticks(
            rotation=0
        )

        st.pyplot(fig)

        plt.close(fig)

    # ========================================================
    # TEXT INSIGHTS
    # ========================================================

    st.subheader("💡 Insights")

    most_common_sentiment = (
        sentiment_counts.idxmax()
    )

    percentage = (
        sentiment_counts.max()
        / total_comments
    ) * 100

    st.info(
        f"Most comments are "
        f"**{most_common_sentiment.lower()}**, "
        f"representing approximately "
        f"**{percentage:.1f}%** of all comments."
    )

    st.info(
        f"The dataset contains "
        f"**{total_comments} comments** "
        f"with a total of "
        f"**{total_likes} likes**."
    )

    # ========================================================
    # LIKES ANALYSIS
    # ========================================================

    st.subheader("👍 Likes Analysis")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Total Likes",
            total_likes
        )

    with col2:

        st.metric(
            "Average Likes",
            f"{df['Likes'].mean():.2f}"
        )

    # ========================================================
    # MOST LIKED COMMENTS
    # ========================================================

    st.subheader("🔥 Most Liked Comments")

    top_comments = (
        df.sort_values(
            by="Likes",
            ascending=False
        )
        .head(10)
    )

    st.dataframe(
        top_comments[
            [
                "Author",
                "Comment",
                "Likes",
                "Sentiment"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    # ========================================================
    # COMMENT LENGTH ANALYSIS
    # ========================================================

    st.subheader("📝 Comment Analysis")

    col1, col2 = st.columns(2)

    # --------------------------------------------------------
    # COMMENT LENGTH
    # --------------------------------------------------------

    with col1:

        fig, ax = plt.subplots()

        ax.hist(
            df["Comment_Length"],
            bins=20
        )

        ax.set_title(
            "Comment Length Distribution"
        )

        ax.set_xlabel(
            "Comment Length"
        )

        ax.set_ylabel(
            "Number of Comments"
        )

        st.pyplot(fig)

        plt.close(fig)

    # --------------------------------------------------------
    # WORD COUNT
    # --------------------------------------------------------

    with col2:

        fig, ax = plt.subplots()

        ax.hist(
            df["Word_Count"],
            bins=20
        )

        ax.set_title(
            "Word Count Distribution"
        )

        ax.set_xlabel(
            "Number of Words"
        )

        ax.set_ylabel(
            "Number of Comments"
        )

        st.pyplot(fig)

        plt.close(fig)

    # ========================================================
    # ALL COMMENTS
    # ========================================================

    st.subheader("💬 All Comments")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# MAIN APPLICATION
# ============================================================

if st.session_state.show_dashboard:

    show_dashboard()

else:

    show_landing_page()


