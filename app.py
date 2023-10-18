from flask import Flask, render_template, request, jsonify
from googleapiclient.discovery import build
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

# Creating Flask Server
app = Flask(__name__)

with open('models.pkl', 'rb') as model_file:
    models = pickle.load(model_file)

with open('vectorizer.pkl', 'rb') as vectorizer_file:
    tfidf_vectorizer = pickle.load(vectorizer_file)

# Function to extract youtube comments from ID

yt_link = ""

def get_youtube_comments(video_id):
    youtube = build('youtube', 'v3', developerKey='AIzaSyDKeOTZPWuLpSIHSkPPbtsxqEDF73-Nc8U')
    comments = []
    counter = 10

    next_page_token = None
    while True:
        if counter == 0:
            break
        else:
            counter = counter - 1

        results = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            textFormat="plainText",
            maxResults=100,
            pageToken=next_page_token
        ).execute()

        for item in results.get("items", []):
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(comment)

        # Check if there are more comments
        next_page_token = results.get("nextPageToken")
        if not next_page_token:
            break

    print(comments)
    return comments


@app.route('/')
def index():
    return render_template('index.html')

commentss = []

@app.route('/process_link', methods=['POST'])
def process_link():
    youtube_link = request.form.get('youtube_link')
    global yt_link
    yt_link = youtube_link
    # comments = get_youtube_comments(video_id=youtube_link)
    # print("/////////COmments Here")
    # print(comments)
    #
    # label_col = []
    # for c in comments:
    #     print("/////////C Here")
    #     print(c)
    #     float_features = [c]
    #     print(float_features)
    #     features = np.array(float_features)
    #     print(features)
    #     data_tfidf = tfidf_vectorizer.transform(features)
    #     prediction = models.predict(data_tfidf)
    #     print(prediction)
    #     label_col.append(prediction)
    #
    # # classified_comments = np.vstack((comments, label_col))
    # # print(comments)
    # # print(label_col)
    #
    # print("Hello")
    # # print(classified_comments)

    return render_template('class.html')

@app.route('/all', methods=['POST'])
def all():
    button_kaunsa = request.form['button_name']
    if(button_kaunsa=='All'):
        print(button_kaunsa)
        comments = get_youtube_comments(video_id=yt_link)
        print("/////////COmments Here")
        print(comments)

        label_col = []
        for c in comments:
            print("/////////C Here")
            print(c)
            float_features = [c]
            print(float_features)
            features = np.array(float_features)
            print(features)
            data_tfidf = tfidf_vectorizer.transform(features)
            prediction = models.predict(data_tfidf)
            print(prediction)
            label_col.append(prediction)

        # classified_comments = np.vstack((comments, label_col))
        # print(comments)
        # print(label_col)

        print("Hello")
        # print(classified_comments)

        return render_template('comments-page.html', comments=comments)

    elif(button_kaunsa=='Relevant'):
        print(button_kaunsa)
        comments = get_youtube_comments(video_id=yt_link)
        print("/////////COmments Here")
        print(comments)
        comments = np.array(comments)
        # label_col = np.empty((0,1))
        label_col = []
        cp = []
        for c in comments:
            cp.append([c])
            print("/////////C Here")
            print(c)
            float_features = [c]
            print(float_features)
            features = np.array(float_features)
            print(features)
            data_tfidf = tfidf_vectorizer.transform(features)
            prediction = models.predict(data_tfidf)
            print(prediction)
            label_col.append(prediction)

        label_array = np.array(label_col)

        cp = np.array(cp)
        ache_comments = cp[label_array == 0]

        # classified_comments = np.vstack((comments, label_col))
        # print(comments)
        # print(label_col)

        print("Hello")
        # print(classified_comments)

        return render_template('comments-page.html', comments=ache_comments)
    elif (button_kaunsa == 'Spam'):
        print(button_kaunsa)
        comments = get_youtube_comments(video_id=yt_link)
        print("/////////COmments Here")
        print(comments)
        comments = np.array(comments)
        # label_col = np.empty((0,1))
        label_col = []
        cp = []
        for c in comments:
            cp.append([c])
            print("/////////C Here")
            print(c)
            float_features = [c]
            print(float_features)
            features = np.array(float_features)
            print(features)
            data_tfidf = tfidf_vectorizer.transform(features)
            prediction = models.predict(data_tfidf)
            print(prediction)
            label_col.append(prediction)

        label_array = np.array(label_col)

        cp = np.array(cp)
        bure_comments = cp[label_array == 1]

        # classified_comments = np.vstack((comments, label_col))
        # print(comments)
        # print(label_col)

        print("Hello")
        # print(classified_comments)

        return render_template('comments-page.html', comments=bure_comments)

if __name__ == '__main__':
    app.run(debug=True)

