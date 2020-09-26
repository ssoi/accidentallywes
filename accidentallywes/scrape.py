import os

from helpers import (create_dataset, download_image, get_latest_submissions,
                     get_reddit_instance, write_dataset)

SUBREDDITNAME = "AccidentalWesAnderson"
NUMSAMPLES = 1000

CURRDIR = os.path.dirname(os.path.abspath(__file__))
DATADIR = os.path.join(CURRDIR, "..", "data")
IMAGEDIR = os.path.join(DATADIR, "images")


def main():
    reddit_instance = get_reddit_instance()

    latest_submissions = get_latest_submissions(
        reddit_instance=reddit_instance,
        subreddit_name=SUBREDDITNAME,
        num_samples=NUMSAMPLES,
    )

    dataset = create_dataset(submissions=latest_submissions)

    for _, submission in dataset.iterrows():
        download_image(image_url=submission["image"], image_dir=IMAGEDIR)

    write_dataset(dataset=dataset, data_dir=DATADIR)


if __name__ == "__main__":
    main()
