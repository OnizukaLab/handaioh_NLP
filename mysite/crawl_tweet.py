
from requests_oauthlib import OAuth1Session
import json
from pprint import pprint
import sys
sys.path.append('handaioh_NLP/utils/')
from Spotlight_return import check_spotlight
import sqlite3
import threading
from datetime import datetime, timedelta
import sched
import time
import re


con = sqlite3.connect('./db.sqlite3')

def get_key():
    text_name = './handaioh_NLP/utils/.key'
    with open(text_name, 'r') as f:
        CK, CS, AT, AS = f.read().strip().split('\n')
    return CK, CS, AT, AS

CK, CS, AT, AS = get_key()
oauth = OAuth1Session(CK, CS, AT, AS)
url = "https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=YahooNewsTopics"

def get_title(text):
    title = re.search("【(.*?)】", text)
    if title is None:
        title_contentes = ''
    else:
        title_contentes = title.group(1)
    return title_contentes

def get_second_text(text):
    second_text = ''
    if len(text) > 1:
        second_text = '。'.join(text[1:])
    return second_text


def get_tweet_list(twitter):
    tweets_list = []

    for tweet in twitter:
        text = tweet['text'].split('\n\n')[-1]
        if 'RT' in text or 'http' in text:
            continue
        text = text.split('。')

        first_text = text[0] + '。'
        second_text = get_second_text(text)
        title = get_title(tweet['text'])

        tweets_list.append({
            'text':first_text,
            'second_text':second_text,
            'title':title,
            'date':tweet['created_at'],
            'favorite_count':int(tweet['favorite_count']),
            'retweet_count':int(tweet['retweet_count'])
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
        "count": "{}".format(number),
    }
    req = oauth.get(
        url,
        params=params
    )
    twitter = json.loads(req.text)
    # pprint(twitter['next_results'])
    tweets_list = get_tweet_list(twitter)
    quiz_cand_list = check_spotlight(tweets_list)
    add_quiz_data(quiz_cand_list)


def add_quiz_data(quiz_cand_list):
    con.execute("DELETE FROM handaioh_NLP_quiz")
    con.commit()
    for i in range(len(quiz_cand_list)):
        quiz_data = quiz_cand_list[i]
        text, date = quiz_data['text'], quiz_data['date']
        favorite_count, retweet_count = quiz_data['favorite_count'], quiz_data['retweet_count']
        second_text, title = quiz_data['second_text'], quiz_data['title']
        blank_cand = quiz_data['blank_cand']
        year, month, day, hour, minitue, sec = get_shape(date)

        con.execute("insert into handaioh_NLP_quiz (text, title, blank_cand, second_text, date_inf, favorite_count, retweet_count) values (?, ?, ?, ?, ?, ?, ?)"
                    , [text, title, blank_cand, second_text, datetime(year, month, day, hour, minitue, sec), favorite_count, retweet_count])
        con.commit()

# 指定時間に動作する関数
def specified_time():

    format_day = "%Y/%m/%d-"
    format_time = "%H:%M:%S"

    # 次回は4時間後にクロール
    next_process = datetime.now() + timedelta(hours=4)
    print('next crawling time is {}'.format(next_process))

    next_date = next_process.strftime(format_day)
    next_time = next_process.strftime(format_time)

    # スケジューラー
    scheduler = sched.scheduler(time.time, time.sleep)


    # 指定時間になったら事項
    run = datetime.strptime(next_date + next_time,  format_day + format_time)
    run = int(time.mktime(run.utctimetuple()))

    # 実行される関数を指定
    scheduler.enterabs(run, 1, get_tweet)
    scheduler.run()

    # 次回実行時間を設定
    t = threading.Thread(target=specified_time)
    t.start()


def main():
    get_tweet()
    t = threading.Thread(target=specified_time)
    t.start()

if __name__ == '__main__':
    main()