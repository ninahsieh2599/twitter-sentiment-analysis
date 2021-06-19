from nltk.twitter import Twitter, Query, Streamer, TweetViewer, TweetWriter, credsfromfile
from nltk.twitter.common import json2csv
from nltk.corpus import twitter_samples
import pandas as pd
import os
from pathlib import Path
from nltk.sentiment.vader import  SentimentIntensityAnalyzer
from wordcloud import WordCloud
import re
from pyecharts.charts import Bar
from pyecharts import options as opts

def getTweet(username):
    oauth = credsfromfile()  # 會搜尋 credentials.txt(預設)

    count = 20  # 設定拿取 tweets 資料則數
    #username = 'CNN'

    client = Query(**oauth)  # 歷史資料
    client.register(TweetWriter())  # 寫入
    client.user_tweets(username, count)  # 拿取 tweets 資料(n則)

    '''
    使用 json2csv 存取 tweets 資料 (text欄位)
    input_file 的 abspath 需參考上述 Query 寫入資料的路徑做修改
    '''

    lists = os.listdir('C:/Users/ninab/twitter-files')
    lists.sort(key=lambda fn: os.path.getmtime('C:/Users/ninab/twitter-files' + "\\" + fn))
    #print('C:/Users/ninab/twitter-files/' + lists[-1])

    input_file = twitter_samples.abspath('C:/Users/ninab/twitter-files/' + lists[-1])
    with open(input_file) as fp:
        json2csv(fp, 'tweets_text.csv', ['text'])

    return lists

def dataprocess():
    tweetList = []
    #讀取
    data = pd.read_csv('tweets_text.csv')
    for line in data.text:
        #print('CNN tweets content: ')
        #print(line)
        line = re.sub(r'http\S+', '', line)
        tweetList.append(line)
        #results = translator.translate(line, dest='zh-tw')
        #print('翻譯: ', results.text)
    #print(tweetList)
    return tweetList

def wordCloud_grah(tweetList):
    text = " ".join(tweetList)
    cloud = WordCloud().generate(text)
    cloud.to_file('output.png')

def bar_graph(tweetList):
    vader = SentimentIntensityAnalyzer()

    data1 = []
    data2 = []
    data3 = []
    column = []
    for tweet in tweetList:
        column.append("推文連結")
        score = vader.polarity_scores(tweet)
        #print(score)
        data1.append(score['neg'])
        data2.append(score['neu'])
        data3.append(score['pos'])

    bar = Bar()
    bar.add_xaxis(column)
    bar.add_yaxis("負面", data1)
    bar.add_yaxis("中性", data2)
    bar.add_yaxis("正面", data3)
    bar.set_global_opts(title_opts=opts.TitleOpts(title="柱狀圖", subtitle="情緒變化趨勢"))
    bar.render("output.html")

def removeOldData(lists):
    for i in range(0, len(lists)-1, 1):
        filePath = Path('C:/Users/ninab/twitter-files/' + lists[i])
        try:
            filePath.unlink()
        except OSError as e:
            print(f"Error:{ e.strerror}")


if __name__ == '__main__':
    result = []
    jsonData = []

    username = input("輸入欲搜尋的twitter ID(不含@): (@twitter_ID)")

    jsonData = getTweet(username)
    result = dataprocess()
    wordCloud_grah(result)
    bar_graph(result)
    removeOldData(jsonData)
