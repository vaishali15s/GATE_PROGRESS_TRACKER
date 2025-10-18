import streamlit as st
import pandas as pd
import json
from datetime import datetime, date

def load_progress_data():
    """Load progress data from JSON file"""
    try:
        with open("progress_data.json", 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_progress_data(data):
    """Save progress data to JSON file"""
    with open("progress_data.json", 'w') as f:
        json.dump(data, f, indent=2, default=str)

def calculate_study_streak(progress_data):
    """Calculate current study streak"""
    if not progress_data:
        return 0
    
    dates = sorted(progress_data.keys(), reverse=True)
    streak = 0
    current_date = date.today()
    
    for date_str in dates:
        check_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        if (current_date - check_date).days == streak:
            streak += 1
        else:
            break
    
    return streak

def get_subject_progress(progress_data, subject):
    """Get progress data for a specific subject"""
    subject_data = []
    for date_str, entries in progress_data.items():
        for entry in entries:
            if entry['subject'] == subject:
                subject_data.append({
                    'date': date_str,
                    **entry
                })
    return pd.DataFrame(subject_data)

def calculate_weekly_summary(progress_data):
    """Calculate weekly study summary"""
    df_data = []
    for date_str, entries in progress_data.items():
        for entry in entries:
            row = {"date": date_str, **entry}
            df_data.append(row)
    
    if not df_data:
        return {}
    
    df = pd.DataFrame(df_data)
    df['date'] = pd.to_datetime(df['date'])
    
    # Get last 7 days
    last_week = df[df['date'] >= (datetime.now() - pd.Timedelta(days=7))]
    
    return {
        'total_hours': last_week['hours_studied'].sum(),
        'total_questions': last_week['questions_attempted'].sum(),
        'avg_confidence': last_week['confidence_level'].mean(),
        'subjects_studied': last_week['subject'].nunique()
    }

def get_improvement_suggestions(progress_data):
    """Generate improvement suggestions based on study patterns"""
    suggestions = []
    
    if not progress_data:
        return ["Start by logging your daily study sessions!"]
    
    # Convert to DataFrame for analysis
    df_data = []
    for date_str, entries in progress_data.items():
        for entry in entries:
            row = {"date": date_str, **entry}
            df_data.append(row)
    
    df = pd.DataFrame(df_data)
    
    # Check study consistency
    study_days = len(df['date'].unique())
    total_days = (datetime.now().date() - datetime.strptime(min(df['date']), "%Y-%m-%d").date()).days + 1
    consistency = study_days / total_days if total_days > 0 else 0
    
    if consistency < 0.7:
        suggestions.append("🎯 Try to maintain more consistent daily study habits")
    
    # Check subject balance
    subject_hours = df.groupby('subject')['hours_studied'].sum()
    if len(subject_hours) > 1 and subject_hours.std() / subject_hours.mean() > 0.5:
        suggestions.append("⚖️ Consider balancing your study time across different subjects")
    
    # Check confidence levels
    avg_confidence = df['confidence_level'].mean()
    if avg_confidence < 5:
        suggestions.append("📚 Focus on understanding concepts better to build confidence")
    elif avg_confidence > 8:
        suggestions.append("🚀 Great confidence! Consider tackling more challenging topics")
    
    # Check question practice
    if df['questions_attempted'].sum() == 0:
        suggestions.append("❓ Start practicing questions to test your understanding")
    else:
        accuracy = df['questions_correct'].sum() / df['questions_attempted'].sum()
        if accuracy < 0.6:
            suggestions.append("🎯 Focus on improving accuracy in question solving")
    
    return suggestions if suggestions else ["🌟 Great job! Keep up the excellent study routine!"]