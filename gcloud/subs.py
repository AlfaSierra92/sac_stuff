from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
import sys
import re

# LANCIARE COME python3 subs.py hashtag
# NON USARE IL CARATTERE "#"
# RICORDARSI DI GENERARE IL FILE credentials.json

nome_script, primo = sys.argv

subscriber = pubsub_v1.SubscriberClient()
# The `subscription_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/subscriptions/{subscription_id}`
subscription_path = subscriber.subscription_path('travel2-405610', 'subs')


def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    # print(f"Received {message}.")
    hashtags = re.findall('(#\w+)', message.data.decode("utf-8"), re.DOTALL)
    for h in hashtags:
        if h == "#"+primo:
            print(f"{message.data}")
    message.ack()


streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}..\n")

# Wrap subscriber in a 'with' block to automatically call close() when done.
with subscriber:
    try:
        # When `timeout` is not set, result() will block indefinitely,
        # unless an exception is encountered first.
        streaming_pull_future.result()
    except TimeoutError:
        streaming_pull_future.cancel()  # Trigger the shutdown.
        streaming_pull_future.result()  # Block until the shutdown is complete.