import tweepy                                      #access the Twitter API with Python
from textblob import TextBlob                           # library for processing textual data
from wordcloud import WordCloud                          #data visualization technique used for representing text data in which the size of each word indicates its frequency or importance
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

#twitter credentials !!!

#authentication obj
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

# authentication access token
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# create API obj 
api = tweepy.API(auth)

# extract tweets from the user
posts = api.user_timeline(screen_name="elonmusk", count = 500, lang= "en", tweet_mode="extended")

#recent 5 tweets
print("Show 5 recent tweets: \n")
for tweet in posts[0:5]:
  print(tweet.full_text + '\n')
  
# create dataframe with a column tweets
df = pd.DataFrame([tweet.full_text for tweet in posts] , columns=['Tweets'])

#show fist 5rows
df.head()

# clean text

# create func to clean tweets
def cleanTxt(text):
  text = re.sub(r'@[A-Za-z0-9]+' , '',text)  #remove @mentions
  text = re.sub(r'#', '',text)  # removing the # symbol
  text = re.sub(r'RT[\s]+', '',text)  #removing retweets
  text = re.sub(r'https?:\/\/\S+', '',text)  #remove the hyper link

  return text

#cleaning text
df['Tweets'] = df['Tweets'].apply(cleanTxt)

# show clean text
df

# create a func to get the subjectivity
def getSubjectivity(text):
  return TextBlob(text).sentiment.subjectivity

# create a func to get polarity
def getPolarity(text):
  return TextBlob(text).sentiment.polarity

# create two new columns 
df['Subjectivity'] = df['Tweets'].apply(getSubjectivity)
df['Polarity'] = df['Tweets'].apply(getPolarity)

#print tweets
df

#create a function to compute negative and positive analysis

def getAnalysis(score):
  if score<0:
    return 'Negative'
  elif score==0:
    return 'Neutral'
  else:
    return 'Positive'

df['Analysis'] = df['Polarity'].apply(getAnalysis)

#Show the dataframe
df

# print positive tweets
j=1
sortedDF = df.sort_values(by=['Polarity'])
for i in range(0,sortedDF.shape[0]):
  if(sortedDF['Analysis'][i] == 'Positive'):
    print(str(j) + ') ' +sortedDF['Tweets'][i])
    print()
    j=j+1

#plot the polarity and subjectivity
plt.figure(figsize=(8,6))
for i in range(0, df.shape[0]):
  plt.scatter(df['Polarity'][i], df['Subjectivity'][i], color='blue')

plt.title('Sentiment Analysis')
plt.xlabel('Polarity')
plt.ylabel('Subjectivity')

# % of positive tweets
round( (ptweets.shape[0] / df.shape[0] )* 100 ,1)
ntweets = df[df.Analysis == 'Negative']
ntweets = ntweets['Tweets']
nptweets = df[df.Analysis == 'Neutral']
nptweets = nptweets['Tweets']

df['Analysis'].value_counts()

#plot and visualize the contents
plt.title('Sentimental Analysis')
plt.xlabel('Sentiment')
plt.ylabel('Counts')

df['Analysis'].value_counts().plot(kind='bar')
plt.show()
