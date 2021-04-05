import tweepy
from TwitterAuth import start_auth, CONSUMER_SECRET, CONSUMER_TOKEN
import hangman
    

if __name__ == "__main__":

    cred = list(open("cred.txt", "r"))
    
    access_token = ""
    access_secret = ""
    if len(cred) <= 0:
        access_token, access_secret = start_auth()    
    else:
        access_token = cred[0].strip("\n")
        access_secret = cred [1].strip("\n")
    auth = tweepy.OAuthHandler(CONSUMER_TOKEN, CONSUMER_SECRET)
    auth.set_access_token(access_token, access_secret)

    api = tweepy.API(auth)

    game_counter = 1
    lang, words = hangman.choose_lang("en")
    while True:
        hangman.game(lang, words, api, game_counter)
        game_counter = game_counter + 1