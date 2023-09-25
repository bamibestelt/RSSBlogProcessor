import argparse
from typing import List

import feedparser

from rabbit import start_listen_request_queue

test_rss = "https://deviesdevelopment.github.io/blog/posts/index.xml"


def main():
    print("Coda decoder starting...")
    args = parse_arguments()
    if args.t:
        print("decoding from hard coded rss path")
        parse_blog_links(test_rss)
        return
    # load RabbitMQ connection
    # listen to message queue
    # use message as rss link
    # reply back with list of url
    start_listen_request_queue()


def parse_blog_links(rss_path: str) -> List[str]:
    feed = feedparser.parse(rss_path)
    print(f"feed entries: {len(feed.entries)}")
    links = []
    for entry in feed.entries:
        links.append(entry.link)
    print(f"total links: {len(links)}")
    return links


def parse_arguments():
    parser = argparse.ArgumentParser(description='Run Coda links decoder.')
    parser.add_argument("-t",
                        action='store_true',
                        help='Use this flag to use test links defined in the code.')

    parser.add_argument("-r",
                        action='store_true',
                        help='Use this flag to receive links from RabbitMQ message.')

    return parser.parse_args()


if __name__ == '__main__':
    main()
