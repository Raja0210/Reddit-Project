import logging
import sys
import numpy as np
import pandas as pd
import praw
from praw import Reddit
from utils.constants import POST_FIELDS


def connect_reddit(CLIENT_ID, SECRET_KEY, AGENT) -> Reddit:
     try:
         reddit = praw.Reddit(client_id=CLIENT_ID,client_secret=SECRET_KEY,user_agent=AGENT)
         logging.info(f"Connect to Reddit:")
         return reddit
     except Exception as e:
         logging.error(f"Error in connect_reddit: {str(e)}")
         sys.exit(1)

def extract_posts(reddit_instance, subreddit, time_filter, limit=None):
    try:
        subreddit = reddit_instance.subreddit(subreddit)
        posts = subreddit.top(time_filter=time_filter,limit=limit)
        post_list = []

        for post in posts:
            post_dict = vars(post)
            post = {key:post_dict[key] for key in POST_FIELDS}
            post_list.append(post)

        return post_list
    except Exception as e:
        logging.error(f"Error in extract_posts: {str(e)}")
        sys.exit(1)

def transform(post_df):
    post_df['created_utc'] = pd.to_datetime(post_df['created_utc'], unit='s')
    post_df['over_18'] = np.where((post_df['over_18'] == True), True, False)
    post_df['author'] = post_df['author'].astype(str)
    edited_mode = post_df['edited'].mode()
    post_df['edited'] = np.where(post_df['edited'].isin([True, False]),
                                 post_df['edited'], edited_mode).astype(bool)
    post_df['num_comments'] = post_df['num_comments'].astype(int)
    post_df['score'] = post_df['score'].astype(int)
    post_df['title'] = post_df['title'].astype(str)

    return post_df

def load_data_to_csv(data: pd.DataFrame, path: str):
    data.to_csv(path, index=False)