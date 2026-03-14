from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def home():

    if request.method == "POST":

        url = request.form.get("url")

        try:
            ydl_opts = {
                "format": "best",
                "outtmpl": "video.%(ext)s"
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                file = ydl.prepare_filename(info)

            return send_file(file, as_attachment=True)

        except Exception as e:
            return f"Error: {e}"

    return render_template("index.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
