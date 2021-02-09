from django.shortcuts import render
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from textblob import TextBlob
from wordcloud import WordCloud,STOPWORDS
import matplotlib.pyplot as plt
import os
plt.switch_backend('agg')
nltk.download('stopwords')
settings_dir = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.dirname(settings_dir))
path= os.path.join(PROJECT_ROOT, 'static\img')
path2 = os.path.join(PROJECT_ROOT)

def menu(request):
    return render(request, "menu.html")

def wordcloud_draw(data, color = 'black',type="Pos",product="mobile",loc="overall"):
    words = ' '.join(data)
    cleaned_word = " ".join([word for word in words.split()
                            if 'http' not in word
                                and not word.startswith('@')
                                and not word.startswith('#')
                                and word != 'RT'
                            ])
    wordcloud = WordCloud(stopwords=STOPWORDS,
                      background_color=color,
                      width=500,
                      height=400
                     ).generate(cleaned_word)
    plt.figure(1,figsize=(13, 13))
    plt.imshow(wordcloud)
    plt.axis('off')
    if(product == "mobile"):
        if(loc == "overall"):
            if(type == "Pos"):
                plt.savefig(path+r"\samsung\mobile\overallPos.png", format="png")
            else:
                plt.savefig(path+r"\samsung\mobile\overallNeg.png", format="png")
        elif(loc == "flipkart"):
            if (type == "Pos"):
                plt.savefig(path+r"\samsung\mobile\flipkartPos.png",
                        format="png")
            else:
                plt.savefig(path+r"\samsung\mobile\flipkartNeg.png",
                        format="png")
        elif(loc == "amazon"):
            if (type == "Pos"):
                plt.savefig(path+r"\samsung\mobile\amazonPos.png",
                        format="png")
            else:
                plt.savefig(path+r"\samsung\mobile\amazonNeg.png",
                        format="png")
        elif (loc == "twitter"):
            if (type == "Pos"):
                plt.savefig(path+r"\samsung\mobile\twitterPos.png",
                        format="png")
            else:
                plt.savefig(path+r"\samsung\mobile\twitterNeg.png",
                        format="png")
    elif(product == "tv"):
        if (loc == "overall"):
            if (type == "Pos"):
                plt.savefig(path+
                    r"\samsung\television\overallPos.png",
                    format="png")
            else:
                plt.savefig(path+
                    r"\samsung\television\overallNeg.png",
                    format="png")
        elif (loc == "flipkart"):
            if (type == "Pos"):
                plt.savefig(path+
                    r"\samsung\television\flipkartPos.png",
                    format="png")
            else:
                plt.savefig(path+
                    r"\samsung\television\flipkartNeg.png",
                    format="png")
        elif (loc == "amazon"):
            if (type == "Pos"):
                plt.savefig(path+
                    r"\samsung\television\amazonPos.png",
                    format="png")
            else:
                plt.savefig(path+
                    r"\samsung\television\amazonNeg.png",
                    format="png")


def cleaner(data):
    corpus = []
    for i in range(0, len(data)):
        review = re.sub('[^a-zA-Z]', ' ', str(data[i]))
        review = review.lower()
        review = review.split()
        all_stopwords = stopwords.words('english')
        all_stopwords.remove('not')
        review = [word for word in review if not word in set(all_stopwords)]
        review = ' '.join(review)
        corpus.append(review)
    data.dropna(inplace=True)
    text_pol = []
    for i in range(0, len(corpus)):
        text = corpus[i]
        senti = TextBlob(text)
        polarity = senti.sentiment.polarity
        if -1 <= polarity < -0.5:
            label = 'Negative'
        elif -0.5 <= polarity < -0.1:
            label = 'Negative'
        elif -0.1 <= polarity < 0.2:
            label = 'Neutral'
        elif 0.2 <= polarity < 0.6:
            label = 'Positive'
        elif 0.6 <= polarity <= 1:
            label = 'Positive'
        text_pol.append(label)
    polDf = pd.DataFrame(list(zip(corpus, text_pol)), columns=['Review', 'Polarity'])
    return polDf


# (Samsung Mobile)
def mobile(request):
    #--------------------------------------------------FLIPKART----------------------------------------------------
    flipkartData = pd.read_csv(path2+r'\samsung\mobile\newFlipkartDataset.csv')
    flipkartPosCount = flipkartData['Polarity'].value_counts()['Positive']
    flipkartNegCount = flipkartData['Polarity'].value_counts()['Negative']
    flipkartNeuCount = flipkartData['Polarity'].value_counts()['Neutral']


    # --------------------------------------------AMAZON----------------------------------------------------
    amazonDataset = pd.read_csv(path2+r'\samsung\mobile\newAmazonDataset.csv')
    amazonPosCount = amazonDataset['Polarity'].value_counts()['Positive']
    amazonNegCount = amazonDataset['Polarity'].value_counts()['Negative']
    amazonNeuCount = amazonDataset['Polarity'].value_counts()['Neutral']


    #--------------------------------------------------TWITTER--------------------------------------------------------
    twitterData = pd.read_csv(path2+r'\samsung\mobile\newTwitterDataset.csv')
    twitterPosCount = twitterData['Polarity'].value_counts()['Positive']
    twitterNegCount = twitterData['Polarity'].value_counts()['Negative']
    twitterNeuCount = twitterData['Polarity'].value_counts()['Neutral']

    # dataWordCloud()

    context = {'flipkartPosCount':flipkartPosCount,'flipkartNegCount':flipkartNegCount,'flipkartNeuCount':flipkartNeuCount
               ,'amazonPosCount':amazonPosCount,'amazonNegCount':amazonNegCount,'amazonNeuCount':amazonNeuCount,
               'twitterPosCount':twitterPosCount,'twitterNegCount':twitterNegCount,'twitterNeuCount':twitterNeuCount}

    return render(request,'mobile/samsung.html',context)

def dataWordCloud(type="mobile"):
    df = pd.read_csv(path2+r'\samsung\mobile\AllMobilesSamsung.csv', encoding='latin1')
    sp_ch = ["?", "\n", "!", "@", "SamsungIndia","READ MORE"]

    for char in sp_ch:
        df['REVIEWS'] = df['REVIEWS'].str.replace(char, '')
    df.rename(columns={'REVIEWS': 'review'}, inplace=True)
    df = df.review.str.lower()
    polDf = cleaner(df)
    data = polDf[['Review', 'Polarity']]
    train = data
    train_pos = train[train['Polarity'] == 'Positive']
    train_pos = train_pos['Review']
    train_neg = train[train['Polarity'] == 'Negative']
    train_neg = train_neg['Review']
    # train_neu = train[train['Polarity'] == 'Neutral']
    # train_neu = train_neu['Review']

    wordcloud_draw(train_pos, 'white', type="Pos")
    wordcloud_draw(train_neg,type="Neg")


def flipkart(request):
    flipkartData = pd.read_csv(path2+
        r'\samsung\mobile\newFlipkartDataset.csv')
    flipkartPosCount = flipkartData['Polarity'].value_counts()['Positive']
    flipkartNegCount = flipkartData['Polarity'].value_counts()['Negative']
    flipkartNeuCount = flipkartData['Polarity'].value_counts()['Neutral']
    displayData = flipkartData.sample(8)
    # data = flipkartData[['Review', 'Polarity']]
    # train = data
    # train_pos = train[train['Polarity'] == 'Positive']
    # train_pos = train_pos['Review']
    # train_neg = train[train['Polarity'] == 'Negative']
    # train_neg = train_neg['Review']
    # wordcloud_draw(train_pos, 'white', type="Pos",loc="flipkart")
    # wordcloud_draw(train_neg, type="Neg",loc="flipkart")

    context = {'flipkartPosCount':flipkartPosCount,'flipkartNegCount':flipkartNegCount,'flipkartNeuCount':flipkartNeuCount
               ,'displayData':displayData}

    return render(request,'mobile/flipkart.html',context)

def amazon(request):
    amazonDataset = pd.read_csv(path2+r'\samsung\mobile\newAmazonDataset.csv')
    amazonPosCount = amazonDataset['Polarity'].value_counts()['Positive']
    amazonNegCount = amazonDataset['Polarity'].value_counts()['Negative']
    amazonNeuCount = amazonDataset['Polarity'].value_counts()['Neutral']
    displayData = amazonDataset.sample(8)
    # data = amazonDataset[['Review', 'Polarity']]
    # train = data
    # train_pos = train[train['Polarity'] == 'Positive']
    # train_pos = train_pos['Review']
    # train_neg = train[train['Polarity'] == 'Negative']
    # train_neg = train_neg['Review']
    # wordcloud_draw(train_pos, 'white', type="Pos", loc="amazon")
    # wordcloud_draw(train_neg, type="Neg", loc="amazon")

    context = {'amazonPosCount': amazonPosCount, 'amazonNegCount': amazonNegCount,
               'amazonNeuCount': amazonNeuCount, 'displayData':displayData}
    return render(request , 'mobile/amazon.html', context)

def twitter(request):
    twitterData = pd.read_csv(path2+r'\samsung\mobile\newTwitterDataset.csv')
    twitterPosCount = twitterData['Polarity'].value_counts()['Positive']
    twitterNegCount = twitterData['Polarity'].value_counts()['Negative']
    twitterNeuCount = twitterData['Polarity'].value_counts()['Neutral']
    displayData = twitterData.sample(8)
    # data = twitterData[['Review', 'Polarity']]
    # train = data
    # train_pos = train[train['Polarity'] == 'Positive']
    # train_pos = train_pos['Review']
    # train_neg = train[train['Polarity'] == 'Negative']
    # train_neg = train_neg['Review']
    # wordcloud_draw(train_pos, 'white', type="Pos", loc="twitter")
    # wordcloud_draw(train_neg, type="Neg", loc="twitter")

    context = {'twitterPosCount': twitterPosCount, 'twitterNegCount': twitterNegCount,
               'twitterNeuCount': twitterNeuCount, 'displayData':displayData}
    return render(request , 'mobile/twitter.html', context)


#-------------------------------------- Samsung Television-------------------------------------
def tv(request):
    # --------------------------------------------------FLIPKART----------------------------------------------------
    flipkartData = pd.read_csv(path2+r'\samsung\television\newFlipkartTV.csv')
    flipkartPosCount = flipkartData['Polarity'].value_counts()['Positive']
    flipkartNegCount = flipkartData['Polarity'].value_counts()['Negative']
    flipkartNeuCount = flipkartData['Polarity'].value_counts()['Neutral']

    #--------------------------------------------------AMAZON--------------------------------------------------------
    amazonDataset = pd.read_csv(path2+r'\samsung\television\newAmazonTV.csv')
    amazonPosCount = amazonDataset['Polarity'].value_counts()['Positive']
    amazonNegCount = amazonDataset['Polarity'].value_counts()['Negative']
    amazonNeuCount = amazonDataset['Polarity'].value_counts()['Neutral']


    #----------------------------------------------WORDCLOUD------------------------------------------------
    # df = pd.read_csv(path2+r'\samsung\television\newMergedTV.csv')
    # data = df[['Review', 'Polarity']]
    # train = data
    # train_pos = train[train['Polarity'] == 'Positive']
    # train_pos = train_pos['Review']
    # train_neg = train[train['Polarity'] == 'Negative']
    # train_neg = train_neg['Review']
    # wordcloud_draw(train_pos, 'white', type="Pos",product="tv")
    # wordcloud_draw(train_neg, type="Neg",product="tv")


    context = {'flipkartPosCount': flipkartPosCount, 'flipkartNegCount': flipkartNegCount,
               'flipkartNeuCount': flipkartNeuCount,'amazonPosCount': amazonPosCount, 'amazonNegCount': amazonNegCount,
               'amazonNeuCount': amazonNeuCount}
    return render(request,"television/overall.html",context)


def flipkartTV(request):
    flipkartData = pd.read_csv(path2+r'\samsung\television\newFlipkartTV.csv')
    flipkartPosCount = flipkartData['Polarity'].value_counts()['Positive']
    flipkartNegCount = flipkartData['Polarity'].value_counts()['Negative']
    flipkartNeuCount = flipkartData['Polarity'].value_counts()['Neutral']
    displayData = flipkartData.sample(8)
    # data = flipkartData[['Review', 'Polarity']]
    # train = data
    # train_pos = train[train['Polarity'] == 'Positive']
    # train_pos = train_pos['Review']
    # train_neg = train[train['Polarity'] == 'Negative']
    # train_neg = train_neg['Review']
    # wordcloud_draw(train_pos, 'white', type="Pos", loc="flipkart",product="tv")
    # wordcloud_draw(train_neg, type="Neg", loc="flipkart",product="tv")

    context = {'flipkartPosCount': flipkartPosCount, 'flipkartNegCount': flipkartNegCount,
               'flipkartNeuCount': flipkartNeuCount, 'displayData' : displayData}

    return render(request,'television/flipkart.html',context)

def amazonTV(request):
    amazonDataset = pd.read_csv(path2+r'\samsung\television\newAmazonTV.csv')
    amazonPosCount = amazonDataset['Polarity'].value_counts()['Positive']
    amazonNegCount = amazonDataset['Polarity'].value_counts()['Negative']
    amazonNeuCount = amazonDataset['Polarity'].value_counts()['Neutral']
    displayData = amazonDataset.sample(8)
    # data = amazonDataset[['Review', 'Polarity']]
    # train = data
    # train_pos = train[train['Polarity'] == 'Positive']
    # train_pos = train_pos['Review']
    # train_neg = train[train['Polarity'] == 'Negative']
    # train_neg = train_neg['Review']
    # wordcloud_draw(train_pos, 'white', type="Pos", loc="amazon", product="tv")
    # wordcloud_draw(train_neg, type="Neg", loc="amazon", product="tv")

    context = {'amazonPosCount': amazonPosCount, 'amazonNegCount': amazonNegCount,
               'amazonNeuCount': amazonNeuCount, 'displayData' : displayData}

    return render(request,'television/amazon.html',context)



