from flask import Flask, render_template, request, send_from_directory
import yt_dlp
import os
import uuid

if not os.path.exists("downloads"):
    os.makedirs("downloads")

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/download", methods=["POST"])
def download():

    url = request.form.get("url")

    video_id = str(uuid.uuid4())
    filename = f"{video_id}.mp4"
    filepath = os.path.join(DOWNLOAD_FOLDER, filename)

    ydl_opts = {
        'outtmpl': filepath,
        'format': 'mp4'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        return f"Error: {e}"

    return render_template("video.html", filename=filename)


@app.route("/downloads/<filename>")
def serve_video(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
