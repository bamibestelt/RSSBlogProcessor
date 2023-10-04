import os
from dotenv import load_dotenv

load_dotenv()

RABBIT_HOST = os.environ.get('RABBIT_HOST')
REQUEST_QUEUE = os.environ.get('BLOG_REQUEST_QUEUE')
BLOG_LINKS_QUEUE = os.environ.get('BLOG_REPLY_QUEUE')
TEST_RSS = os.environ.get('TEST_RSS')
