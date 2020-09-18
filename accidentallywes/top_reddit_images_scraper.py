from .base_reddit_images_scraper import BaseRedditImagesScraper


class TopRedditImagesScraper(BaseRedditImagesScraper):
    def __init__(self, subreddit_name, top_k):
        super().__init__(self, subreddit_name)
        self.top_k = top_k

    def validate_submissions(self):
             

