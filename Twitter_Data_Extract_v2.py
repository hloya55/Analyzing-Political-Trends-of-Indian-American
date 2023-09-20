 # -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 09:09:41 2022

@author: harsh
"""

import tweepy
import pandas as pd
import time

import warnings
warnings.filterwarnings("ignore")


client = tweepy.Client(bearer_token='AAAAAAAAAAAAAAAAAAAAAJhfVgEAAAAABQ1tu62StG5ItxcJsxgDoCasZ8I%3DnQFwKA81Llft4oqYYOIHvDLGxUiqJ8eVjxfllz6ux3eFO8CxTU')


query = '(election OR usaelection OR uselection OR election2024 OR presidentialelection OR Trump OR Biden OR senate OR congressman OR congresswoman OR hindu trump OR modi trump OR modi uselection OR indian us president OR india us president OR modi biden OR indian biden OR demoractic president OR republican president) place_country:US'
# query = '(hindu trump OR modi trump OR modi uselection OR indian us president OR india us president OR modi biden OR indian biden OR indian trump) place_country:US'    

data = pd.DataFrame(columns=['Username', 'User_Description', 'User_Location', 'Tweet_Text', 'Location', 'Created_At'])

start = time.time()

for itr in range(2000):
    
    if itr == 0 :
        end = '2021-01-08T22:32:01Z'
    else:
        end = data.iloc[-1][5]


    tweets = client.search_all_tweets(query = query,
                                      tweet_fields = ['text', 'created_at'],
                                      user_fields = ['name', 'username', 'description', 'location'],
                                      place_fields = ['full_name', 'country_code'],
                                      expansions = ['geo.place_id','author_id'],
                                      end_time = end,
                                      max_results = 500)
    
    # itr_tweet_id = tweets.meta['oldest_id']
    # token = tweets.meta['next_token']
    
    for tweet,user,loc in zip(tweets.data, tweets.includes['users'],tweets.includes['places']):
        
        temp = {'Username': user.name,
                'User_Description': user.description,
                'User_Location': user.location,
                'Tweet_Text': tweet.text,
                'Location' : loc.full_name,
                'Created_At' : tweet.created_at}
        
        data = data.append(temp, ignore_index = True)
        
    print("Iteration Completed :",itr)
    # time.sleep(1)

data.to_csv("[Dump_18]data_sample.csv",index = False)

end = time.time()

elapsed_time = end - start
print("Time Taken -", round(elapsed_time/60),"Minutes")








# (election OR usaelection OR election2022 OR midterms OR presidentialelection) 
# (place_country:USA OR place_country: United States of America) -russia -local -international lang:en
# qurey will not match with the quoted tweet 

# try catch in case of missing fields




