import pandas as pd
import os
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions, EmotionOptions
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# IBM Watson credentials
API_KEY = os.environ['ibm_nlu_apiKey']
SERVICE_URL = os.environ['ibm_nlu_url']

authenticator = IAMAuthenticator(API_KEY)
nlu = NaturalLanguageUnderstandingV1(
    version="2023-01-01",
    authenticator=authenticator
)
nlu.set_service_url(SERVICE_URL)

def analyze_reddit_comments(input_path, output_path):
    """Analyze Reddit comments using Watson NLU."""
    data = pd.read_csv(input_path)
    results = []

    for comment in data["comment"]:
        try:
            response = nlu.analyze(
                text=comment,
                features=Features(
                    sentiment=SentimentOptions(),
                    emotion=EmotionOptions()
                )
            ).get_result()
            sentiment = response["sentiment"]["document"]["label"]
            emotions = response["emotion"]["document"]["emotion"]
            results.append({"comment": comment, "sentiment": sentiment, **emotions})
        except Exception as e:
            print(f"Error analyzing comment: {e}")
    
    analyzed_data = pd.DataFrame(results)
    analyzed_data.to_csv(output_path, index=False)
    print(f"Analyzed data saved to {output_path}")

# Analyze Reddit comments
analyze_reddit_comments("data/cleaned/reddit_comments.csv", "data/cleaned/analyzed_reddit_comments.csv")
