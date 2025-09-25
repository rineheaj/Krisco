from flask import Flask, render_template, request, redirect, url_for, jsonify
from pathlib import Path
from datetime import datetime, timedelta
import json
import os

from github_file_services import (
    save_guestbook_github,
    read_guestbook_github,
    save_guestbook_github_json,
    read_guestbook_json_github,
)

app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = timedelta(days=2)

IMAGES_FOLDER = Path(__file__).parent / "static" / "images"
GUEST_BOOK = Path(__file__).parent / "data" / "guestbook.txt"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/gallery")
def gallery():
    imgs = [img.name for img in IMAGES_FOLDER.iterdir() if img.suffix.endswith(".jpg")]
    return render_template("gallery.html", imgs=imgs)


# @app.route("/story")
# def story():
#     return render_template("story.html")


# @app.route("/messages")
# def messages():
#     return render_template("messages.html")


@app.route("/guestbook_local_json", methods=["GET", "POST"])
def guestbook_local_json():
    filepath = "data/guestbook.json"
    if not os.path.exists(filepath):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, mode="w", encoding="utf-8") as outfile:
            json.dump([], outfile)

    if request.method == "POST":
        name = request.form.get("name")
        message = request.form.get("message")
        if name and message:
            new_entry = {
                "timestamp": datetime.now().strftime("%m-%d-%Y %H:%M:%S"),
                "name": name,
                "message": message,
            }
            with open(filepath, mode="r", encoding="utf-8") as infile:
                entries = json.load(infile)
            entries.append(new_entry)

            try:
                with open(filepath, mode="w", encoding="utf-8") as outfile:
                    json.dump(entries, outfile, indent=2)
                print(f"✅ Saved json to {filepath}")
            except Exception as e:
                print(f"⚠️ Could not save local guestbook.json {e}")

            return redirect(url_for("guestbook_local_json"))

    # GET REQUEST
    with open("data/guestbook.json", mode="r", encoding="utf-8") as infile:
        entries = json.load(infile)
    entries = list(reversed(entries))

    if not entries:
        print("❌ No entries in json guestbook")
    else:
        for entry in entries:
            print(f"🟢 {entry}")

    return render_template("guestbook.html", entries=entries)


@app.route("/guestbook_json", methods=["GET", "POST"])
def guestbook_json():
    if request.method == "POST":
        name = request.form.get("name")
        message = request.form.get("message")
        if name and message:
            try:
                save_guestbook_github_json(name, message)
            except Exception as e:
                print(f"⚠️ Failed to save to GitHub: {e}")
            return redirect(url_for("guestbook_json"))

    entries = read_guestbook_json_github()
    for e in entries:
        print(f"🟢 {e}")
    return render_template("guestbook.html", entries=entries)


@app.route("/guestbook", methods=["GET", "POST"])
def guestbook():
    if request.method == "POST":
        name = request.form.get("name")
        message = request.form.get("message")
        safe_message = message.replace("\n", " \\n ")
        if name and message:
            try:
                save_guestbook_github(name=name, message=safe_message)
            except Exception as e:
                print(f"⚠️ Failed to save to GitHub: {e}")
                entry = f"{datetime.now().strftime('%m-%d-%Y %H:%M:%S')} | {name}: {safe_message}\n"
                GUEST_BOOK.parent.mkdir(parents=True, exist_ok=True)
                with open(GUEST_BOOK, mode="a", encoding="utf-8") as outfile:
                    outfile.write(entry)
                print(f"Guestbook saved locally to {outfile}")

        return redirect(url_for("guestbook"))

    # GET REQUEST PART
    entries = read_guestbook_github()
    if not entries and GUEST_BOOK.exists():
        with open(GUEST_BOOK, mode="r", encoding="utf-8") as infile:
            entries = list(reversed(infile.readlines()))

    formmed_entries = []
    for e in entries:
        target_name = e.split(" | ")[1].split(":")[0].strip()
        target_message = e.split(" | ")[1].split(":")[1].strip()
        formmed_entries.append({"name": target_name, "message": target_message})

    return render_template("guestbook.html", entries=formmed_entries)


@app.route("/.well-known/appspecific/com.chrome.devtools.json")
def devtools():
    ua = request.headers.get("User-Agent", "HUH AGENT").lower()
    print(ua)
    if "chrome" in ua:
        return "", 204
    else:
        return jsonify(
            {
                "status_code": 200,
                "response_text": "Running in a local environment. This endpoint is for Chrome DevTools.",
            }
        ), 200


if __name__ == "__main__":
    app.run(debug=True)
