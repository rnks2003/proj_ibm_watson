from flask import Flask, render_template, request, redirect, url_for
import os
import pandas as pd
from scripts.reddit_data_collection import collect_reddit_data
from scripts.preprocess_reddit_data import preprocess_reddit_data
from scripts.ibm_watson_nlu import analyze_reddit_comments

app = Flask(__name__)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/collect_data', methods=['POST'])
def collect_data():
    subreddit_name = request.form.get('subreddit_name')
    try:
        # Collect Reddit data
        data = collect_reddit_data(subreddit_name)
        # Save collected data to CSV
        data.to_csv('data/raw/reddit_data.csv', index=False)
        return redirect(url_for('preprocess_data'))
    except Exception as e:
        return f"Error collecting data: {e}"

@app.route('/preprocess_data')
def preprocess_data():
    try:
        # Preprocess data
        preprocess_reddit_data('data/raw/reddit_data.csv', 'data/cleaned/reddit_comments.csv')
        return redirect(url_for('analyze_data'))
    except Exception as e:
        return f"Error preprocessing data: {e}"

@app.route('/analyze_data')
def analyze_data():
    try:
        # Analyze sentiment and emotions
        analyze_reddit_comments('data/cleaned/reddit_comments.csv', 'data/cleaned/analyzed_reddit_comments.csv')
        analyzed_data = pd.read_csv('data/cleaned/analyzed_reddit_comments.csv')
        return render_template('results.html', data=analyzed_data.to_dict(orient='records'))
    except Exception as e:
        return f"Error analyzing data: {e}"

if __name__ == '__main__':
    app.run(debug=True)
