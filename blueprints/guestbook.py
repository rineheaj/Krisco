from datetime import datetime
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
)
from flask_login import (
    login_required
)
from setup_utils.github_file_services import (
    save_guestbook_github,
    read_guestbook_github,
)
from setup_utils.constants import (
    GUEST_BOOK,
)
import threading


guestbook_bp = Blueprint("guestbook", __name__, url_prefix="/guestbook")

def async_save_to_github(name: str, message: str):
    def task():
        print(f"⌛ Background save started for {name}")
        try:
            save_guestbook_github(name=name, message=message)
            print(f"✅ Saved to GitHub: {name}")
        except Exception as e:
            print(f"⚠️ Background GitHub save failed: {e}")
        
    threading.Thread(target=task, daemon=True).start()



def sanitize_message(message: str | None) -> str | None:
    if not message:
        return None
    return message.replace("\n", " \\n ").strip()



@guestbook_bp.route("/", methods=["GET", "POST"])
@login_required
def guestbook():
    if request.method == "POST":
        name = request.form.get("name")
        safe_message = sanitize_message(request.form.get("message"))

        if name and safe_message:
            entry = f"{datetime.now().strftime('%m-%d-%Y %H:%M:%S')} | {name}: {safe_message}\n"
            GUEST_BOOK.parent.mkdir(parents=True, exist_ok=True)
            with open(GUEST_BOOK, mode="a", encoding="utf-8") as outfile:
                outfile.write(entry)
            print(f"Guestbook saved locally to {outfile}")
            async_save_to_github(name, safe_message)

    #GET request part
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

    # 🔑 If SPA request, return updated page directly
    if request.headers.get("X-Requested-With") == "fetch":
        return render_template("guestbook.html", entries=formatted_entries)

    return render_template("guestbook.html", entries=formatted_entries)




