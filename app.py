from flask import Flask, render_template, request, send_from_directory
import yt_dlp
import os

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)


@app.route("/", methods=["GET","POST"])
def home():

    if request.method == "POST":

        url = request.form.get("url")

        ydl_opts = {
            "outtmpl": f"{DOWNLOAD_FOLDER}/video.%(ext)s",
            "format": "best"
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)

            video = os.path.basename(filename)

            return render_template("video.html", video=video)

        except Exception as e:
            return str(e)

    return render_template("index.html")


@app.route("/downloads/<path:filename>")
def download_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename)


port = int(os.environ.get("PORT", 8080))

app.run(host="0.0.0.0", port=port)
