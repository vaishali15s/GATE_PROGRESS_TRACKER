import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, date
import json
import os

# Configure page
st.set_page_config(
    page_title="GATE Progress Tracker",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Data file path
DATA_FILE = "progress_data.json"

def load_data():
    """Load progress data from JSON file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_data(data):
    """Save progress data to JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2, default=str)

def main():
    st.title("📚 GATE Progress Tracker")
    st.markdown("### Track your GATE preparation journey with daily inputs and visual insights")
    
    # Load existing data
    progress_data = load_data()
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a page", 
                               ["Daily Input", "Progress Reports", "Subject Analysis", "Motivational Insights"])
    
    if page == "Daily Input":
        daily_input_page(progress_data)
    elif page == "Progress Reports":
        progress_reports_page(progress_data)
    elif page == "Subject Analysis":
        subject_analysis_page(progress_data)
    elif page == "Motivational Insights":
        motivational_insights_page(progress_data)

def daily_input_page(progress_data):
    st.header("📝 Daily Study Input")
    
    # Date selection
    study_date = st.date_input("Study Date", value=date.today())
    date_str = study_date.strftime("%Y-%m-%d")
    
    # Subject selection
    subjects = ["Mathematics", "Physics", "Chemistry", "English", "Aptitude", "Engineering Graphics", 
                "Computer Science", "Electrical", "Mechanical", "Civil", "Electronics"]
    selected_subject = st.selectbox("Subject", subjects)
    
    # Study details
    col1, col2 = st.columns(2)
    with col1:
        hours_studied = st.number_input("Hours Studied", min_value=0.0, max_value=24.0, step=0.5, value=0.0)
        topics_covered = st.text_area("Topics Covered", placeholder="List the topics you studied today...")
    
    with col2:
        difficulty_level = st.select_slider("Difficulty Level", 
                                          options=["Very Easy", "Easy", "Medium", "Hard", "Very Hard"],
                                          value="Medium")
        confidence_level = st.slider("Confidence Level (1-10)", min_value=1, max_value=10, value=5)
    
    # Questions practice
    st.subheader("Question Practice")
    col3, col4 = st.columns(2)
    with col3:
        questions_attempted = st.number_input("Questions Attempted", min_value=0, step=1, value=0)
    with col4:
        questions_correct = st.number_input("Questions Correct", min_value=0, step=1, value=0)
    
    # Notes and observations
    notes = st.text_area("Notes & Observations", placeholder="Any additional notes about today's study session...")
    
    # Save button
    if st.button("Save Today's Progress", type="primary"):
        if date_str not in progress_data:
            progress_data[date_str] = []
        
        entry = {
            "subject": selected_subject,
            "hours_studied": hours_studied,
            "topics_covered": topics_covered,
            "difficulty_level": difficulty_level,
            "confidence_level": confidence_level,
            "questions_attempted": questions_attempted,
            "questions_correct": questions_correct,
            "notes": notes,
            "timestamp": datetime.now().isoformat()
        }
        
        progress_data[date_str].append(entry)
        save_data(progress_data)
        st.success("✅ Progress saved successfully!")
        st.balloons()

def progress_reports_page(progress_data):
    st.header("📊 Progress Reports")
    
    if not progress_data:
        st.warning("No data available. Start by adding daily study entries!")
        return
    
    # Convert data to DataFrame
    df_data = []
    for date_str, entries in progress_data.items():
        for entry in entries:
            row = {"date": date_str, **entry}
            df_data.append(row)
    
    df = pd.DataFrame(df_data)
    df['date'] = pd.to_datetime(df['date'])
    
    # Overall statistics
    st.subheader("📈 Overall Statistics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_hours = df['hours_studied'].sum()
        st.metric("Total Hours Studied", f"{total_hours:.1f}")
    
    with col2:
        total_questions = df['questions_attempted'].sum()
        st.metric("Total Questions Attempted", f"{total_questions}")
    
    with col3:
        avg_confidence = df['confidence_level'].mean()
        st.metric("Average Confidence", f"{avg_confidence:.1f}/10")
    
    with col4:
        study_days = len(df['date'].dt.date.unique())
        st.metric("Study Days", f"{study_days}")
    
    # Daily hours chart
    st.subheader("📅 Daily Study Hours")
    daily_hours = df.groupby('date')['hours_studied'].sum().reset_index()
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(daily_hours['date'], daily_hours['hours_studied'], marker='o', linewidth=2, markersize=6)
    ax.set_title('Daily Study Hours Over Time')
    ax.set_xlabel('Date')
    ax.set_ylabel('Hours Studied')
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)
    
    # Subject-wise distribution
    st.subheader("📚 Subject-wise Study Distribution")
    subject_hours = df.groupby('subject')['hours_studied'].sum().sort_values(ascending=False)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    subject_hours.plot(kind='bar', ax=ax, color='skyblue')
    ax.set_title('Hours Studied by Subject')
    ax.set_xlabel('Subject')
    ax.set_ylabel('Total Hours')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

def subject_analysis_page(progress_data):
    st.header("🔍 Subject Analysis")
    
    if not progress_data:
        st.warning("No data available. Start by adding daily study entries!")
        return
    
    # Convert data to DataFrame
    df_data = []
    for date_str, entries in progress_data.items():
        for entry in entries:
            row = {"date": date_str, **entry}
            df_data.append(row)
    
    df = pd.DataFrame(df_data)
    
    # Subject selector
    subjects = df['subject'].unique()
    selected_subject = st.selectbox("Select Subject for Analysis", subjects)
    
    subject_df = df[df['subject'] == selected_subject]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"📊 {selected_subject} - Key Metrics")
        total_hours = subject_df['hours_studied'].sum()
        avg_confidence = subject_df['confidence_level'].mean()
        total_questions = subject_df['questions_attempted'].sum()
        correct_questions = subject_df['questions_correct'].sum()
        accuracy = (correct_questions / total_questions * 100) if total_questions > 0 else 0
        
        st.metric("Total Hours", f"{total_hours:.1f}")
        st.metric("Average Confidence", f"{avg_confidence:.1f}/10")
        st.metric("Question Accuracy", f"{accuracy:.1f}%")
    
    with col2:
        st.subheader("📈 Confidence Trend")
        if len(subject_df) > 1:
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.plot(pd.to_datetime(subject_df['date']), subject_df['confidence_level'], 
                   marker='o', linewidth=2, color='green')
            ax.set_title(f'{selected_subject} - Confidence Over Time')
            ax.set_ylabel('Confidence Level')
            ax.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.info("Need more data points to show trend")
    
    # Recent topics
    st.subheader("📝 Recent Topics Covered")
    recent_topics = subject_df.nlargest(5, 'date')[['date', 'topics_covered', 'confidence_level']]
    st.dataframe(recent_topics, use_container_width=True)

def motivational_insights_page(progress_data):
    st.header("💪 Motivational Insights")
    
    if not progress_data:
        st.warning("No data available. Start by adding daily study entries!")
        return
    
    # Convert data to DataFrame
    df_data = []
    for date_str, entries in progress_data.items():
        for entry in entries:
            row = {"date": date_str, **entry}
            df_data.append(row)
    
    df = pd.DataFrame(df_data)
    df['date'] = pd.to_datetime(df['date'])
    
    # Motivational quotes
    quotes = [
        "\"Success is not final, failure is not fatal: it is the courage to continue that counts.\" - Winston Churchill",
        "\"The future belongs to those who believe in the beauty of their dreams.\" - Eleanor Roosevelt",
        "\"Don't watch the clock; do what it does. Keep going.\" - Sam Levenson",
        "\"The only impossible journey is the one you never begin.\" - Tony Robbins",
        "\"Success is walking from failure to failure with no loss of enthusiasm.\" - Winston Churchill"
    ]
    
    import random
    st.info(random.choice(quotes))
    
    # Progress insights
    total_hours = df['hours_studied'].sum()
    study_days = len(df['date'].dt.date.unique())
    avg_daily_hours = total_hours / study_days if study_days > 0 else 0
    
    st.subheader("🎯 Your Journey So Far")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Study Streak", f"{study_days} days")
        if study_days >= 7:
            st.success("🔥 Great consistency!")
        elif study_days >= 3:
            st.info("👍 Good start!")
        else:
            st.warning("⚡ Keep going!")
    
    with col2:
        st.metric("Daily Average", f"{avg_daily_hours:.1f} hours")
        if avg_daily_hours >= 6:
            st.success("🚀 Excellent dedication!")
        elif avg_daily_hours >= 4:
            st.info("📈 Good progress!")
        else:
            st.warning("💪 You can do more!")
    
    with col3:
        recent_confidence = df.nlargest(5, 'date')['confidence_level'].mean()
        st.metric("Recent Confidence", f"{recent_confidence:.1f}/10")
        if recent_confidence >= 7:
            st.success("😊 Feeling confident!")
        elif recent_confidence >= 5:
            st.info("🙂 Steady progress!")
        else:
            st.warning("📚 Keep studying!")
    
    # Goal setting
    st.subheader("🎯 Set Your Goals")
    daily_goal = st.number_input("Daily Study Hours Goal", min_value=1.0, max_value=16.0, value=6.0, step=0.5)
    
    if avg_daily_hours >= daily_goal:
        st.success(f"🎉 Congratulations! You're meeting your daily goal of {daily_goal} hours!")
    else:
        remaining = daily_goal - avg_daily_hours
        st.info(f"📈 You need {remaining:.1f} more hours per day to reach your goal!")

if __name__ == "__main__":
    main()