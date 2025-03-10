import pandas as pd
import os
from datetime import timedelta

def frequency_categorical_recommender(
    user_id,
    n_recommendations=5,
    behaviors_path="/content/drive/MyDrive/BigData/processed_behaviours_train.parquet",
    news_path="/content/drive/MyDrive/BigData/processed_news_train.parquet",
    use_recency=True,
    recency_weeks=2
):
    """
    For a given user, loads behaviors & news data from the specified parquet files in Google Drive,
    determines the user's most frequently read category, and returns top n articles in that category
    that the user hasn't read yet.

    Parameters:
      user_id (str): The user identifier from the behaviors DataFrame.
      n_recommendations (int): Number of articles to recommend.
      behaviors_path (str): Path to the behaviors .parquet in Google Drive.
      news_path (str): Path to the news .parquet in Google Drive.
      use_recency (bool): Whether to limit behavior data to last `recency_weeks`.
      recency_weeks (int): Number of weeks to consider if use_recency=True.

    Returns:
      (recommendations_df, explanation_str)
        - recommendations_df: DataFrame with columns [news_id, category, title, url].
        - explanation_str: Explanation text.
        - If no recommendations found, returns (None, explanation).
    """

    # Attempt to auto-mount Drive if in Colab
    try:
        import google.colab
        from google.colab import drive
        if not os.path.exists("/content/drive"):
            drive.mount("/content/drive", force_remount=True)
    except ImportError:
        pass  # Not in Colab, skip

    # 1) Load the parquet files
    df_behav = pd.read_parquet(behaviors_path)
    df_news = pd.read_parquet(news_path)

    # 2) Filter behaviors for the specified user
    user_behav = df_behav[df_behav["user_id"] == user_id]
    if user_behav.empty:
        return None, f"No behavior records found for user {user_id}"

    # 3) Optional recency filtering (last 2 weeks by default)
    user_behav["time"] = pd.to_datetime(user_behav["time"], errors="coerce")
    latest_time = user_behav["time"].max()
    if pd.isnull(latest_time):
        recent_behav = user_behav
    else:
        threshold = latest_time - timedelta(weeks=recency_weeks)
        recent_behav = user_behav if not use_recency else user_behav[user_behav["time"] >= threshold]

    # 4) Parse user's reading history (space-separated news IDs)
    history_series = recent_behav["history"].dropna().astype(str)
    user_history_list = " ".join(history_series).split()
    if not user_history_list:
        return None, f"User {user_id} has no reading history in the last {recency_weeks} weeks."

    # 5) Determine top category
    # Map from news_id -> category
    news_cat_map = df_news.set_index("news_id")["category"]
    user_categories = pd.Series(user_history_list).map(news_cat_map).dropna()
    if user_categories.empty:
        return None, "No category information found for the user's history."

    top_category = user_categories.value_counts().idxmax()

    # 6) Get candidate articles in that category, excluding read IDs
    read_ids = set(user_history_list)
    candidates = df_news[df_news["category"] == top_category].copy()
    candidates = candidates[~candidates["news_id"].isin(read_ids)]

    # Return first n_recommendations
    recommendations = candidates.head(n_recommendations)
    if recommendations.empty:
        explanation = (
            f"Based on your history, you appear to favor **{top_category}** news, "
            "but no unseen articles remain in that category."
        )
        return None, explanation

    explanation = (
        f"Based on your reading history, you appear to favor **{top_category}** news. "
        f"Here are {len(recommendations)} articles you haven't read yet:"
    )
    return recommendations[["news_id", "category", "title", "url"]], explanation

# Example usage:
if __name__ == "__main__":
    example_user = "U13740"
    recs, expl = frequency_categorical_recommender(example_user, 5)
    if recs is not None:
        print(expl)
        print(recs)
    else:
        print(expl)
