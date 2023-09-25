import json
import os
from typing import List

import pika
from dotenv import load_dotenv

import feedparser

load_dotenv()

RABBIT_HOST = os.environ.get('RABBIT_HOST')
REQUEST_QUEUE = os.environ.get('BLOG_REQUEST_QUEUE')
BLOG_LINKS_QUEUE = os.environ.get('BLOG_REPLY_QUEUE')


def start_listen_request_queue():
    # need to add broker credentials
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=REQUEST_QUEUE)
    channel.basic_consume(queue=REQUEST_QUEUE, on_message_callback=listen_to_queue, auto_ack=True)
    print('Listening to request. To exit press CTRL+C')
    channel.start_consuming()


def listen_to_queue(ch, method, properties, body):
    print(f"Received RSS to process: {body}")
    bytes_to_string = body.decode('utf-8')
    links = parse_blog_links(bytes_to_string)
    send_blog_links_queue(links)


def send_blog_links_queue(links: List[str]):
    json_list = json.dumps(links)
    # need to add broker credentials
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=BLOG_LINKS_QUEUE)
    channel.basic_publish(exchange='', routing_key=BLOG_LINKS_QUEUE, body=json_list)
    print(f"Blog links size {len(links)} sent!")
    connection.close()


def parse_blog_links(rss_path: str) -> List[str]:
    feed = feedparser.parse(rss_path)
    print(f"feed entries: {len(feed.entries)}")
    links = []
    for entry in feed.entries:
        links.append(entry.link)
    print(f"total links: {len(links)}")
    return links
