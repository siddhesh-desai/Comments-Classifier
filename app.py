from flask import Flask, render_template, request
from googleapiclient.discovery import build
import re

# Creating Flask Server
app = Flask(__name__)


# Convert YT video link into ID
def get_youtube_video_id(link):
    regex = r"(?<=v=|v\/|vi\/|vi=|youtu.be\/|/embed/|/v/|/e/|watch\?v=|watch\?feature=player_embed&v=|embed\/)([" \
            r"a-zA-Z0-9_-]+) "
    match = re.search(regex, link)

    if match:
        video_id = match.group(1)
        return video_id
    else:
        return None


# Function to extract youtube comments from ID


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


@app.route('/process_link', methods=['POST'])
def process_link():
    youtube_link = request.form.get('youtube_link')
    comments = get_youtube_comments(video_id=get_youtube_video_id(youtube_link))
    return render_template('comments-page.html', comments=comments)


if __name__ == '__main__':
    app.run(debug=True)
