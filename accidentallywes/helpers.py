import os
from datetime import datetime

import pandas as pd
import requests
from praw import Reddit


def _get_reddit_creds_from_env():
    app_name = os.environ["APPNAME"]
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
        if not submission.is_video and _is_jpeg(submission.url)
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

    return result


def _is_jpeg(url):
    is_jpeg = url[-4:].lower() in (".jpg", ".jpeg")

    return is_jpeg


def download_image(image_url, image_dir):
    print("{} {}".format(image_url, _is_jpeg(image_url)))
    image_request = requests.get(image_url)

    filepath = _get_filepath_from_url(image_url, image_dir)
    with open(filepath, "wb") as image_file:
        image_file.write(image_request.content)

    return


def _get_filepath_from_url(url, image_dir):
    _, filename = os.path.split(url)
    filepath = os.path.join(image_dir, filename)

    return filepath


def write_dataset(dataset, data_dir):
    timestamp = str(int(datetime.utcnow().timestamp()))
    filename = f"{timestamp}.csv"
    filepath = os.path.join(data_dir, filename)

    dataset.to_csv(filepath)

    return
