import snscrape.modules.twitter as sntwitter

import yaml
from random import randint
import re
import emoji
import time
import traceback
from datetime import datetime, timedelta, date

class Data:
    with open("configuration.yml", "r") as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    word_to_search = data["words_to_search"]
    accounts_to_tag = data["accounts_to_tag"]
    accounts_to_blacklist = data["accounts_to_blacklist"]
    sentence_for_tag = data["sentence_for_tag"]
    hashtag_to_blacklist = data["hashtag_to_blacklist"]
    giveaway_to_blacklist = data["giveaway_to_blacklist"]
    max_giveaway = data["max_giveaway"]
    minimum_like = data["minimum_like"]
    minimum_rt = data["minimum_rt"]
    maximum_day = data["maximum_day"]
    nb_of_giveaway = data["nb_of_giveaway"]
    sentence_for_random_comment = data["sentence_for_random_comment"]
    tweet_lang = data["tweet_lang"]
    add_sentence_to_tag = data["add_sentence_to_tag"]
    word_list_to_check_for_special_comment = data["word_list_to_check_for_special_comment"]
    word_list_to_check_for_comment = data["word_list_to_check_for_comment"]
    short_word_list_to_check_for_comment = data["short_word_list_to_check_for_comment"]
    word_list_to_check_for_tag = data["word_list_to_check_for_tag"]
    one_poeple_list = data["one_poeple_list"]
    two_poeple_list = data["two_poeple_list"]
    three_or_more_poeple_list = data["three_or_more_poeple_list"]

def is_date_older_than_a_number_of_day(date_str):
    d = Data()
    date_str = str(date_str)
    today = datetime.now().date()
    date = datetime.strptime(date_str, '%Y-%m-%d').date()
    delta = today - date
    if delta.days > d.maximum_day:
        return True
    else:
        return False

def remove_non_alphanumeric(string):
    s = string.split("\n")
    return s[0]

def write_into_file(path, x):
    return
    with open(path, "ab") as f:
        f.write(str(x).encode("utf-8"))

def reset_file(path):  
    f = open(path, "w")
    f.write("")    
    f.close            

def print_file_info(path):
    with open(path, "r" ,encoding='utf8', errors='ignore') as f:
        content = f.read()
    return content

def remove_emojie(text):
    return emoji.replace_emoji(text, replace='')
    #return emoji.get_emoji_regexp().sub(r'',text)

def delete_hashtag_we_dont_want(l):
    d = Data()
    new_l = []

    for elem in l:
        if elem.lower().replace("#","") not in d.hashtag_to_blacklist:
            new_l.append(elem + " ")
    
    return (" ".join(new_l))


def check_for_forbidden_word(sentence):
    d = Data()
    forbidden = d.giveaway_to_blacklist
    for elem in forbidden:
        if elem.lower() in sentence.lower():
            return True
    return False

def list_of_account_to_follow(maker_of_the_tweet,sentence):
    account_to_follow = [maker_of_the_tweet.replace("@","")]
    s = sentence.split(" ")
    for word in s:
        try:
            if word[0] == "@" and word.replace("@","") != maker_of_the_tweet.replace("@",""):
                account_to_follow.append(remove_non_alphanumeric(word.replace("@","")))
        except:
            pass
    account_to_follow = list(dict.fromkeys(account_to_follow))
    return (" ".join(account_to_follow))

def get_the_right_word(sentence):
    new_sentence = ""
    
    guillemet_counter = 0
    for i in range(len(sentence)):
        if sentence[i] == '"' or sentence[i] == '“' or sentence[i] == '«' or sentence[i] == "»":
            guillemet_counter = guillemet_counter + 1
        if guillemet_counter >= 2:
            break
        if guillemet_counter == 1 or sentence[i] == '"' or sentence[i] == '“' or sentence[i] == "«" or sentence[i] == "»":
            new_sentence = new_sentence + sentence[i]
    
    return (new_sentence.replace('"',"").replace("“","").replace("«","").replace("»",""))

def what_to_comment(sentences):
    s = sentences.split("\n")
    d = Data()
    for word in d.word_list_to_check_for_special_comment:
        for sentence in s:
            if word in sentence.lower():
                comment = sentence.split(word)
                if len(comment) == 1:
                    c = comment[0]
                else:
                    c = comment[1]
                if '"' in c or '“' in c:
                    c = get_the_right_word(c)
                return(c.replace('"',"").replace("“","").replace("«","").replace("»",""))
                
    return ("")

def get_a_better_list(l):
    account_you_follow_from_file = print_file_info("account.txt").split("\n")
    new_l = []
    account = []
    for i in range(len(l)):
        line_f = l[i].split(" ")
        for j in range(len(line_f)):
            new_l.append(line_f[j])
            if line_f[j].replace(",","").replace(";","") not in account_you_follow_from_file and line_f[j].replace(",","").replace(";","") not in account:
                account.append(line_f[j].replace(",","").replace(";",""))
                write_into_file("account.txt",line_f[j].replace(",","").replace(";","")+"\n")
    return (new_l)

def check_if_we_need_to_comment(text):
    d = Data()

    for elem in d.word_list_to_check_for_comment:
        if elem.lower() in text.lower():
            return True
    
    for word_to_check in d.short_word_list_to_check_for_comment:
        for word in text.split():
            if word.lower().startswith(word_to_check.lower()) and len(word) <= 6:
                return True

    text = text.lower()
    return False


def check_if_we_need_to_tag(text):
    d = Data()
    for elem in d.word_list_to_check_for_tag:
        if elem.lower() in text.lower():
            return True
    return False

def delete_url(s):
    s_ = s.split(" ")
    n_s = []
    for i in range(len(s_)):
        if "https" not in s_[i]:
            n_s.append(s_[i])
    n =  " ".join(n_s)
    n = n.strip()

    return(n)

def search_tweet_for_rt(text,nb):
    tweet_url = []
    MAX = 0
    try:
        text = text + ' lang:fr'
        mode_param = sntwitter.TwitterSearchScraperMode.TOP
        for i,tweet in enumerate((sntwitter.TwitterSearchScraper(text, mode = mode_param).get_items())):
            url =  f"https://twitter.com/user/status/{tweet.id}"
            tweet_url.append(url)
            MAX+=1
            if MAX >= nb:
                break
        return(tweet_url)
    except:
        return(tweet_url)


def who_many_people_to_tag(text):
    d = Data()

    for one in d.one_poeple_list:
        if one.lower() in text.lower():
            return(d.accounts_to_tag[0])
    
    for two in d.two_poeple_list:
        if two.lower() in text.lower():
            return(d.accounts_to_tag[0]+" "+d.accounts_to_tag[1])
    
    return(" ".join(d.accounts_to_tag))
    
def check_if_we_need_to_tag_two(text):
    d = Data()
    
    for one in d.one_poeple_list:
        if one.lower() in text.lower():
            return True
    
    for two in d.two_poeple_list:
        if two.lower() in text.lower():
            return True
    
    for other in d.three_or_more_poeple_list:
        if other.lower() in text.lower():
            return True
    
    return False    

def check_blacklist(account):
    d = Data
    for backlist_account in d.accounts_to_blacklist:
        if account.lower() == backlist_account.lower().replace("@",""):
            return(True)
    return (False)


def search_giveaway():
    try:
        d = Data()
        reset_file("recent_url.txt")
        tweets_need_to_comment_or_not = []
        tweets_text = []
        tweets_id = []
        tweets_url = []
        tweets_full_comment = []
        tweets_account_to_follow = []
        nb_of_giveaway_found = 0
        char = '#'
        full_phrase = ""
        doublon = 0
        url_from_file = print_file_info("url.txt").split("\n")
        print_data = False
        date_ = ""
        date_format = "%Y-%m-%d"
        for search_word in d.word_to_search:
            text = search_word + ' lang:'+d.tweet_lang
            if d.tweet_lang == "any":
                text = search_word 
            for i,tweet in enumerate(sntwitter.TwitterSearchScraper(text).get_items()):
                date_ = str(tweet.date)
                date_ = date_[0:10]
                year, month, day = map(int, date_.split("-"))
                ddate = date(year, month, day)
                url =  f"https://twitter.com/user/status/{tweet.id}"
                if tweet.id not in tweets_id and tweet.likeCount >= d.minimum_like and check_for_forbidden_word(tweet.rawContent) == False and check_blacklist(tweet.user.username) == False and url not in url_from_file and is_date_older_than_a_number_of_day(ddate) == False and tweet.retweetCount >= d.minimum_rt and nb_of_giveaway_found < d.nb_of_giveaway:
                    words = tweet.rawContent.split()
                    result = [word for word in words if word.startswith(char)]
                    hashtag = delete_hashtag_we_dont_want(result)
                    if check_if_we_need_to_tag(tweet.rawContent) == True:
                        if check_if_we_need_to_comment(tweet.rawContent) == True:
                            full_phrase = delete_url(what_to_comment(tweet.rawContent)) + who_many_people_to_tag(tweet.rawContent) + " " + hashtag
                            if d.add_sentence_to_tag == True:
                                full_phrase = d.sentence_for_tag[randint(0,len(d.sentence_for_tag) - 1)] + " " + delete_url(what_to_comment(tweet.rawContent)) + who_many_people_to_tag(tweet.rawContent) + " " + hashtag
                        else:
                            full_phrase = delete_url(what_to_comment(tweet.rawContent)) + who_many_people_to_tag(tweet.rawContent) + " "
                            if d.add_sentence_to_tag == True:
                                full_phrase = d.sentence_for_tag[randint(0,len(d.sentence_for_tag) - 1)] + " " + delete_url(what_to_comment(tweet.rawContent)) + who_many_people_to_tag(tweet.rawContent) + " "
                    else:
                        full_phrase = d.sentence_for_random_comment[randint(0,len(d.sentence_for_random_comment) - 1)] + " " + delete_url(what_to_comment(tweet.rawContent)) + " " + hashtag
                    tweets_id.append(tweet.id)
                    tweets_text.append(tweet.rawContent)
                    tweets_url.append(url)
                    if check_if_we_need_to_tag(tweet.rawContent) == True or check_if_we_need_to_tag_two(tweet.rawContent) == True:
                        tweets_need_to_comment_or_not.append(True)
                    else:
                        tweets_need_to_comment_or_not.append(check_if_we_need_to_comment(tweet.rawContent))
                    tweets_account_to_follow.append(list_of_account_to_follow(tweet.user.username ,tweet.rawContent))
                    tweets_full_comment.append(remove_emojie(full_phrase))
                    write_into_file("url.txt",url+"\n")
                    write_into_file("recent_url.txt",url+"\n")
                    nb_of_giveaway_found+=1
                else:
                    doublon +=1
                if nb_of_giveaway_found>=d.nb_of_giveaway:
                    break
        tweets_account_to_follow = get_a_better_list(tweets_account_to_follow)
        if print_data == True:
            print(tweets_text)
            print(tweets_url)
            print(tweets_full_comment)
            print(tweets_account_to_follow)
            print("Nb of doublon " + str(doublon))
        print("Number of giveaway found = " + str(nb_of_giveaway_found))
        print("Ending giveaway search")
        return (tweets_text,tweets_url,tweets_full_comment,tweets_account_to_follow,tweets_need_to_comment_or_not)
    except Exception as e:
        print("SNSCRAPE NEED TO RESTART WAIT 10 MINUTES")
        print("Error " + str(e))
        print(traceback.format_exc())
        time.sleep(600)
        search_giveaway()

def giweaway_from_url_file(tweets_text,account_list):
    try:
        d = Data()
        tweets_need_to_comment_or_not = []
        tweets_full_comment = []
        tweets_account_to_follow = []
        nb_of_giveaway_found = 0
        char = '#'
        full_phrase = ""
        url_from_file = print_file_info("url.txt").split("\n")
        print_data = False
        for t in tweets_text:
            words = t.split(" ")
            result = [word for word in words if word.startswith(char)]
            hashtag = delete_hashtag_we_dont_want(result)
            if check_if_we_need_to_tag(t) == True:
                if check_if_we_need_to_comment(t) == True:
                    full_phrase = delete_url(what_to_comment(t)) + who_many_people_to_tag(t) + " " + hashtag
                    if d.add_sentence_to_tag == True:
                        full_phrase = d.sentence_for_tag[randint(0,len(d.sentence_for_tag) - 1)] + " " + delete_url(what_to_comment(t)) + who_many_people_to_tag(t) + " " + hashtag
                else:
                    full_phrase = delete_url(what_to_comment(t)) + who_many_people_to_tag(t) + " "
                    if d.add_sentence_to_tag == True:
                        full_phrase = d.sentence_for_tag[randint(0,len(d.sentence_for_tag) - 1)] + " " + delete_url(what_to_comment(t)) + who_many_people_to_tag(t) + " "
            else:
                full_phrase = d.sentence_for_random_comment[randint(0,len(d.sentence_for_random_comment) - 1)] + " " + delete_url(what_to_comment(t)) + " " + hashtag
            
            if check_if_we_need_to_tag(t) == True or check_if_we_need_to_tag_two(t) == True:
                tweets_need_to_comment_or_not.append(True)
            else:
                tweets_need_to_comment_or_not.append(check_if_we_need_to_comment(t))
            tweets_full_comment.append(remove_emojie(full_phrase))
            tweets_account_to_follow.append(list_of_account_to_follow("" ,t))


        for a in account_list:
            if a not in tweets_account_to_follow and a != "f":
                tweets_account_to_follow.append(a)
        if print_data == True:
            print(tweets_full_comment)
            print(tweets_need_to_comment_or_not)
        print("Ending giveaway from url file")
        print(tweets_need_to_comment_or_not)
        print("flopipipipipa")
        return (tweets_need_to_comment_or_not,tweets_full_comment,tweets_account_to_follow)
    except Exception as e:
        print("YOLO YOLO BANG BANG")
        print("Error " + str(e))
        time.sleep(600)
        giweaway_from_url_file(tweets_text)