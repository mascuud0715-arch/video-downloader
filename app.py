from flask import Flask, render_template, request, redirect, url_for
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
            "outtmpl": f"{DOWNLOAD_FOLDER}/%(title)s.%(ext)s",
            "format": "best"
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            return redirect("/downloads")

        except Exception as e:
            return str(e)

    return render_template("index.html")


@app.route("/downloads")
def downloads():

    files = os.listdir(DOWNLOAD_FOLDER)

    return render_template("downloads.html", files=files)


@app.route("/download/<name>")
def download(name):

    return redirect(f"/downloads/{name}")


port = int(os.environ.get("PORT",8080))

app.run(host="0.0.0.0",port=port)
