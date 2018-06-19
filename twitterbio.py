import tweepy
import configparser
import locale

config = configparser.ConfigParser()
config.read('tweepy.ini')

def auth():
    auth = tweepy.OAuthHandler(config['auth']['oId'], config['auth']['oSecret'])
    auth.set_access_token(config['auth']['aId'], config['auth']['aSecret'])
    return tweepy.API(auth)

def getBio( session , screenname ):   
    usr = session.get_user(screenname)
    vtxt = " ^unverified"
    loc = ""
    if usr.location:
        loc = ' | Location: ' + usr.location
    if usr.verified:
        vtxt = " ^verified"    
    return '['+ usr.name +'](https://twitter.com/' + usr.screen_name + ')' + vtxt + ' | Reach: ' + format(usr.followers_count) + loc + '\n' + '\n' + 'Bio: ' + usr.description

def getUser( session, id ):
    tweet = session.get_status(id)
    username = tweet.user.screen_name
    return username

def format(n):
    locale.setlocale(locale.LC_ALL, '')
    return locale.format('%d', n, True)