import praw
import os
import string
import twitterbio
import re
import csv
import datetime

reddit = praw.Reddit('contextbot1')
subreddit = reddit.subreddit('ukpolitics+ContextualBot')
twitbio = twitterbio
session = twitbio.auth()
threadlist = list()
newlist = list()

for submission in subreddit.stream.submissions():
    skip = False
    if "twitter.com/" not in submission.url or [submission.id] in threadlist:
        print(submission.id + ' - skipped')
        continue
    for comment in submission.comments:
        if comment.author.name == "ContextualRobot":
            skip = True
            break
    if skip == True:
        continue
    with open('boilerplate.txt', 'r') as file1:
        data = file1.read()
    sn = re.search(r".com/(\w+)", submission.url).group(1)
    if "twitter.com/twitter/statuses/" in submission.url:
        sn = twitbio.getUser(session, re.search(r".statuses/(\w+)", submission.url).group(1))       
    bio = twitbio.getBio(session, sn)
    pattern = re.compile(r"[\w\.-]+@[\w\.-]+|[+0-9-\ ]{11,20}")
    for match in re.findall(pattern, bio):
        bio = bio.replace(match, " - ")
    data = data.replace("%BIO%", bio)
    try:
        submission.reply(data)
        print(data)
    except praw.exceptions.APIException as exc:
        print(exc.message)