
from requests_oauthlib import OAuth1Session
import json
from pprint import pprint
from Spotlight_return import check_spotlight
import sqlite3
import datetime

con = sqlite3.connect('../../db.sqlite3')

def get_key():
    text_name = '.key'
    with open(text_name, 'r') as f:
        CK, CS, AT, AS = f.read().strip().split('\n')
    return CK, CS, AT, AS

CK, CS, AT, AS = get_key()
oauth = OAuth1Session(CK, CS, AT, AS)
url = "https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=YahooNewsTopics"


def get_tweet_list(twitter):
    tweets_list = []

    for tweet in twitter:
        text = tweet['text'].split('\n\n')[-1].split('\n')[0]
        text = text.split('。')[0] + '。'
        if 'RT' in text or 'http' in text:
            continue
        tweets_list.append({
            'text':text,
            'date':tweet['created_at']
        })
    return tweets_list

def get_shape(date):
    month_dict = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6
        , 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
    date = date.split()
    hour, minitue, sec = list(map(int, date[3].split(':')))
    year, month, day = int(date[5]), month_dict[date[1]], int(date[2])
    return year, month, day, hour, minitue, sec


def get_tweet():
    number = 200
    params = {
        "count": "{}".format(number)
    }
    req = oauth.get(
        url,
        params=params
    )
    twitter = json.loads(req.text)
    tweets_list = get_tweet_list(twitter)
    quiz_cand_list = check_spotlight(tweets_list)
    add_quiz_data(quiz_cand_list)

def add_quiz_data(quiz_cand_list):
    con.execute("DELETE FROM handaioh_NLP_quiz")
    con.commit()
    for i in range(len(quiz_cand_list)):
        quiz_data = quiz_cand_list[i]
        text, date = quiz_data['text'], quiz_data['date']
        year, month, day, hour, minitue, sec = get_shape(date)

        con.execute("insert into handaioh_NLP_quiz (text, date_inf) values (?, ?)", [text, datetime.datetime(year, month, day, hour, minitue, sec)])
        con.commit()



if __name__ == '__main__':
    get_tweet()