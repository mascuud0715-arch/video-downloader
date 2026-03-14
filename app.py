import os
import json
import requests
from datetime import datetime
from flask import Flask, render_template, request

app = Flask(__name__)

# ================= FILES =================

HISTORY_FILE = "history.json"

if not os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "w") as f:
        json.dump([], f)


# ================= HOME =================

@app.route("/")
def home():
    return render_template("index.html")


# ================= DOWNLOAD =================

@app.route("/download", methods=["POST"])
def download():

    url = request.form.get("url")

    if not url:
        return "Please paste TikTok link"

    api = f"https://tikwm.com/api/?url={url}"

    r = requests.get(api).json()

    video = r["data"]["play"]
    title = r["data"]["title"]
    thumbnail = r["data"]["cover"]

    save_history(url, title, thumbnail, video)

    return render_template(
        "video.html",
        video=video,
        title=title,
        thumbnail=thumbnail
    )


# ================= SAVE HISTORY =================

def save_history(url, title, thumbnail, video):

    with open(HISTORY_FILE) as f:
        data = json.load(f)

    data.insert(0, {
        "url": url,
        "title": title,
        "thumbnail": thumbnail,
        "video": video,
        "time": datetime.now().strftime("%I:%M %p")
    })

    with open(HISTORY_FILE, "w") as f:
        json.dump(data, f)


# ================= DOWNLOADS PAGE =================

@app.route("/downloads")
def downloads():

    with open(HISTORY_FILE) as f:
        data = json.load(f)

    return render_template("downloads.html", data=data)


# ================= RUN =================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
