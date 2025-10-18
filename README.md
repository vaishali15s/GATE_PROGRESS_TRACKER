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
