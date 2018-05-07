import tweepy
import configparser

config = configparser.ConfigParser()
config.read('tweepy.ini')

def auth():
    auth = tweepy.OAuthHandler(config['auth']['oId'], config['auth']['oSecret'])
    auth.set_access_token(config['auth']['aId'], config['auth']['aSecret'])
    return tweepy.API(auth)

def getBio( session , screenname ):   
    usr = session.get_user(screenname)
    vtxt = " ^unverified"
    if usr.verified:
        vtxt = " ^verified"    
    return 'Twitter Name: ['+ usr.name +'](https://twitter.com/' + usr.screen_name + ')' + vtxt + ' Reach: ' + str(usr.followers_count) + '\n' + '\n' + 'Bio: ' + usr.description

def getUser( session, id ):
    tweet = session.get_status(id)
    username = tweet.user.screen_name
    return username