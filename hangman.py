import random, tweepy, time
from datetime import datetime


def get_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time

def choose_lang(pLang):
    words = []
    lang = []
    if pLang == "de":
        lang = list(open('lang/de/de.txt', 'r'))
        words = list(open('lang/de/woerter.txt', 'r'))
    elif pLang == "en":
        lang = list(open('lang/en/en.txt', 'r'))
        words = list(open('lang/en/words.txt', 'r'))
    return lang, words

def random_word(pWords):
    return random.choice(pWords)

def check_for_occurence(pWord, pLetter):
    out_list = []
    for index, letter in enumerate(pWord):
        if letter == pLetter:
            out_list.append(index)
    return out_list

def build_word_string(pWord, pLetter, pOldOutput):
    if pOldOutput == 0:
        output = "*" * (len(pWord)-1)
    else:
        output = pOldOutput

    letter_in_list = check_for_occurence(pWord, pLetter)
    for pos in letter_in_list:
        output = output[:pos] + pLetter + output[pos+1:]

    return output

def get_replies(pAPI, pID):
    name = "@PlayHangmanBot"
    tweet_id = pID
    replies=[]
    for tweet in tweepy.Cursor(pAPI.search,q='to:'+name, result_type='recent', timeout=999999).items(1000):
        if hasattr(tweet, 'in_reply_to_status_id'):
            if (tweet.in_reply_to_status_id==tweet_id):
                replies.append(tweet)
    return replies

def get_highest_like_reply(pAPI, pID):
    replies = get_replies(pAPI, pID)
    id_likes = {}

    for tweet in replies:
        id_likes[tweet.id] = tweet.favorite_count

    if len(id_likes) == 0:
        ret_val = "warte"
    else:
        ret_val = max(id_likes, key=lambda key: id_likes[key])

    return ret_val



def wrong_guess(count): #Thanks to https://gist.github.com/SedaKunda/79e1d9ddc798aec3a366919f0c14a078
    if count == 1:
        print("Wrong guess, try again")
        print()
        print()
        print()
        print()
        print("___|___")
        print()
		
    if count == 2:
        print("Wrong guess, try again")
        print("   |")
        print("   |")
        print("   |")
        print("   |")
        print("   |")
        print("   |")
        print("   |")
        print("___|___")
    
    if count == 3:
        print("Wrong guess, try again")
        print("   ____________")
        print("   |")
        print("   |")
        print("   |")
        print("   |")
        print("   |")
        print("   |")
        print("   | ")
        print("___|___")
    
    if count == 4:
        print("Wrong guess, try again")
        print("   ____________")
        print("   |          _|_")
        print("   |         /   \\")
        print("   |        |     |")
        print("   |         \\_ _/")
        print("   |")
        print("   |")
        print("   |")
        print("___|___")
    
    if count == 5:
        print("Wrong guess, try again")
        print("   ____________")
        print("   |          _|_")
        print("   |         /   \\")
        print("   |        |     |")
        print("   |         \\_ _/")
        print("   |           |")
        print("   |           |")
        print("   |")
        print("___|___")
    
    if count == 6:
        print("Wrong guess, try again")
        print("   ____________")
        print("   |          _|_")
        print("   |         /   \\")
        print("   |        |     |")
        print("   |         \\_ _/")
        print("   |           |")
        print("   |           |")
        print("   |          / \\ ")
        print("___|___      /   \\")
    
    if count == 7:
        print("GAME OVER!")
        print("   ____________")
        print("   |          _|_")
        print("   |         /   \\")
        print("   |        |     |")
        print("   |         \\_ _/")
        print("   |          _|_")
        print("   |         / | \\")
        print("   |          / \\ ")
        print("___|___      /   \\")

def game(pLang, pWords, pAPI, game_counter):
    print(pLang[0])
    print(pLang[1])
    word = random_word(pWords).lower()
    print(word)

    while "//" in word:
        word = random_word().lower()

    end = False
    right_letters = []
    wrong_letters = []
    cache_out_str = 0

    temp_str = build_word_string(word, "Ä", cache_out_str)
    cache_out_str = temp_str
    out_str = "Welcome to Game #" + str(game_counter) + ".\nThis is your hint:\n" + temp_str + "\nThe current gametime is " + get_time()

    first_tweet = pAPI.update_status(out_str)
    tweet_id = first_tweet.id

    while end == False:
        time.sleep(60*10)
        letter_in = pAPI.get_status(get_highest_like_reply(pAPI, tweet_id)).text.strip(" @PlayHangmanBot ").lower()

        if not letter_in == "warte":

            if letter_in == word:
                status = "Game #" + str(game_counter) + " completed.\nThe word was: " + cache_out_str + "\nThe current gametime is " + get_time()
                pAPI.update_status(status)
                end = True
                return

            if letter_in in word:
                right_letters.append(letter_in)

                temp_str = build_word_string(word, letter_in, cache_out_str)
                cache_out_str = temp_str

                if cache_out_str in word:
                    status = "Game #" + str(game_counter) + " completed.\nThe word was: " + cache_out_str + "\nThe current gametime is " + get_time()
                    pAPI.update_status(status)
                    end = True
                    return

                status = "Game #" + str(game_counter) + "\nThe current hint is:\n" + cache_out_str + "\nThe current gametime is " + get_time()

            else:
                wrong_letters.append(letter_in)
                wrong_guess(len(wrong_letters))            
                if len(wrong_letters) == 7:
                    end = True
                    return    
                status = "Game #" + str(game_counter) + "\nYou have " + str(len(wrong_letters)) + " wrong tries left.\nThe current hint is:\n" + cache_out_str + "\nThe wrong letters are " + "".join(wrong_letters) + "\nThe current gametime is " + get_time()
            
            tweet_id = pAPI.update_status(status).id





