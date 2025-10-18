# GATE Progress Tracker

A comprehensive Streamlit-based web application to track GATE preparation progress with daily inputs, graphical reports, and motivational insights. Built using Python, pandas, and matplotlib to help aspirants analyze study patterns, monitor consistency, and stay motivated throughout their GATE journey.

## Features

### 📝 Daily Input
- Log daily study sessions with detailed information
- Track subjects studied, hours spent, and topics covered
- Record difficulty level and confidence ratings
- Monitor question practice and accuracy
- Add personal notes and observations

### 📊 Progress Reports
- Visual charts showing daily study hours over time
- Subject-wise study distribution analysis
- Overall statistics and metrics
- Study consistency tracking

### 🔍 Subject Analysis
- Deep dive into individual subject performance
- Confidence trend analysis for each subject
- Recent topics covered tracking
- Subject-specific metrics and insights

### 💪 Motivational Insights
- Daily motivational quotes
- Study streak tracking
- Goal setting and progress monitoring
- Personalized improvement suggestions
- Achievement celebrations

## Installation

1. Clone this repository:
```bash
git clone https://github.com/vaishali15s/GATE_PROGRESS_TRACKER.git
cd GATE_PROGRESS_TRACKER
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the Streamlit application:
```bash
streamlit run app.py
```

## Usage

1. **Daily Input**: Start by logging your daily study sessions using the "Daily Input" page
2. **View Progress**: Check your progress using the "Progress Reports" page to see visual analytics
3. **Subject Analysis**: Analyze individual subjects to identify strengths and areas for improvement
4. **Stay Motivated**: Visit the "Motivational Insights" page for encouragement and goal tracking

## File Structure

```
GATE_PROGRESS_TRACKER/
├── app.py              # Main Streamlit application
├── utils.py            # Utility functions for data processing
├── requirements.txt    # Python dependencies
├── README.md          # Project documentation
└── progress_data.json # Data storage (created automatically)
```

## Data Storage

The application stores your progress data in a local JSON file (`progress_data.json`) which is created automatically when you start logging your study sessions. This ensures your data persists between sessions.

## Technologies Used

- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **Matplotlib**: Data visualization
- **Seaborn**: Statistical data visualization
- **JSON**: Data storage format

## Contributing

Feel free to fork this repository and submit pull requests for any improvements or bug fixes.

## License

This project is open source and available under the MIT License.

**Author:** Vaishali Sharma

## Live demo

I plan to host a live demo of this Streamlit app so others can try it without cloning the repo. To view the demo once deployed visit the Streamlit share URL (will be added here after deployment).

## Quick deploy to Streamlit Community Cloud

1. Push the project to a public GitHub repository (already done for this repo).
2. Sign in at https://share.streamlit.io with your GitHub account.
3. Click "New app", choose this repository and the `main` branch, and set the main file path to `app.py`.
4. Click "Deploy". Streamlit will install dependencies from `requirements.txt` and launch the app. The site will provide a persistent public URL you can share on LinkedIn.

Notes:
- Keep `gate_progress.csv` in `.gitignore` to avoid publishing personal study data. The deployed app will create/receive CSV at runtime on the Streamlit instance.
- If you prefer a different host (Railway, Render, Vercel), I can provide step-by-step instructions.

## Suggested LinkedIn post

Use this copy when you share the project on LinkedIn (replace links):

"Excited to share my GATE Progress Tracker — a Streamlit app to log daily practice, track PYQs and study hours, and visualize progress. Try the live demo: <LIVE_DEMO_URL> or view the code on GitHub: https://github.com/vaishali15s/GATE_PROGRESS_TRACKER. Feedback and contributions welcome!"

Tips:
- Add a screenshot of the app (attach as image in the post) for more engagement.
- Pin the GitHub repo link in the first comment or in the post body.
