from helpers import (create_dataset, download_images, get_latest_submissions,
                     get_reddit_instance, write_dataset)

SUBREDDITNAME = "AccidentalWesAnderson"
NUMSAMPLES = 1000


def main():
    reddit_instance = get_reddit_instance()

    latest_submissions = get_latest_submissions(
        reddit_instance=reddit_instance,
        subreddit_name=SUBREDDITNAME,
        num_samples=NUMSAMPLES,
    )

    dataset, urls = create_dataset(submissions=latest_submissions)

    download_images(urls=urls, image_dir=IMAGEDIR)
    write_dataset(dataset=dataset, data_dir=DATADIR)
