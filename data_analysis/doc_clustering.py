import nltk
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from matplotlib import pyplot as plt
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage
import hdbscan

# I wanted more control to test certain things with stemming, therefore, this is needed to override the TfidfVectorizer
def needed_tfidf(doc):
    return doc

def doc_clustering(data):
    tokenized_docs = []
    for index, row in data.iterrows():
        if(row['cluster'] == None):
            tmp = stem_token_stop(row['text'])
            tokenized_docs.append(tmp)
    #vectorize sentences 
    vectorizer = TfidfVectorizer(
        analyzer = 'word',
        tokenizer = needed_tfidf,
        preprocessor = needed_tfidf,
        token_pattern = None)  
    #transform using TFIDF vectorizer
    vectors = vectorizer.fit_transform(tokenized_docs)
    dataframe = pd.DataFrame(vectors.toarray(), columns=vectorizer.get_feature_names())
    print('tf-idf Matrix:')
    print(dataframe)
    labels = clustering(dataframe.to_numpy(), True)
    return labels

# removes stopwords, tokenizes the docs and stems the words
# returns array with stemmed words per doc 
# partly from http://brandonrose.org/clustering?ref=dzone
def stem_token_stop(doc):
    stopwords = nltk.corpus.stopwords.words('english')
    stemmer = nltk.stem.porter.PorterStemmer()
    alphabet = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    #remove <br> from removing redundancy
    doc = doc.replace('<br>','')
    #remove \n 
    doc = doc.replace('\n',' ')
    #remove everything between [** something **]
    doc = re.sub(r'\[\*\*.+?\*\*\]', '', doc)
    #remove time followed by am or pm 
    doc = re.sub(r'\d( am| pm|am|pm| AM| PM|AM|PM)', '', doc)
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word for sent in nltk.sent_tokenize(doc) for word in nltk.word_tokenize(sent)]
    #remove stopwords
    tokens = [token for token in tokens if token not in stopwords]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            #remove everything that are not letter 
            token = ''.join(filter(alphabet.__contains__, token))
            filtered_tokens.append(token)
    #lower case everything
    filtered_tokens = [token.lower() for token in filtered_tokens]
    #stemm all the word using porter stemmer
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems

#tfidf_array is array containing all docs in vector space and DBSCAN is a bool to use DBSCAN algo or agglomerative clustering
def clustering(tfidf_array, DBSCAN):
    if(DBSCAN == False):
        # to check for the number of clusters 
        plt.figure(figsize=(10, 7))
        dendrogram(linkage(tfidf_array, method = 'ward'))
        plt.show()
        #fill in optimal cluster size from dendrogram
        # model = AgglomerativeClustering(n_clusters=6, affinity='euclidean', linkage='ward') 
        # model.fit_predict(tfidf_array)
        # labels = model.labels_
        # print(labels)
    else:
        #cluster doc vectors with HDBSCAN algo
        model = hdbscan.HDBSCAN(min_cluster_size=2)
        labels = model.fit_predict(tfidf_array)        
    return labels