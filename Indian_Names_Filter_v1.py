# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 20:11:17 2022

@author: harsh
"""

import pandas as pd

import warnings
warnings.filterwarnings("ignore")
    
indian_names_df = pd.read_csv("indian_names_pool.csv")
first_name = list(indian_names_df['first_name'])
last_name = list(indian_names_df['last_name'])
indian_names = first_name
indian_names.extend(last_name)


df1 = pd.read_csv("[Dump_5]data_sample.csv")
df2 = pd.read_csv("[Dump_6]data_sample.csv")
df3 = pd.read_csv("[Dump_7]data_sample.csv")
df4 = pd.read_csv("[Dump_8]data_sample.csv")
df5 = pd.read_csv("[Dump_9]data_sample.csv")
df6 = pd.read_csv("[Dump_10]data_sample.csv")
df7 = pd.read_csv("[Dump_11]data_sample.csv")
df8 = pd.read_csv("[Dump_12]data_sample.csv")
df9 = pd.read_csv("[Dump_13]data_sample.csv")
df10 = pd.read_csv("[Dump_14]data_sample.csv")
df11 = pd.read_csv("[Dump_15]data_sample.csv")
df12 = pd.read_csv("[Dump_16]data_sample.csv")
df13 = pd.read_csv("[Dump_17]data_sample.csv")
df14 = pd.read_csv("[Dump_18]data_sample.csv")





filtered_twitter_data = pd.DataFrame()
twitter_data = pd.DataFrame()

twitter_data = twitter_data.append(df1)
twitter_data = twitter_data.append(df2)
twitter_data = twitter_data.append(df3)
twitter_data = twitter_data.append(df4)
twitter_data = twitter_data.append(df5)
twitter_data = twitter_data.append(df6)
twitter_data = twitter_data.append(df7)
twitter_data = twitter_data.append(df8)
twitter_data = twitter_data.append(df9)
twitter_data = twitter_data.append(df10)
twitter_data = twitter_data.append(df11)
twitter_data = twitter_data.append(df12)
twitter_data = twitter_data.append(df13)
twitter_data = twitter_data.append(df14)





final_list = []


for row in twitter_data['Username']:

    list_ = []

    for chr_ in str(row):
        if chr_.isalpha() or chr_ == " ":
            list_.append(chr_)
    name = "".join(list_)

    name_first_last = name.split(" ")
    list_temp = []
    for cnt in range(len(name_first_last)):
        list_temp.append(name_first_last[cnt])

    # if len(name_first_last) > 1:
    #     list_temp = [name_first_last[0],name_first_last[1]]
    # else:
    #     list_temp = [name_first_last[0], ""]

    final_list.append(list_temp)

    

# print(final_list)

twitter_filtred_indians = []
temp = {}

for idx,each in enumerate(final_list):
    print(idx)
    # if (each[0].lower() in first_name) or (each[1].lower() in last_name):
    #     twitter_filtred_indians.append(each)
    #     filtered_twitter_data = filtered_twitter_data.append(twitter_data.iloc[idx])
        
    for x in each:
        if x.lower() in indian_names:
            twitter_filtred_indians.append(each)
            filtered_twitter_data = filtered_twitter_data.append(twitter_data.iloc[idx])
            
list_unique = set()

for i in twitter_filtred_indians:
    list_unique.add(i[0])
    
filtered_twitter_data.to_csv("filtered_twitter_data.csv",index = False)

