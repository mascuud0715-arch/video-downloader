import os
import uuid
from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import yt_dlp

app = Flask(__name__)

# ================= SETTINGS =================
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# ================= HOME =================
@app.route("/")
def index():
    return render_template("index.html")

# ================= DOWNLOAD =================
@app.route("/download", methods=["POST"])
def download():

    url = request.form.get("url")

    if not url:
        return redirect(url_for("index"))

    video_id = str(uuid.uuid4())[:10]
    filename = f"{video_id}.mp4"
    filepath = os.path.join(DOWNLOAD_FOLDER, filename)

    ydl_opts = {
        "outtmpl": filepath,
        "format": "mp4",
        "quiet": True,
        "noplaylist": True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        return f"Download Error: {e}"

    return render_template("video.html", filename=filename)

# ================= VIDEO PREVIEW =================
@app.route("/video/<filename>")
def video(filename):
    return render_template("video.html", filename=filename)

# ================= SERVE VIDEO =================
@app.route("/downloads/<filename>")
def downloads(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename)

# ================= LIST DOWNLOADS =================
@app.route("/all-downloads")
def all_downloads():
    files = os.listdir(DOWNLOAD_FOLDER)
    return render_template("downloads.html", files=files)

# ================= RUN LOCAL =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
