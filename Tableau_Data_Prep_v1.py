# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 20:45:33 2022

@author: harsh
"""
if __name__ == '__main__':
    import pandas as pd
    import re
    import numpy
    
    import warnings
    warnings.filterwarnings("ignore")
    
    indian_twitter_data = pd.read_csv("filtered_twitter_data.csv")
    
    def remove_usernames_links(tweet):
        tweet = re.sub('@[^\s]+','',tweet)
        tweet = re.sub('http[^\s]+','',tweet)
        return tweet
    
    indian_twitter_data['Tweet_Text'] = indian_twitter_data['Tweet_Text'].apply(remove_usernames_links)
    
    
    
    import gensim
    from nltk.stem import WordNetLemmatizer, SnowballStemmer
    # import nltk
    # nltk.download('wordnet')
    # nltk.download('omw-1.4')
    
    stemmer = SnowballStemmer('english')
    
    def lemmatize_stemming(text):
        return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))
    
    def preprocess(text):
        result = []
        for token in gensim.utils.simple_preprocess(text):
            if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
                result.append(lemmatize_stemming(token))
        return result
    
    processed_tweets = indian_twitter_data['Tweet_Text'].map(preprocess)
    
    remove_qurey_words = ['trump', 'donald','biden', 'elect', 'presid','senat', 'republican','democrat']
    
    dictionary = gensim.corpora.Dictionary(processed_tweets)
    del_ids = [k for k,v in dictionary.items() if v in remove_qurey_words]
    dictionary.filter_tokens(bad_ids=del_ids)
    
    dictionary.filter_extremes(no_below = 15, no_above = 0.7, keep_n = 5000)
    bow_corpus = [dictionary.doc2bow(doc) for doc in processed_tweets]
    
    lda_model = gensim.models.LdaMulticore(bow_corpus, num_topics=10, id2word=dictionary, passes=10, workers = 3)
    
    topics = lda_model.show_topics(formatted=False)
    
    
    
    def format_topics_sentences(ldamodel = lda_model, corpus = bow_corpus, texts = indian_twitter_data['Tweet_Text']):
        # Init output
        sent_topics_df = pd.DataFrame()
    
        # Get main topic in each document
        for i, row_list in enumerate(ldamodel[corpus]):
            row = row_list[0] if ldamodel.per_word_topics else row_list            
            # print(row)
            row = sorted(row, key=lambda x: (x[1]), reverse=True)
            # Get the Dominant topic, Perc Contribution and Keywords for each document
            for j, (topic_num, prop_topic) in enumerate(row):
                if j == 0:  # => dominant topic
                    wp = ldamodel.show_topic(topic_num)
                    topic_keywords = ", ".join([word for word, prop in wp])
                    sent_topics_df = sent_topics_df.append(pd.Series([int(topic_num), round(prop_topic,4), topic_keywords]), ignore_index=True)
                else:
                    break
        sent_topics_df.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']
    
        # Add original text to the end of the output
        contents = pd.Series(texts)
        sent_topics_df = pd.concat([sent_topics_df, contents], axis=1)
        return(sent_topics_df)
    
    print("Applying Topic Modelling")
    df_topic_sents_keywords = format_topics_sentences(lda_model, bow_corpus, indian_twitter_data['Tweet_Text'])
    print("Topic Modelling completed")
    
    # Format
    df_dominant_topic = df_topic_sents_keywords.reset_index()
    df_dominant_topic.columns = ['Document_No', 'Dominant_Topic', 'Topic_Perc_Contrib', 'Keywords', 'Text']
    # df_dominant_topic.head(10)
    
    indian_twitter_data['Dominant_Topic'] = df_dominant_topic['Dominant_Topic']
    print("Dominant Topics Extracted")
    
    query_string_republican = ['Conservative','Maga','Christ follower','Christian','Jesus','God','Husband',
                               'Family','Father','Wife','Loves America',
                               'Populist','Republican','Hindu','Patriot','Child of God','Trump']
    
    query_string_democrat = ['Artist','Producer','Writer','Director','Actor','Editor',
                             'Black lives matter','Him','Her','She','Vote blue','Democrat',
                             'Gun control','Stand with president Biden','LGBT','Pro choice']
    
    
    indian_twitter_data['Support_Group'] = ''
    indian_twitter_data['Sentiment'] = ''
    indian_twitter_data['Sentiment_Score'] = 0.00
    
    
    
    print("Importing Sentiment Model")
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    tokenizer = AutoTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment-latest")
    model = AutoModelForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment-latest")
    
    from transformers import pipeline
    sentiment_task = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer, max_length=512, truncation=True)
    # sentiment = sentiment_task(list(indian_twitter_data.Tweet_Text))
    # print("Sentiment Evaluation Done!")
    
    temp = {}
    word = ''
    sentiment = []
    republican_supporter_data = pd.DataFrame()
    democratic_supporter_data = pd.DataFrame()
    middle_data = pd.DataFrame()
    
    for row_num in range(len(indian_twitter_data)):
    # for row_num in range(10000):
        
        sentiment = sentiment_task(indian_twitter_data['Tweet_Text'][row_num])
        
        indian_twitter_data['Sentiment'][row_num] = sentiment[0]['label']
        indian_twitter_data['Sentiment_Score'][row_num] = sentiment[0]['score']
            
        temp = {'Username': indian_twitter_data.Username[row_num],
                'User_Description': indian_twitter_data.User_Description[row_num],
                'User_Location': indian_twitter_data.User_Location[row_num],
                'Tweet_Text': indian_twitter_data.Tweet_Text[row_num],
                'Location' : indian_twitter_data.Location[row_num],
                'Created_At' : indian_twitter_data.Created_At[row_num],
                'Sentiment' : indian_twitter_data.Sentiment[row_num],
                'Sentiment_Score' : indian_twitter_data.Sentiment_Score[row_num],
                'Dominant_Topic' : indian_twitter_data.Dominant_Topic[row_num]}
    
        if indian_twitter_data['User_Description'][row_num] != indian_twitter_data['User_Description'][row_num]:
            middle_data = middle_data.append(temp, ignore_index = True)
            indian_twitter_data['Support_Group'][row_num] = "Middle"
            print(row_num, "NaN")
        
        elif any(word.lower() in indian_twitter_data['User_Description'][row_num].lower() for word in query_string_republican):
            republican_supporter_data = republican_supporter_data.append(temp, ignore_index = True)
            indian_twitter_data['Support_Group'][row_num] = "Republican"
            print(row_num, "Republican")
        
        elif any(word.lower() in indian_twitter_data['User_Description'][row_num].lower() for word in query_string_democrat): 
            democratic_supporter_data = democratic_supporter_data.append(temp, ignore_index = True)
            indian_twitter_data['Support_Group'][row_num] = "Democratic"
            print(row_num, "Democratic")
        
        else:
            middle_data = middle_data.append(temp, ignore_index = True)
            indian_twitter_data['Support_Group'][row_num] = "Middle"
            print(row_num, "Middle")
        
    
    democratic_supporter_data['Support_Group'] = "Democratic"
    republican_supporter_data['Support_Group'] = "Republican"
    middle_data['Support_Group'] = "Middle"
    
    
    
    indian_twitter_data.to_csv("tableau_data_input.csv")
    
    print("Data Seggregation completed")



