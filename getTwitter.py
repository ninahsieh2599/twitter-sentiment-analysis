from nltk.twitter import Twitter, Query, Streamer, TweetViewer, TweetWriter, credsfromfile
from nltk.twitter.common import json2csv
from nltk.corpus import twitter_samples
import pandas as pd
import os
from pathlib import Path
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from wordcloud import WordCloud
import re
from pyecharts.charts import Bar
from pyecharts import options as opts


def getTweet(username):
    oauth = credsfromfile()  # 會搜尋 credentials.txt(預設)

    count = 20  # 設定拿取 tweets 資料則數
    # username = 'CNN'

    client = Query(**oauth)  # 歷史資料
    client.register(TweetWriter())  # 寫入
    client.user_tweets(username, count)  # 拿取 tweets 資料(count則)

    '''
    使用 json2csv 存取 tweets 資料 (text欄位)
    input_file 的 abspath 需參考寫入資料的路徑做修改
    '''

    lists = os.listdir('C:/Users/ninab/twitter-files')  # json檔路徑
    lists.sort(key=lambda fn: os.path.getmtime('C:/Users/ninab/twitter-files' + "\\" + fn))     # 檔案依新增時間排序

    input_file = twitter_samples.abspath('C:/Users/ninab/twitter-files/' + lists[-1])   # 取最新新增的檔案
    with open(input_file) as fp:
        json2csv(fp, 'tweets_text.csv', ['text'])   # 轉為csv檔

    return lists


def dataProcess():
    tweetList = []
    # 讀取
    data = pd.read_csv('tweets_text.csv')
    for line in data.text:
        line = re.sub(r'http\S+', '', line)
        tweetList.append(line)
    return tweetList


def wordCloud_grah(tweetList):
    text = " ".join(tweetList)  # 將所有推文合在一個string list中
    cloud = WordCloud().generate(text)  # 根據20則推文內容產生文字雲
    cloud.to_file('output.png')     # 產生圖片


def bar_graph(tweetList):
    vader = SentimentIntensityAnalyzer()

    # data1 = []
    # data2 = []
    # data3 = []
    data4 = []
    column = []
    for tweet in tweetList:
        column.append("推文")     # x軸文字
        score = vader.polarity_scores(tweet)    # 根據每則推文進行情緒分析
        # print(score)
        # data1.append(score['neg'])     # 負面
        # data2.append(score['neu'])     # 中性
        # data3.append(score['pos'])     # 正面
        if score['compound'] > 0:       # 中位數
            data4.append(
                opts.BarItem(name="推文", value=score['compound'], itemstyle_opts=opts.ItemStyleOpts(color="#c23531")))
            # 正值為紅色
        elif score['compound'] == 0:
            data4.append(
                opts.BarItem(name="推文", value=score['compound'], itemstyle_opts=opts.ItemStyleOpts(color="#61a0a8")))
            # 0為中性情緒
        else:
            data4.append(
                opts.BarItem(name="推文", value=score['compound'], itemstyle_opts=opts.ItemStyleOpts(color="#2f4554")))
            # 負值為深藍色

    bar = Bar()
    bar.add_xaxis(column)   # 設定x軸
    bar.add_yaxis("綜合分析", data4)     # 設定y軸
    # bar.add_yaxis("負面", data1)
    # bar.add_yaxis("中性", data2)
    # bar.add_yaxis("正面", data3)
    bar.set_global_opts(title_opts=opts.TitleOpts(title="柱狀圖", subtitle="情緒變化趨勢"))  # 標題
    bar.render("output.html")   # 結果是html


def removeOldData(lists):
    for i in range(0, len(lists)-1, 1):
        filePath = Path('C:/Users/ninab/twitter-files/' + lists[i])     # 找到json檔位址
        try:
            filePath.unlink()   # 刪除該路徑檔案
        except OSError as e:
            print(f"Error:{ e.strerror}")


if __name__ == '__main__':
    result = []
    jsonData = []

    username = input("輸入欲搜尋的twitter ID(不含@): ")

    jsonData = getTweet(username)
    result = dataProcess()
    wordCloud_grah(result)
    bar_graph(result)
    removeOldData(jsonData)
