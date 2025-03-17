import logging
from etls.reddit_etl import connect_reddit, extract_posts, transform, load_data_to_csv
from utils.constants import SECRET, CLIENT_ID, OUTPUT_PATH
import pandas as pd


def reddit_extraction(file_name,subreddit,time_filter='day',limit='None'):
    try:
        instance = connect_reddit(CLIENT_ID,SECRET,'Raja Agent')
        posts = extract_posts(instance,subreddit,time_filter,limit)
        post_df = pd.DataFrame(posts)
        post_df = transform(post_df)
        file_path = f'{OUTPUT_PATH}/{file_name}.csv'
        load_data_to_csv(post_df,file_path)

        return file_path
    except Exception as e:
        logging.error(f"Error in reddit_extraction: {str(e)}")
        raise