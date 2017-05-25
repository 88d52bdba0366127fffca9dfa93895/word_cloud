import re

import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from spacy.en import English
from nltk.corpus import stopwords
from wordcloud import WordCloud

df = pd.read_csv('hacker_news_comments.csv')
df['story_time'] = pd.to_datetime(df['story_time'], unit='s')
df['year'] = df['story_time'].apply(lambda x: x.year)
df['month'] = df['story_time'].apply(lambda x: x.month)

grouped_ym = df.groupby(['year', 'month'])['comment_text'].apply(list)
indexes_ym = grouped_ym.index

nlp = English()
stop_words = stopwords.words('english')
with open('stopword.txt') as f:
    content = f.readlines()

stop_words.extend([x.strip() for x in content])

filename = 'hacker_news_comments'
for i in range(len(grouped_ym)):
    #for i in range(3):
    data = " ".join(grouped_ym[i])
    soup = BeautifulSoup(data, "html.parser")
    text0 = soup.text
    text1 = re.sub(r'http\S+', '', text0)
    text2 = " ".join([''.join(e for e in t.lower() if e.isalnum())
        for t in text1.split()])
    doc = nlp(text2)
    text3 = [np.text for np in doc.noun_chunks
        if len(np.text) >= 3 and np.text not in stop_words]
    text4 = " ".join(text3)
    time = indexes_ym[i]
    year = str(time[0])
    month = str(time[1])
    wordcloud = WordCloud(max_font_size=40).generate(text4)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title('Time: %s/%s' % (year, month))
    plt.savefig(filename + '%s_%s.png' % (year, month))
    plt.close()
    # plt.show()

grouped_y = df.groupby(['year'])['comment_text'].apply(list)
indexes_y = grouped_y.index

for i in range(len(grouped_y)):
    data = " ".join(grouped_y.iloc[i])
    soup = BeautifulSoup(data, "html.parser")
    text0 = soup.text
    text1 = re.sub(r'http\S+', '', text0)
    text2 = " ".join([''.join(e for e in t.lower() if e.isalnum())
        for t in text1.split()])
    doc = nlp(text2)
    text3 = [np.text for np in doc.noun_chunks
        if len(np.text) >= 3 and np.text not in stop_words]
    text4 = " ".join(text3)
    year = str(indexes_y[i])
    print year
    wordcloud = WordCloud(max_font_size=40).generate(text4)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title('Time: %s' % (year))
    plt.savefig(filename + '%s.png' % (year))
    plt.close()
    # plt.show()
