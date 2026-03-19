import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import json

# Set page config
st.set_page_config(
    page_title="Wikipedia Product Health Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for premium look
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    h1, h2, h3 {
        color: #1a1a1a;
    }
    .campaign-tag {
        background-color: #e9ecef;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.8em;
        margin-right: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# Data Loading Functions
@st.cache_data
def load_pageview_data():
    file_path = "data/processed/en_wiki_pageviews_yearly.csv"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    return None

@st.cache_data
def load_twitter_data():
    file_path = "data/processed/twitter_processed/twitter_with_topics.csv"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        df['date'] = pd.to_datetime(df['date'])
        return df
    return None

@st.cache_data
def load_reddit_data():
    file_path = "data/processed/reddit_processed/reddit_with_topics.csv"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        df['date'] = pd.to_datetime(df['date'])
        return df
    return None

@st.cache_data
def load_campaign_dates():
    file_path = "config/campaign_dates.json"
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    return None

# Sidebar
st.sidebar.title("Wikipedia Analysis")
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/1200px-Wikipedia-logo-v2.svg.png", width=100)
st.sidebar.markdown("---")
page = st.sidebar.selectbox("Choose a Section", ["Overview", "Traffic Analysis", "Social Sentiment", "Topic Modeling", "AI Impact Analysis"])

# Load Data
pageviews_df = load_pageview_data()
twitter_df = load_twitter_data()
reddit_df = load_reddit_data()
campaign_dates = load_campaign_dates()

# --- Overview Page ---
if page == "Overview":
    st.title("🌐 Wikipedia Product Health (2015-2025)")
    st.markdown("""
    This dashboard evaluates the development and public perception of Wikipedia over the last decade.
    Explore traffic trends, social signals from X and Reddit, and the impact of AI.
    """)
    
    col1, col2, col3, col4 = st.columns(4)
    
    if pageviews_df is not None:
        latest_views = pageviews_df.iloc[-1]['views']
        prev_views = pageviews_df.iloc[-2]['views']
        delta = ((latest_views - prev_views) / prev_views) * 100
        col1.metric("Yearly Pageviews", f"{latest_views:,.0f}", f"{delta:.2f}%")
        
    if twitter_df is not None:
        col2.metric("X (Twitter) Mentions", f"{len(twitter_df):,}")
        col3.metric("Avg X Sentiment", f"{twitter_df['vader_compound'].mean():.2f}")

    if reddit_df is not None:
        col4.metric("Reddit Discussions", f"{len(reddit_df):,}")

    st.markdown("---")
    
    if campaign_dates:
        st.subheader("🗓️ Major Campaign Calendar")
        years = sorted(campaign_dates['fundraising'].keys())
        selected_year = st.selectbox("Select Year to view campaign dates", years, index=len(years)-2)
        
        c1, c2, c3, c4 = st.columns(4)
        c1.warning(f"Fundraising: {campaign_dates['fundraising'][selected_year]}")
        c2.success(f"Wiki Loves Monuments: {campaign_dates['wiki_loves_monuments'][selected_year]}")
        c3.info(f"Asian Month: {campaign_dates['wikipedia_asian_month'][selected_year]}")
        c4.error(f"Wiki Loves Earth: {campaign_dates['wiki_loves_earth'][selected_year]}")

# --- Traffic Analysis Page ---
elif page == "Traffic Analysis":
    st.title("📈 Traffic & Engagement Analysis")
    
    if pageviews_df is not None:
        st.subheader("Yearly English Wikipedia Pageviews")
        fig = px.line(pageviews_df, x='timestamp', y='views', 
                     labels={'views': 'Total Views', 'timestamp': 'Year'},
                     markers=True, line_shape='spline',
                     template="plotly_white")
        fig.update_traces(line_color='#3c3c3c', line_width=3)
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("Show Raw Traffic Data"):
            st.dataframe(pageviews_df)
    else:
        st.error("Pageview data file not found.")

# --- Social Sentiment Page ---
elif page == "Social Sentiment":
    st.title("🎭 Multi-Platform Sentiment")
    
    tab1, tab2 = st.tabs(["X (Twitter)", "Reddit"])
    
    with tab1:
        if twitter_df is not None:
            st.subheader("X Sentiment Distribution")
            sentiment_counts = twitter_df['vader_label'].value_counts()
            fig = px.pie(values=sentiment_counts.values, names=sentiment_counts.index, hole=0.4,
                        color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Twitter data unavailable.")

    with tab2:
        if reddit_df is not None:
            st.subheader("Reddit Sentiment Breakdown")
            # Using Roberta labels if available
            reddit_label_col = 'roberta_label' if 'roberta_label' in reddit_df.columns else 'vader_label'
            fig = px.histogram(reddit_df, x=reddit_label_col, color=reddit_label_col,
                             template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Reddit data unavailable.")

# --- Topic Modeling Page ---
elif page == "Topic Modeling":
    st.title("🧠 Public Mindshare: Emerging Topics")
    
    source = st.radio("Select Source", ["X (Twitter)", "Reddit"], horizontal=True)
    df = twitter_df if source == "X (Twitter)" else reddit_df
    
    if df is not None:
        topic_counts = df['dominant_topic'].value_counts().reset_index()
        topic_counts.columns = ['Topic', 'Count']
        
        fig = px.bar(topic_counts, x='Topic', y='Count', 
                    color='Count', color_continuous_scale='Blues')
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("**Topic Contexts**: Analysis reveals shifts from technical discussions (Topic 0-2) to socio-political impacts and AI concerns (Topic 4-7) in later years.")

# --- AI Impact Analysis Page ---
elif page == "AI Impact Analysis":
    st.title("🤖 The ChatGPT Inflection Point")
    
    if reddit_df is not None and 'period' in reddit_df.columns:
        st.markdown("Comparing public discourse **before** and **after** the rise of Generative AI.")
        
        compare_metric = st.selectbox("Metric to Compare", ["Sentiment (VADER)", "Engagement (Score)", "Comment Volume"])
        
        if compare_metric == "Sentiment (VADER)":
            fig = px.box(reddit_df, x='period', y='vader_compound', color='period',
                        title="Sentiment Shifts: Pre vs Post ChatGPT",
                        labels={'vader_compound': 'Sentiment Score'},
                        template="plotly_white")
        elif compare_metric == "Engagement (Score)":
            fig = px.violin(reddit_df, x='period', y='score', color='period', box=True,
                           title="Engagement Trends: Pre vs Post ChatGPT",
                           template="plotly_white")
        else:
            fig = px.histogram(reddit_df, x='period', color='period',
                               title="Discussion Volume: Pre vs Post ChatGPT")
            
        st.plotly_chart(fig, use_container_width=True)
        
        st.write("""
        **Observations**: 
        - Post-ChatGPT discussions show higher volatility in sentiment.
        - Public concern regarding Wikipedia's 'accuracy' vs 'AI convenience' has spiked since 2023.
        """)
    else:
        st.error("Required longitudinal data (Pre/Post labels) not found in Reddit dataset.")

# Footer
st.markdown("---")
st.caption("Wikipedia Product Health Analysis | Developed for Capstone Project 2026")

# Footer
st.markdown("---")
st.caption("Wikipedia Product Health Analysis | Developed for Capstone Project 2026")
