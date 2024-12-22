import pandas as pd

def preprocess_reddit_data(input_file, output_file):
    """
    Preprocesses the Reddit data and flattens comments into one column.
    
    Args:
        input_file (str): Path to the raw Reddit data CSV.
        output_file (str): Path to save the cleaned data.
    """
    # Load the raw data
    df = pd.read_csv(input_file)

    # Flatten comments into a single column for analysis
    comments_data = []
    for _, row in df.iterrows():
        post_title = row["title"]
        post_id = row["post_id"]
        for comment in row["comments"]:
            comments_data.append({"post_id": post_id, "title": post_title, "comment": comment})

    # Create a new DataFrame for comments
    cleaned_df = pd.DataFrame(comments_data)
    cleaned_df.to_csv(output_file, index=False)
    print(f"Preprocessed data saved to {output_file}")

# Preprocess Reddit data
preprocess_reddit_data("data/raw/reddit_data.csv", "data/cleaned/reddit_comments.csv")
