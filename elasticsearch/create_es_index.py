from elasticsearch import Elasticsearch
import pandas as pd
from sklearn.feature_extraction import text
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction import text
from nltk.stem.porter import PorterStemmer

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

oracle = pd.read_csv('oracleTM.csv', index_col=0)
oracle.drop_duplicates(inplace=True)

wikibooks = pd.read_csv('data.csv', index_col=0)
wikibooks.drop_duplicates(inplace=True)

oracle = pd.read_csv('oracleTM.csv', index_col=0)
oracle.drop_duplicates(inplace=True)



stop = text.ENGLISH_STOP_WORDS
porter_stemmer = PorterStemmer()

wikibooks['text'] = wikibooks["text"].apply(lambda x: ''.join(["" if ord(i) < 32 or ord(i) > 126 else i for i in x]))
oracle['text'] = oracle["text"].apply(lambda x: ''.join(["" if ord(i) < 32 or ord(i) > 126 else i for i in x]))

wikibooks['text'] = wikibooks['text'].apply(lambda x: ' '.join([porter_stemmer.stem(word.lower()) for word in x.split() if word not in (stop)]))
oracle['text'] = oracle['text'].apply(lambda x: ' '.join([porter_stemmer.stem(word.lower()) for word in x.split() if word not in (stop)]))
    
def preprocessing(df_col):
    stop = text.ENGLISH_STOP_WORDS
    porter_stemmer = PorterStemmer()
    df_col = df_col.apply(lambda x: ''.join(["" if ord(i) < 32 or ord(i) > 126 else i for i in x]))
    df_col = df_col.apply(lambda x: ' '.join([porter_stemmer.stem(word.lower()) for word in x.split() if word not in (stop)]))
    return df_col

wikibooks['json'] = wikibooks.apply(lambda x: x.to_json(), axis=1)
oracle['json'] = oracle.apply(lambda x: x.to_json(), axis=1)

es.indices.delete(index='java_wikibook', ignore=[400, 404])

for index in range(len(wikibooks)):
    es.index(index='java_wikibook', doc_type='document', id=index, body=wikibooks.iloc[index]['json'])

es.indices.delete(index='java_oracle', ignore=[400, 404])
for index in range(len(oracle)):
    es.index(index='java_oracle', doc_type='document', id=index, body=oracle.iloc[index]['json'])

