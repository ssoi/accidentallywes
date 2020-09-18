import os

import boto3
import requests

from abc import ABC
from praw import Reddit

class BaseRedditImagesScraper(ABC):
    def __init__(self, subreddit_name):
        self._reddit = self._get_reddit_instance()
        self._s3 = boto3.resource('s3')

        self.subreddit_name = subreddit_name

    def scrape(self):
        submissions = self.get_submissions()
          

    @classmethod    
    def get_submissions(self):
        pass

    @classmethod    
    def validate_submission(self):
        pass

    @staticmethod
    def _get_reddit_creds_from_env():
        creds = {
            'username': os.environ['USERNAME']
            'password': os.environ['PASSWORD']
            'client_id': os.environ['CLIENTID']
            'client_secret': os.environ['CLIENTSECRET']
        }

        return creds

    @staticmethod
    def _get_reddit_instance():
        creds = self._get_reddit_creds_from_env()
        reddit = Reddit(**creds)

        if reddit.user.me() != creds['username']:
            raise ValueError('Reddit username does not match')
        
        return reddit

