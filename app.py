from flask import Flask, render_template, request, send_from_directory
import yt_dlp
import os
import uuid

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"

# samee folder haddii uusan jirin
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        url = request.form.get("url")

        if not url:
            return "No URL provided"

        video_id = str(uuid.uuid4())[:8]

        ydl_opts = {
            "outtmpl": f"{DOWNLOAD_FOLDER}/{video_id}.%(ext)s",
            "format": "best",
            "noplaylist": True
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)

            video = os.path.basename(filename)

            return render_template("video.html", video=video)

        except Exception as e:
            return f"Download error: {str(e)}"

    return render_template("index.html")


@app.route("/downloads/<path:filename>")
def download_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename)


@app.route("/downloads")
def list_downloads():

    files = os.listdir(DOWNLOAD_FOLDER)

    return render_template("downloads.html", files=files)
