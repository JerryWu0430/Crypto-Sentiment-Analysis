#   import libraries
import os
import re
from regex import D
import sys
import tweepy
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import PySimpleGUI as sg
from textblob import TextBlob
from tweepy import OAuthHandler
from matplotlib.ticker import NullFormatter 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
sg.theme("Reddit")

#   import keys for Twitter API Elevated Access (personal)
application_path = os.path.abspath('login.txt')
keys = open(f"{application_path}",'r')
lines = keys.readlines()
consumer_key = lines[0].rstrip()
consumer_secret = lines[1].rstrip()
access_token = lines[2].rstrip()
access_token_secret = lines[3].rstrip()
bearer_token = lines[4].rstrip()

#   authenticate to the twitter API
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#   create a client to collect tweets
Client = tweepy.Client(bearer_token=bearer_token, 
                    consumer_key= consumer_key, 
                    consumer_secret= consumer_secret,
                    access_token= access_token,
                    access_token_secret=access_token_secret)

#   set the display option of tweets to 100 characters & show all the rows of tweets collected
pd.options.display.max_colwidth = 100
pd.set_option('display.max_rows', 9999)

#   layout of the GUI, where there is a homepage and 5 seperated pages for the 5 cryptocurrency
homepage = [[sg.Text('Twitter Sentiment Analysis on Cryptocurrency',font = "Helvetica 20",size=(50,1)),sg.Button("Refresh for More Tweets",font = "Helvetica 15",key="refresh")],
        [sg.Text("Cryptocurrency just like any other investment involves risks, and has potential in losing all your money. (DYOR) 📈📈 ", font = "Helvetica 10")],
        [sg.Text("This application is not any financial advice, but an educational application to monitor the sentiment of Twitter users. ", font = "Helvetica 10")],
        [sg.Text("(Application) Discord/Telegram/Twitter → Crypto community", font = "Helvetica 10")],
        [sg.Text("(Website) CoinMarketCap → Live price indicator", font = "Helvetica 10")],
        [sg.Text("(Website) Coinbase → Exchanging currencies to cryptocurrencies", font = "Helvetica 10")],
        [sg.Text("Total tweets in an hour",font = "Helvetica 11",key="total_tweets")],
        [sg.Text("TOP #1 Crypto Currency",font = "Helvetica 11",key="T1")],
        [sg.Text("TOP #2 Crypto Currency",font = "Helvetica 11",key="T2")],
        [sg.Text("TOP #3 Crypto Currency",font = "Helvetica 11",key="T3")],
        [sg.Text("TOP #4 Crypto Currency",font = "Helvetica 11",key="T4")],
        [sg.Text("TOP #5 Crypto Currency",font = "Helvetica 11",key="T5")],
        [sg.Text("Tweets Collected",font = "Helvetica 11",key="collect")],
        [sg.Canvas(key='-CANVAS-')]]
bitcoin = [[sg.Text('Bitcoin Sentiment Analysis (#BTC)',font = "Helvetica 20",size=(50,1)),sg.Button("Refresh for More Tweets",font = "Helvetica 15",key="refresh")],
        [sg.Text('[number of tweets per hour]',font = "Helvetica 15",key="total_Bitcoin")],
        [sg.Text("[sentiment for Bitcoin]",font = "Helvetica 15",key="Bitcoin_pos")],
        [sg.Text("[sentiment for Bitcoin]",font = "Helvetica 15",key="Bitcoin_neu")],
        [sg.Text("[sentiment for Bitcoin]",font = "Helvetica 15",key="Bitcoin_neg")],
        [sg.Multiline("[tweets and their corresponding sentiment]",font = "Helvetica 14",enter_submits=False,key="Bitcoin",size=(120,30))],]

ethereum = [[sg.Text('Ethereum Sentiment Analysis (#ETH)',font = "Helvetica 20",size=(50,1)),sg.Button("Refresh for More Tweets",font = "Helvetica 15",key="refresh")],
        [sg.Text('[number of tweets per hour]',font = "Helvetica 15",key="total_Ethereum")],
        [sg.Text("[sentiment for Ethereum]",font = "Helvetica 15",key="Ethereum_pos")],
        [sg.Text("[sentiment for Ethereum]",font = "Helvetica 15",key="Ethereum_neu")],
        [sg.Text("[sentiment for Ethereum]",font = "Helvetica 15",key="Ethereum_neg")],
        [sg.Multiline("[tweets and their corresponding sentiment]",font = "Helvetica 14",enter_submits=False,key="Ethereum",size=(120,30))],]

binance = [[sg.Text('BinanceCoin Sentiment Analysis (#BNB)',font = "Helvetica 20",size=(50,1)),sg.Button("Refresh for More Tweets",font = "Helvetica 15",key="refresh")],
        [sg.Text('[number of tweets per hour]',font = "Helvetica 15",key="total_BNB")],
        [sg.Text("[sentiment for BinanceCoin]",font = "Helvetica 15",key="BNB_pos")],
        [sg.Text("[sentiment for BinanceCoin]",font = "Helvetica 15",key="BNB_neu")],
        [sg.Text("[sentiment for BinanceCoin]",font = "Helvetica 15",key="BNB_neg")],
        [sg.Multiline("[tweets and their corresponding sentiment]",font = "Helvetica 14",enter_submits=False,key="BNB",size=(120,30))],]

solana = [[sg.Text('Solana Sentiment Analysis (#SOL)',font = "Helvetica 20",size=(50,1)),sg.Button("Refresh for More Tweets",font = "Helvetica 15",key="refresh")],
        [sg.Text('[number of tweets per hour]',font = "Helvetica 15",key="total_Solana")],
        [sg.Text("[sentiment for Solana]",font = "Helvetica 15",key="Solana_pos")],
        [sg.Text("[sentiment for Solana]",font = "Helvetica 15",key="Solana_neu")],
        [sg.Text("[sentiment for Solana]",font = "Helvetica 15",key="Solana_neg")],
        [sg.Multiline("[tweets and their corresponding sentiment]",font = "Helvetica 14",enter_submits=False,key="Solana",size=(120,30))],]

ripple = [[sg.Text('Ripple Sentiment Analysis (#XRP)',font = "Helvetica 20",size=(50,1)),sg.Button("Refresh for More Tweets",font = "Helvetica 15",key="refresh")],
        [sg.Text('[number of tweets per hour]',font = "Helvetica 15",key="total_XRP")],
        [sg.Text("[sentiment for Ripple]",font = "Helvetica 15",key="XRP_pos")],
        [sg.Text("[sentiment for Ripple]",font = "Helvetica 15",key="XRP_neu")],
        [sg.Text("[sentiment for Ripple]",font = "Helvetica 15",key="XRP_neg")],
        [sg.Multiline("[tweets and their corresponding sentiment]",font = "Helvetica 14",enter_submits=False,key="XRP",size=(120,30))],]

layout = [[sg.TabGroup([[sg.Tab("Homepage",homepage),
                        sg.Tab("Bitcoin",bitcoin),
                        sg.Tab("Ethereum",ethereum),
                        sg.Tab("Binance",binance),
                        sg.Tab("Solana",solana),
                        sg.Tab("Ripple",ripple)]],font="Helvetica 16")]]

#   define the window of the GUI, and enable updating for Graph                    
window = sg.Window('Twitter Sentiment Analysis on Cryptocurrencies', layout, finalize=True, element_justification='center', font='Helvetica 18',size=(1300,1000))

#   define class for each cryptocurrency
class CryptoCurrency ():
    def __init__ (self,query):
        self.query = query
        self.pos = int(0)
        self.neg = int(0)
        self.neu = int(0)
        self.total = int(0)
        self.tweets = []

    #   cleant tweets for the sentiment analysis
    def clean_tweet(self,tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    #   using a pretrained model, determine the sentiment of the tweets
    def get_tweet_sentiment(self,tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 'POSITIVE'
        elif analysis.sentiment.polarity == 0:
            return 'NEUTRAL'
        else:
            return 'NEGATIVE'

    #   collect tweets with the limit of the variable count
    def get_tweets (self,count):
        self.tweets = []
        pagination = []

        #   collect tweets using the Cursor function
        for status in tweepy.Cursor(api.search_tweets,f"{self.query} -filter:retweets").items(count):
            pagination.append(status.text)

        #   append the text of the tweet and sentiment together into a dictionary
        for tweet in range(len(pagination)):
            parsed_tweet = {}
            parsed_tweet['SENTIMENT'] = self.get_tweet_sentiment(str(pagination[tweet]))
            parsed_tweet['TEXT'] = str(pagination[tweet])
            self.tweets.append(parsed_tweet)
        return self.tweets
        
    #   get the tweets posted under an hour for each specific cryptocurrency
    def get_tweets_count (self,start,end):
        self.total = Client.get_recent_tweets_count(query = self.query,start_time=start,end_time=end)
        return self.total    

    #   dislay the the total tweets of that specific tweet in an hour, and the # of positive, negative, and neutral tweeets
    def display(self):
            total_tweets = self.pos + self.neg + self.neu
            window[f"{self.query}_pos"].update(f"# of Positive: {self.pos}({round(self.pos/total_tweets*100,2)}%)")
            window[f"{self.query}_neg"].update(f"# of Negative: {self.neg}({round(self.neg/total_tweets*100,2)}%)")
            window[f"{self.query}_neu"].update(f"# of Neutral: {self.neu}({round(self.neu/total_tweets*100,2)}%)")
            window[f"total_{self.query}"].update(f"Total Tweets for {self.query}: {self.total}")
            #   display the tweets and their corresponding sentiment
            window[self.query].update(f"{self.df}")
    
    #   create a dataframe for tweets and their sentiment
    def data_analysis (self,count,pos,neu,neg):
        self.tweets = self.tweets + self.get_tweets(count)
        self.df = pd.DataFrame(self.tweets)

        #   calculate the number of positive, negative, and neutral
        for i in range(len(self.tweets)):
            if self.tweets[i]['SENTIMENT'] == 'POSITIVE':
                self.pos = self.pos +1
            elif self.tweets[i]['SENTIMENT'] == 'NEGATIVE':
                self.neg = self.neg +1
            else:
                self.neu = self.neu +1

        #   add the total number of positive, negative, neutral in a list for further calculation
        pos.append(self.pos)
        neu.append(self.neu)
        neg.append(self.neg)
        return pos,neu,neg
        
    #   add each total tweet into the TOTAL Tweet of 5 cryptocurrencies ALL TOGETHER
    def total_tweets (self,total_tweets,total_sort):
        start_time,end_time = get_time()
        self.total = self.get_tweets_count(start_time,end_time)[3]["total_tweet_count"]
        total_tweets = total_tweets + int(self.total)

        #   creating a dictionary of the name of cryptocurrency and number of tweets colelcted for them
        total_sort[self.query] = self.total
        return total_tweets,total_sort



#   getting the current time and time of an hour ago
def get_time ():
    #   gather current time in RFC3339 datetime style for tweepy operation
    date = datetime.datetime.utcnow()
    time = (date.strftime("%Y-%m-%dT%H:%M:%S"))

    #   determine the end time, because it has to be 1 minute before the current time
    #   if the the end time is 00, -1 would not be an appropriate time
    #   hence go back an hour and set the minute to 59
    if time[14:16] == "00":
        end_time =  time[:11] + str((int(time[11:13])-1))+ ":59" +time[16:] + ".00Z"
    else:
        if len(str(int(time[14:16])-1)) != 2:
            end_time =  time[:14] + "0" +str((int(time[14:16])-1))+ time[16:] + ".00Z"
        else:
            end_time =  time[:14] + str((int(time[14:16])-1))+ time[16:] + ".00Z"

    #   determine the start time for the tweet collection (1 hour before)
    start_time =  time[:11] + str((int(time[11:13])-1))+ time[13:] + ".00Z"
    return start_time, end_time

#   defining the figure, so a matplotlib graph can fit in a pysimplegui format
def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

#   setting the graphs in the homepage
def homepage_chart (pos,neg,neu):
    #   reset the graph when the refresh button is being pressed (avoid overlapse)
    plt.close('all')
    crypto_name = ["BTC","ETH","BNB","SOL","XRP","TOTAL"]

    pos.append(np.average(pos))
    neg.append(np.average(neg))
    neu.append(np.average(neu))

    #   create a dictionary of each sentiment to an array of positive, negative, neutral
    data = {
        "Positive":pos,
        "Neutral":neu,
        "Negative":neg}

    #   create a dataframe 
    df = pd.DataFrame(data,index=crypto_name)

    #   define a stacked horizontal bar graph with different color for each sentiment
    plots = df.plot(kind = 'barh',
            stacked = True,
            figsize=(10,6),
            color = ["#46B748","#FCDE02","#EA1D25"]
            )
    #   define the axis, and position of the graph.
    plt.legend(loc="upper left", ncol=2)
    plt.xlabel("Sentiments")
    plt.ylabel("Cryptocurrencies")

    #   define the figure, and update the graph in the homepage.
    fig = matplotlib.figure.Figure(figsize=(10, 6), dpi=100)
    fig = plt.gcf()
    fig_canvas_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)

    return fig_canvas_agg

#   homepage GUI
def homepage_info (total,rank):
    #update the total tweet collected in an hour
    window['total_tweets'].update(f"Total tweets posted about cryptocurrencies: {total}")
    count = 0
    
    #   for loop to print out all the ranking of popularity of cryptocurrencies
    #   rank is equal to the total_sorted dictionary, hence we need keys to access value
    for key in rank:
        count = count + 1
        display = str(f"T{count}")
        window[display].update(f"{count}. {key}: {rank[key]}")

#   main function
def main():
    #   define each crypto class with their corresponding query for searching
    BTC = CryptoCurrency("Bitcoin")
    ETH = CryptoCurrency("Ethereum")
    BNB = CryptoCurrency("BNB")
    SOL = CryptoCurrency("Solana")
    XRP = CryptoCurrency("XRP")
    #   number of sentiment of each cryptocurrency in a list
    pos = []
    neu = []
    neg = []
    #   combine all the class objects into an array for operation
    crypto = [BTC,ETH,BNB,SOL,XRP]
    #   the number of tweet to collect once the app is opened
    count = 100
    total_tweets = 0
    total_sort = {}
    collect = 0
    #   for each cryptocurrency, gather the number of positive, neutral, negative tweets
    for type in range(len(crypto)):
        pos,neu,neg = crypto[type].data_analysis(count,pos,neu,neg)
        #   gather the total tweets of each crypto currency, add them to the total tweets of ALL 5
        #   append to an dictionary where then it will be sorted
        total_tweets, total_sort = crypto[type].total_tweets(total_tweets,total_sort)
    #   using the dictionary, where the key is the cryptocurrency, and the value is the total tweets
    #   sort in reverse order from greatest to least, and store in a new variable
    total_sorted = dict(sorted(total_sort.items(), key=lambda item: item[1],reverse=True))
    #   display on the GUI
    homepage_info(total_tweets,total_sorted)
    #   display chart on GUI, and obtain the value of fig_agg 
    fig_agg = homepage_chart(pos,neg,neu)
    for coin in crypto:
        coin.display()
    collect = collect + count*5
    window['collect'].update(f"Actual Tweets Collected: {int(collect)}")
    #   GUI Loop
    while True:             
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):
            break
        #   actions when the refresh button is pressed
        if event == "refresh":
            pos = []
            neu = []
            neg = []
            #   collect another 100 tweets 
            for type in range(len(crypto)):
                pos,neu,neg = crypto[type].data_analysis(100,pos,neu,neg)
            #   update information
            fig_agg.get_tk_widget().forget()
            fig_agg = homepage_chart(pos,neg,neu)
            for coin in crypto:
                coin.display()
            collect = collect + count*5
            window['collect'].update(f"Actual Tweets Collected: {int(collect)}")

main()