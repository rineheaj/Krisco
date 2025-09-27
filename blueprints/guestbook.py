from datetime import datetime
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for
)
from setup_utils.github_file_services import (
    save_guestbook_github,
    read_guestbook_github
)
from pathlib import Path


guestbook_bp = Blueprint("guestbook", __name__, url_prefix="/guestbook")


GUEST_BOOK = Path(__file__).parent / "data" / "guestbook.txt"


@guestbook_bp.route("/", methods=["GET", "POST"])
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

        return redirect(url_for("guestbook.guestbook"))

    # GET request part no else block needed
    entries = read_guestbook_github()
    if not entries and GUEST_BOOK.exists():
        with open(GUEST_BOOK, mode="r", encoding="utf-8") as infile:
            entries = list(reversed(infile.readlines()))

    formatted_entries = []
    for e in entries:
        try:
            target_name = e.split(" | ")[1].split(":")[0].strip()
            target_message = e.split(" | ")[1].split(":")[1].strip()
            formatted_entries.append({"name": target_name, "message": target_message})
        except Exception:
            continue

    return render_template("guestbook.html", entries=formatted_entries)
