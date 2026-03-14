import os
import uuid
from flask import Flask, render_template, request, send_from_directory
import yt_dlp

app = Flask(__name__)

# Folder videos lagu kaydiyo
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Download video
@app.route("/download", methods=["POST"])
def download():

    url = request.form.get("url")

    if not url:
        return "Link geli"

    video_id = str(uuid.uuid4())[:8]
    filename = f"{video_id}.mp4"
    filepath = os.path.join(DOWNLOAD_FOLDER, filename)

    ydl_opts = {
        "outtmpl": filepath,
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        "quiet": True,
        "noplaylist": True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

            title = info.get("title")
            thumbnail = info.get("thumbnail")

    except Exception as e:
        return f"Download error: {e}"

    return render_template(
        "video.html",
        filename=filename,
        title=title,
        thumbnail=thumbnail
    )


# Video serve
@app.route("/downloads/<filename>")
def downloads(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
