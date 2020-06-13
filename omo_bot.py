from keys import consumer_key, consumer_secret, key, secret
from email_info import email, password

import random
import smtplib
import tweepy
import time

FILE_NAME = 'last_seen.txt'

REPLIES = [
    "Don't be razz please", 
    "Guy behave", 
]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)

api = tweepy.API(auth)

def follow_back():
    followers = api.followers_ids()
    for follower in followers:
        api.create_friendship(follower)
    return

def reply_omo_tweets():
    time_line_tweets = api.home_timeline(read_last_seen(FILE_NAME))
    for tweet in time_line_tweets:
        if 'omo' in tweet.text.lower().split() and tweet.text[:2] != 'RT':
            api.update_status('@' + tweet.user.screen_name + ' ' + REPLIES[random.randint(0,1)], tweet.id)
            store_last_seen(FILE_NAME, tweet.id)
    return

def read_last_seen(FILE_NAME):
    file_read = open(FILE_NAME, 'r')
    last_seen_id = int(file_read.read().strip())
    file_read.close()
    return last_seen_id

def store_last_seen(FILE_NAME, last_seen_id):
    file_write = open(FILE_NAME, 'w')
    file_write.write(str(last_seen_id))
    file_write.close()
    return

def runBot():
    while True:
        follow_back()
        reply_omo_tweets()
        time.sleep(60)

try:
    runBot()

except Exception as e:
    subject = "Omo-Bot is down"
    text = e
    message = 'Subject: {}\n\n{}'.format(subject, text)

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()
