import praw
import pandas as pd
import os

# Set up the Reddit API client
reddit = praw.Reddit(
    client_id=os.environ['reddit_ibm_client_id'],  # Replace with your client_id
    client_secret=os.environ['reddit_ibm_client_secret'],  # Replace with your client_secret
    user_agent=os.environ['reddit_ibm_user_agent']  # Replace with your user_agent
)

def collect_reddit_data(subreddit_name, limit=100):
    """
    Collects post titles and comments from a specified subreddit.
    
    Args:
        subreddit_name (str): The name of the subreddit.
        limit (int): The number of posts to collect.
        
    Returns:
        pd.DataFrame: DataFrame with post titles and comments.
    """
    subreddit = reddit.subreddit(subreddit_name)
    posts_data = []

    # Collect posts from the subreddit
    for post in subreddit.hot(limit=limit):
        post_title = post.title
        post_id = post.id
        post_comments = []

        # Collect comments for each post
        post.comments.replace_more(limit=0)  # Remove "More comments" to get all comments
        for comment in post.comments.list():
            post_comments.append(comment.body)

        posts_data.append({"post_id": post_id, "title": post_title, "comments": post_comments})

    # Create a DataFrame
    df = pd.DataFrame(posts_data)
    return df

# Save collected data to CSV
df = collect_reddit_data("AskReddit", limit=100)
df.to_csv("data/raw/reddit_data.csv", index=False)
print("Data collected and saved to reddit_data.csv")
