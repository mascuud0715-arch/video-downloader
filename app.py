from flask import Flask, render_template, request, redirect, send_from_directory
import yt_dlp
import os
import uuid

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/download", methods=["POST"])
def download():

    url = request.form["url"]

    filename = str(uuid.uuid4()) + ".mp4"

    path = os.path.join(DOWNLOAD_FOLDER, filename)

    ydl_opts = {
        "format": "mp4",
        "outtmpl": path
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except:
        return "Download error"

    return redirect("/video/" + filename)


@app.route("/video/<filename>")
def video(filename):
    return render_template("video.html", video=filename)


@app.route("/downloads/<path:filename>")
def file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename)


@app.route("/downloads")
def downloads():

    files = os.listdir(DOWNLOAD_FOLDER)

    return render_template("downloads.html", files=files)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
