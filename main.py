import praw
import os
import string
import twitterbio
import re
import csv
import datetime

reddit = praw.Reddit('contextbot1')
subreddit = reddit.subreddit('ukpolitics')
twitbio = twitterbio
session = twitbio.auth()
threadlist = list()
newlist = list()
log = list()

log.append('------------------------')
log.append(' ')
log.append(datetime.datetime.now())
with open("replylist.csv", 'r+') as csvfile:
    reader = csv.reader(csvfile, delimiter =',')   
    for row in reader:
        threadlist.append(row)
log.append('posted list loaded')
for submission in subreddit.new(limit=10):   
    if "twitter.com/" not in submission.url or [submission.id] in threadlist:
        print(submission.id + ' - skipped')
        log.append(submission.id + ' - skipped')
        continue
    with open('boilerplate.txt', 'r') as file1:
        data = file1.read()
    log.append('New thread')
    sn = re.search(r".com/(\w+)", submission.url).group(1)
    if "twitter.com/twitter/statuses/" in submission.url:
        sn = twitbio.getUser(session, re.search(r".statuses/(\w+)", submission.url).group(1))       
    bio = twitbio.getBio(session, sn)
    snip = ""
    snip = re.search(r"[\w\.-]+@[\w\.-]+", bio)
    if snip :bio = bio.replace(snip.group(0), " - ")
    data = data.replace("%BIO%", bio)
    try:
        submission.reply(data)
        with open("replylist.csv", 'a') as csvfile:
            wr = csv.writer(csvfile, dialect='excel', delimiter = ',')
            wr.writerow([submission.id])
        log.append(data.encode('utf-8').strip())
        print(data)
    except praw.exceptions.APIException as exc:
        log.append(exc.message)
with open("redditlog.log", 'a') as logfile:
    wr = csv.writer(logfile)
    for row in log:
        wr.writerow([row])
    wr.writerow('')