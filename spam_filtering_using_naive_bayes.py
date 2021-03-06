# -*- coding: utf-8 -*-
"""Spam_filtering_using_Naive_Bayes.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZelTlqTHTzJzUDsS3QZxww6MEwpfTicj
"""

import numpy as np
import pandas as pd
import re
import nltk
import time
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import GaussianNB

df = pd.read_csv('/content/spam.csv',encoding='latin-1')

df.head()

"""<h3>Cleaning and Preparing text</h3>
<ul>
    <li>Cleaning links</li>
    <li>Cleaning digits except alphabetical and numeric characters</li>
    <li>Lowering</li>
    <li>Tokenising</li>
    <li>Lemmatizing and Removing Stop words</li>
    <li>Bag of words</li>
</ul>

<h3>Cleaning links</h3>
<p>There are links in the mail such as: <a>https://google.com.tr</a>. If we don't remove them they can cause problems.</p>
<p>To clean the following links, we can use Regex(regular) expression.A regular expression is a special sequence of characters that helps you match or find other strings or sets of strings, using a specialized syntax held in a pattern. Regular expressions are widely used in UNIX world. </p>
"""

x = df["v2"]
x_clnd_link = [re.sub(r"http\S+", "", text) for text in x]

print(x_clnd_link[0])

"""<h3>Cleaning digits except alphabetical and numeric characters</h3>
<p>As you can see from the text above, there are a lot of digits such as <b>*</b> and <b>:</b> They don't have a meaning, so we should remove them from the texts.

In order to clean unrelevant digits we'll use regex again.</p>
"""

pattern = "[^a-zA-Z0-9]"

"""<p>-This helps to remove special characters</p>"""

#This means to replace all the characters following the pattern
x_cleaned = [re.sub(pattern, " ",text) for text in x_clnd_link]

print(x_cleaned[0])

"""<p><b>Now let's lower the texts, I won't add a section for it because it is a familiar process from the vanilla python.

</b></p>
"""

x_lowered = [text.lower() for text in x_cleaned]

print(x_lowered[0])

"""<h3>Tokeninzing</h3>
<p>In order to create a feature that shows whether the text includes the word or not, we need to split words into lists, we can do this using pythonString.split() but there is a better function to do this in NLTK.

Let's tokenize the texts.</p>
"""

nltk.download('punkt')

x_tokenized = [nltk.word_tokenize(text) for text in x_lowered]

print(x_tokenized[0])

"""<p>- Each sentence turned into a list that contains words.</p>

<h3>Lemmatizing and Removing Stopwords</h3>
<p>In natural languages, words can get additional so each word can have a lot of versions, sometimes these additionals may give tips to us but in filtering spams, we don't need them.There are two ways to remove additionals: <b>Stemmers and Lemmatizers</b> </p>

<h3>Stemmers</h3>
<p>Stemmers are rule based weak tools, they remove additionals using rules but in natural languages everything does not follow the rules. Also It cant change tenses, for instance lemmatizers convert learnt into learn, stemmers don't touch them. Although stemmers are weak they are fast and although so many natural language do not have lemmatizers most of them have stemmers.</p>

<h3>Lemmatizers</h3>
<p>Lemmatizers uses dictionaries to remove additionals and change tenses. They work good but developing a lemmatizer is hard and needs a lot of resource, so they are rare. Also lemmatizers use dictionaries, and that causes lemmatizers being slow.

In this kernel we'll use NLTK's WordNet Lemmatizer. WordNet is a big dictionary.</p>
"""

nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
lemma = WordNetLemmatizer()

"""<p>- Now, we can easily use lemmatizer</p>"""

words = ["pets","bats","cats","removed","beers","went","stopped","studied"]
for word in words:
    print(lemma.lemmatize(word), end=" ")

"""<p>- We can now lemmatize our tokenized text</p>"""

x_lemmatized = [[lemma.lemmatize(word) for word in text] for text in x_tokenized]

print(x_lemmatized[0])

"""<h3>Removing Stopwords</h3>
<p>In natural languages there are words that not have a special meaning such as <b>will</b>, it is always a tense and such as <b>and,or</b>

In order to win from time and improve the model we should remove them. There are several ways to remove them but in this kernel we'll use stopwords corpora of NLTK. There are stopwords of 11 natural language in there.</p>
"""

import nltk
nltk.download('stopwords')

stopwords = nltk.corpus.stopwords.words('english')
x_prepared = [[word for word in text if word not in stopwords] for text in x_lemmatized]

print(x_prepared[0])

"""<p>Let's see the unique words of our dataset</p>

<h3>Bag of words</h3>
<p>And we came to the final process of this section: Bag of Words. Bag of Words is an easy approach to make sense of texts.</p>
"""

vectorizer = CountVectorizer(max_features=20000)
x = vectorizer.fit_transform([" ".join(text) for text in x_prepared]).toarray()

x.shape

x_train,x_test,y_train,y_test = train_test_split(x,np.asarray(df["v1"]),random_state=42,test_size=0.2)
x_train.shape
print(y_test)

"""<h3>Naive Bayes Model</h3>"""

start_time = time.time()
NB = GaussianNB()
NB.fit(x_train,y_train)
end_time = time.time()

print(round(end_time-start_time,2))

NB.score(x_test,y_test)

import itertools

from sklearn.metrics import confusion_matrix
y_pred = NB.predict(x_test)

conf = confusion_matrix(y_pred=y_pred,y_true=y_test)
import seaborn
import matplotlib.pyplot as plt

def plot_confusion_matrix(conf, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Greens):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        conf = conf.astype('float') / conf.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(conf)

    plt.imshow(conf, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = conf.max() / 2.
    for i, j in itertools.product(range(conf.shape[0]), range(conf.shape[1])):
        plt.text(j, i, format(conf[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if conf[i, j] > thresh else "black")

    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()

plt.figure()
plot_confusion_matrix(conf, classes=['Non Spam','Spam'], normalize=False,
                      title='Confusion matrix')

"""

Pickle is the easiest way of saving a python object.</p>"""

import pickle

with open("model.pckl", mode ="wb") as F:
    pickle.dump(NB,F)
    
with open("vectorizer.pckl", mode="wb") as F:
    pickle.dump(vectorizer, F)

def predict_mail(mail):
    
    model = pickle.load(open("model.pckl",mode="rb"))
    vectorizer = pickle.load(open("vectorizer.pckl",mode="rb"))
    
    lemma = WordNetLemmatizer()
    
    stopwords = nltk.corpus.stopwords.words('english')
    
    mail = re.sub(r"http\S+", "", mail)
    mail = re.sub("[^a-zA-Z0-9]"," ",mail)
    mail = mail.lower()
    mail = nltk.word_tokenize(mail)
    mail = [lemma.lemmatize(word) for word in mail]
    mail = [word for word in mail if word not in stopwords]
    mail = " ".join(mail)
    
    vector = vectorizer.transform([mail])
    decision = model.predict(vector.toarray())
    
    return decision[0]

predict_mail(" All end sem and also the re- examinations of June 2021 will be held through online mode, and it will be of 40 marks with Two Hours duration followed by 45 minutes more, in order to offset more time if at all spent in dealing with any connectivity or technical snag during the examination. ")

predict_mail("It is hereby to inform to all concerned students having back log in practical courses that their practical re-examinations will be conducted from 21 to 30 June 2021 on viva basis by the respective faculty who will announce its schedule along with the digital platform for it and its log in detail to the students in advance. The list of such students has been attached herewith for ready reference and perusal of all concerned.")

predict_mail("Free entry in 2 a weekly competition to win FA Cup final tickets 21st May 2005. Text FA to 87121 to receive entry question(std txt rate)T&C's apply 08452810075over18's")

"""## WORDCLOUD"""

from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

def plot_wordcloud(text, mask=None, max_words=200, max_font_size=100, figure_size=(24.0,16.0), 
                   title = None, title_size=40, image_color=False):
    stopwords = set(STOPWORDS)

    wordcloud = WordCloud(background_color='black',
                    stopwords = stopwords,
                    max_words = max_words,
                    max_font_size = max_font_size, 
                    random_state = 42,
                    width=800, 
                    height=400,
                    mask = mask)
    wordcloud.generate(str(text))
    
    plt.figure(figsize=figure_size)
    if image_color:
        image_colors = ImageColorGenerator(mask);
        plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation="bilinear");
        plt.title(title, fontdict={'size': title_size,  
                                  'verticalalignment': 'bottom'})
    else:
        plt.imshow(wordcloud);
        plt.title(title, fontdict={'size': title_size, 'color': 'black', 
                                  'verticalalignment': 'bottom'})
    plt.axis('off');
    plt.tight_layout()

spam_train_index = [i for i,o in enumerate(y_train) if o == "spam"]
non_spam_train_index = [i for i,o in enumerate(y_train) if o == "ham"]

spam_email = np.array(x_prepared)[spam_train_index]
non_spam_email = np.array(x_prepared)[non_spam_train_index]

plot_wordcloud(spam_email,title = 'Spam Email')

plot_wordcloud(non_spam_email,title="Non Spam Email")