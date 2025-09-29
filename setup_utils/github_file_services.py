from github import Github, GithubException
from werkzeug.utils import secure_filename
import base64
import os
from datetime import datetime
import json


def save_guestbook_github(name, message):
    g = Github(os.getenv("GITHUB_TOKEN"))
    repo = g.get_repo(os.getenv("GITHUB_REPO"))
    branch = os.environ.get("GITHUB_BRANCH", "main")

    try:
        contents = repo.get_contents("data/guestbook.txt", ref=branch)
        old_text = contents.decoded_content.decode("utf-8")
        sha = contents.sha
    except Exception as e:
        old_text = ""
        sha = None
        print(f"Error saving guestbook.txt file: {e}")

    entry = entry = (
        f"{datetime.now().strftime('%m-%d-%Y %H:%M:%S')} | {name}: {message}\n"
    )
    new_text = old_text + entry

    if sha:
        repo.update_file(
            path="data/guestbook.txt",
            message=f"Add guestbook entry by {name}",
            content=new_text,
            sha=sha,
            branch=branch,
        )
    else:
        repo.create_file(
            path="data/guestbook.txt",
            message=f"Create guestbook.txt with first entry by {name}",
            branch=branch,
        )


def read_guestbook_github():
    g = Github(os.getenv("GITHUB_TOKEN"))
    repo_name = os.getenv("GITHUB_REPO")
    brnach = os.getenv("GITHUB_BRANCH", "main")
    repo = g.get_repo(repo_name)

    try:
        contents = repo.get_contents("data/guestbook.txt", ref=brnach)
        text = contents.decoded_content.decode("utf-8")
        return list(reversed(text.splitlines()))
    except GithubException as e:
        print(f"⚠️ Github error: {e}")
        return []
    except Exception as e:
        print(f"Error in read guestbook: {e}\nReturning empty list.")
        return []


def save_guestbook_github_json(name, message):
    g = Github(os.getenv("GITHUB_TOKEN"))
    repo_name = os.getenv("GITHUB_REPO")
    branch = os.getenv("GITHUB_BRANCH", "main")
    repo = g.get_repo(repo_name)

    entry = {
        "timestamp": datetime.now().strftime("%m-%d-%Y %H:%M:%S"),
        "name": name,
        "message": message,
    }

    try:
        contents = repo.get_contents("data/guestbook.json", ref=branch)
        old_data = json.loads(contents.decoded_content.decode("utf-8"))
        sha = contents.sha
    except GithubException as e:
        old_data = []
        sha = None
        print(f"Github Error while saving json: {e}")
    except Exception as e:
        print(f"ERROR while saving json to github: {e}")
        old_data = []
        sha = None

    old_data.append(entry)
    new_text = json.dumps(old_data, ensure_ascii=False, indent=2)

    if sha:
        repo.update_file(
            path="data/guestbook.json",
            message=f"Add guestbook entry by {name}",
            content=new_text,
            sha=sha,
            branch=branch,
        )
    else:
        repo.create_file(
            path="data/guestbook.json",
            message=f"Create guestbook.txt with first entry by {name}",
            content=new_text,
            branch=branch,
        )


def read_guestbook_json_github():
    g = Github(os.getenv("GITHUB_TOKEN"))
    repo_name = os.getenv("GITHUB_REPO")
    branch = os.getenv("GITHUB_BRANCH", "main")
    repo = g.get_repo(repo_name)

    try:
        contents = repo.get_contents("data/guestbook.json", ref=branch)
        data = json.loads(contents.decoded_content.decode("utf-8"))
        return list(reversed(data))
    except GithubException as e:
        print(f"⚠️ Error reading json from Github: {e}")
        return []
    except Exception as e:
        print(f"⚠️ General error while reading file from Github: {e}")
        return []


def save_uploaded_image_to_github(file_storage, filename=None):
    g = Github(os.getenv("GITHUB_TOKEN"))
    repo_name = os.getenv("GITHUB_REPO")
    branch = os.getenv("GITHUB_BRANCH", "main")
    repo = g.get_repo(repo_name)

    if not filename:
        filename = secure_filename(file_storage.filename)
    
    path = f"static/uploads/{filename}"

    file_bytes = file_storage.read()
    encoded_content = base64.b64encode(file_bytes).decode("ascii")

    try:
        contents = repo.get_contents(path, ref=branch)
        sha = contents.sha
        repo.update_file(
            path=path,
            message=f"Update uploaded image {filename}",
            content=encoded_content,
            sha=sha,
            branch=branch,
        )
    except GithubException as e:
        print(f"❌ Could not find file to update on GitHub, creating a new one. Error message on the next line.\n{e}")
        repo.create_file(
            path=path,
            message=f"Add uploaded image {filename}",
            content=encoded_content,
            branch=branch,
        )
    
    file_storage.stream.seek(0)

    return path


