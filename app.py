from flask import Flask, render_template, request
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

            video = filename.split("/")[-1]

            return render_template("video.html", video=video)

        except Exception as e:
            return str(e)

    return render_template("index.html")


@app.route("/downloads/<file>")
def downloads(file):
    return app.send_static_file(f"../downloads/{file}")


port = int(os.environ.get("PORT",8080))

app.run(host="0.0.0.0",port=port)
