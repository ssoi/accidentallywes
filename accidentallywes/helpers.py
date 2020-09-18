import os
from datetime import datetime

import pandas as pd
import requests

from praw import Reddit


def _get_reddit_creds_from_env():
    app_name = os.environ["APP_NAME"]
    username = os.environ["USERNAME"]

    creds = {
        "username": username,
        "password": os.environ["PASSWORD"],
        "client_id": os.environ["CLIENTID"],
        "client_secret": os.environ["CLIENTSECRET"],
        "user_agent": f"/u/{username} {app_name}",
    }

    return creds


def get_reddit_instance():
    creds = _get_reddit_creds_from_env()
    reddit = Reddit(**creds)

    if reddit.user.me() != creds["username"]:
        raise ValueError("Reddit username does not match")

    return reddit


def get_latest_submissions(reddit_instance, subreddit_name, num_samples):
    subreddit = reddit_instance.subreddit(subreddit_name)

    latest_submissions = subreddit.new(limit=num_samples)

    return latest_submissions


def create_dataset(submissions):
    DATASETCOLS = ["score", "upvote_ratio", "title", "age", "comments", "image", "url"]

    dataset_rows = [
        _process_submission(submission)
        for submission in submissions
        if not submission.is_video
    ]

    dataset = pd.DataFrame(dataset_rows, columns=DATASETCOLS)

    return dataset


def _process_submission(submission):
    submission_age = datetime.utcnow() - datetime.fromtimestamp(submission.created_utc)

    result = (
        submission.score,
        submission.upvote_ratio,
        submission.title,
        submission_age.days,
        submission.num_comments,
        submission.url,
        submission.shortlink,
    )

    return results
