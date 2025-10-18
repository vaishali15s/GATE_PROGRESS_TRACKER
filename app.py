import streamlit as st
import pandas as pd
from datetime import date
import os
import matplotlib.pyplot as plt

# 📘 App Title
st.title("📘 GATE Progress Tracker")

# 📝 Section 1: Daily Data Input
st.subheader("📝 Enter Today's Study Data")

today = st.date_input("Date", value=date.today())
pyqs = st.number_input("PYQs Attempted", min_value=0, max_value=100)
marks = st.number_input("Marks Scored", min_value=0.0, max_value=100.0)
hours = st.number_input("Study Hours", min_value=0.0, max_value=24.0)
topics = st.multiselect("Topics Covered", [
    "Network Theory", "Analog", "EDC", "Signals", "Control Systems", "Digital",
    "Maths", "Aptitude", "Communication", "EMT"
])

data_file = "gate_progress.csv"
new_entry = {
    "Date": today,
    "PYQs Attempted": pyqs,
    "Marks Scored": marks,
    "Study Hours": hours,
    "Topics": ", ".join(topics)
}

# 💾 Submit Button
if st.button("Submit"):
    if os.path.exists(data_file):
        df_old = pd.read_csv(data_file)
        df = pd.concat([df_old, pd.DataFrame([new_entry])], ignore_index=True)
    else:
        df = pd.DataFrame([new_entry])
    df.to_csv(data_file, index=False)
    st.success("✅ Entry added successfully!")

# 🧹 Reset Data (Day 11)
st.subheader("🧹 Reset Tracker")
if st.button("Reset All Data"):
    if os.path.exists(data_file):
        os.remove(data_file)
        st.warning("⚠ All data deleted.")
    else:
        st.info("ℹ No data file found.")

# 📤 Upload CSV (Day 12)
st.subheader("📤 Upload CSV")
uploaded_file = st.file_uploader("Upload your CSV file", type="csv")
if uploaded_file is not None:
    df_uploaded = pd.read_csv(uploaded_file)
    df_uploaded.to_csv(data_file, index=False)
    st.success("📥 Uploaded and replaced previous data.")

# 📊 Section 2: Data Overview
st.subheader("📊 Study Data Summary")

if os.path.exists(data_file):
    df = pd.read_csv(data_file)
    df["Date"] = pd.to_datetime(df["Date"])

    st.dataframe(df)

    st.metric("� Days Tracked", df["Date"].nunique())
    st.metric("📖 Total PYQs", int(df["PYQs Attempted"].sum()))
    st.metric("🎯 Avg. Marks", round(df["Marks Scored"].mean(), 2))
    st.metric("⏳ Study Hours", round(df["Study Hours"].sum(), 1))

    best_day = df[df["Marks Scored"] == df["Marks Scored"].max()]["Date"].dt.strftime('%Y-%m-%d').values[0]
    st.metric("🏆 Best Performance", best_day)

    # 📈 Marks & Hours Chart
    st.markdown("### � Progress Chart")
    fig, ax = plt.subplots()
    ax.plot(df["Date"], df["Marks Scored"], label="Marks", color="green", marker='o')
    ax.plot(df["Date"], df["Study Hours"], label="Hours", color="blue", linestyle='--', marker='x')
    ax.set_xlabel("Date")
    ax.set_ylabel("Value")
    ax.set_title("Marks vs Study Hours")
    ax.legend()
    st.pyplot(fig)

    # 📊 PYQs Bar Chart
    st.markdown("### 🧪 PYQs Attempted")
    fig2, ax2 = plt.subplots()
    ax2.bar(df["Date"].dt.strftime('%b %d'), df["PYQs Attempted"], color='purple')
    ax2.set_xlabel("Date")
    ax2.set_ylabel("PYQs")
    ax2.set_title("PYQs Attempted")
    st.pyplot(fig2)

    # 🔍 Filter Section
    st.subheader("🔍 Filter Data")
    start_date = st.date_input("Start Date", value=df["Date"].min())
    end_date = st.date_input("End Date", value=df["Date"].max())
    all_topics = sorted(set(t for sub in df["Topics"].dropna().str.split(', ') for t in sub))
    selected_topics = st.multiselect("Select Topics", all_topics)

    filtered_df = df[(df["Date"] >= pd.to_datetime(start_date)) & (df["Date"] <= pd.to_datetime(end_date))]
    if selected_topics:
        filtered_df = filtered_df[filtered_df["Topics"].str.contains('|'.join(selected_topics), case=False)]

    st.markdown("### 📄 Filtered Data")
    st.dataframe(filtered_df)

    # 🗓 Weekly Summary
    st.subheader("� Weekly Summary")
    df["Week"] = df["Date"].dt.to_period("W").astype(str)
    weekly_summary = df.groupby("Week").agg({
        "PYQs Attempted": "sum",
        "Marks Scored": "mean",
        "Study Hours": "sum"
    }).reset_index()
    st.dataframe(weekly_summary)

    fig3, ax3 = plt.subplots()
    ax3.bar(weekly_summary["Week"], weekly_summary["Study Hours"], color='orange')
    ax3.set_title("Weekly Study Hours")
    ax3.set_ylabel("Hours")
    st.pyplot(fig3)

    # ⚙ Study Efficiency
    st.subheader("⚙ Study Efficiency")
    df["Efficiency"] = df["Marks Scored"] / df["Study Hours"]
    st.line_chart(df.set_index("Date")["Efficiency"].fillna(0))

    max_eff = df["Efficiency"].max()
    eff_day = df[df["Efficiency"] == max_eff]["Date"].dt.strftime('%Y-%m-%d').values[0]
    st.metric("📈 Best Efficiency", eff_day)

    # 📥 Download Filtered Data
    st.subheader("⬇ Export Filtered Data")
    if not filtered_df.empty:
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV", csv, "filtered_gate_data.csv", "text/csv")
    else:
        st.info("No data available to export.")

    # ✅ Subject-Wise Scoreboard (Day 13)
    st.subheader("� Subject-Wise Scoreboard")
    subject_df = pd.DataFrame(columns=["Subject", "Days", "Total PYQs", "Avg Marks", "Total Hours"])

    for subject in all_topics:
        sub_entries = df[df["Topics"].str.contains(subject, na=False)]
        if not sub_entries.empty:
            subject_df = pd.concat([subject_df, pd.DataFrame([{
                "Subject": subject,
                "Days": sub_entries["Date"].nunique(),
                "Total PYQs": sub_entries["PYQs Attempted"].sum(),
                "Avg Marks": round(sub_entries["Marks Scored"].mean(), 2),
                "Total Hours": round(sub_entries["Study Hours"].sum(), 1)
            }])])

    subject_df = subject_df.sort_values(by="Total Hours", ascending=False)
    st.dataframe(subject_df)

    # 📊 Visual Dashboard for Topics (Day 14)
    st.subheader("📊 Visual Dashboard")

    topic_freq = {}
    topic_hours = {}

    for index, row in df.iterrows():
        for topic in str(row["Topics"]).split(", "):
            topic_freq[topic] = topic_freq.get(topic, 0) + 1
            topic_hours[topic] = topic_hours.get(topic, 0) + float(row["Study Hours"])

    freq_df = pd.DataFrame({
        "Topic": list(topic_freq.keys()),
        "Days Studied": list(topic_freq.values()),
        "Total Hours": list(topic_hours.values())
    }).sort_values(by="Total Hours", ascending=False)

    fig4, ax4 = plt.subplots()
    ax4.pie(freq_df["Days Studied"], labels=freq_df["Topic"], autopct="%1.1f%%", startangle=90)
    ax4.axis('equal')
    st.pyplot(fig4)

    fig5, ax5 = plt.subplots()
    ax5.bar(freq_df["Topic"], freq_df["Total Hours"], color='teal')
    ax5.set_ylabel("Total Hours")
    ax5.set_xlabel("Topic")
    ax5.set_title("Topic Mastery")
    st.pyplot(fig5)

else:
    st.info("🔔 No data yet. Add your first study entry.")

# 🌟 Motivation
st.markdown("> 🌟 *\"Discipline is the bridge between goals and accomplishment.\" – Jim Rohn*")