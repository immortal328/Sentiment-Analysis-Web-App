from file import to_pickle, fetch_data
from vader_sentiment import sentiment_score, lexicon_retings, result_analysis
import pickle
from flask import Flask, render_template, request, url_for
import pandas as pd
#####

import scrapy
from scrapy.crawler import CrawlerProcess
import scrapy.crawler as crawler
from multiprocessing import Process, Queue
from twisted.internet import reactor
from FlipkartReviews.FlipkartReviews.spiders.FlipkartSpider import *
from model_sentiment import load_model, load_tokenizer, get_review_prediction

model = load_model()
tokenizer = load_tokenizer()


#process = CrawlerProcess()
app = Flask(__name__)


# Home
@app.route("/", methods=['GET', 'POST'])
def SentimentHome():
    return render_template('sentiment_home.html')


# Prediction
@app.route("/predict", methods=['GET', 'POST'])
def SentimentPredict():
    text = request.form['text']
    to_pickle(text)
    sentiment, score = sentiment_score(text)
    return render_template('sentiment_predict.html', sentiment=sentiment, score=score)


'''
@app.route("/file_input")
def FileInput():
    return render_template('file_input.html')
'''

# To display disabled input


@app.route("/submitted")
def SentimentSubmit():
    return render_template('sentiment_predict.html')


# Visualisation
@app.route('/column', methods=['GET', 'POST'])
def Column(chartID='chart_ID', chart_type='column', chart_height=500):

    chart = {"renderTo": chartID,
             "type": chart_type,
             "height": chart_height
             }
    series = lexicon_retings()
    title = {"text": 'Lexicon Ratings'}
    xAxis = {"title": {"text": 'Words'}, "categories": ['']}
    yAxis = {"title": {"text": 'Lexicon Rating'}}
    return render_template('column.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)


@app.route('/line', methods=['GET', 'POST'])
def Line(chartID='chart_ID', chart_type='line', chart_height=500):
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height, }
    words, results = result_analysis()
    series = [{"name": 'Polarity', "data": results}]
    title = {"text": 'My Title'}
    title = {"text": 'Result Analysis'}
    xAxis = {"categories": words}
    yAxis = {"title": {"text": 'Polarity'}}
    return render_template('line.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)


############################################################################################
############################################################################################
############################################################################################
############################################################################################
############################################################################################
############################################################################################

@app.route("/reviews", methods=['GET', 'POST'])
def ReviewHome():
    return render_template('review_home.html')


@app.route("/predict_review", methods=['GET', 'POST'])
def ReviewPredict():
    url = request.form['text']
    # url = https://www.flipkart.com/dear-stranger-know-you-feel-journey-hope-healing/p/itm47dc1fa34daa0?pid=9789388754798&lid=LSTBOK9789388754798D1MDRQ&marketplace=FLIPKART&srno=s_1_1&otracker=search&otracker1=search&fm=SEARCH&iid=d11c11d2-ea24-40de-b8ae-c516e7070177.9789388754798.SEARCH&ppt=sp&ppn=sp&ssid=vsjx8vl7cg0000001586942952585&qH=7d8949bcbf85067f
    file = open(r"url.txt", "w")
    file.write(url)
    file.close()
    from FlipkartReviews.FlipkartReviews.spiders.FlipkartSpider import run_spider
    run_spider(FlipkartSpider)

    total, positive, negative = get_review_prediction(model, tokenizer)

    return render_template('review_predict.html', total=total, positive=positive, negative=negative)


@app.route("/show_review", methods=['GET', 'POST'])
def ReviewAll():
    df = pd.read_csv('dataframe.csv', sep='|')
    index = df.index + 1
    df = df.set_index(index)
    return render_template('review_all.html',  tables=[df.to_html(classes='data')], titles=['na', 'Reviews'])


@app.route("/review_submitted")
def ReviewSubmit():
    return render_template('review_predict.html')


if __name__ == '__main__':
    app.run(debug=True)
