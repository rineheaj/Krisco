from github import Github
import os
from datetime import datetime



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
    
    entry = entry = f"{datetime.now().strftime('%m-%d-%Y %H:%M:%S')} | {name}: {message}\n"
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
    repo = g.get_repo("GITHUB_REPO")
    brnach = os.getenv("GITHUB_BRANCH", "main")
    try:
        contents = repo.get_contents("data/guestbook.txt", ref=brnach)
        text = contents.decoded_content.decode("utf-8")
        return list(reversed(text.splitlines()))
    except Exception as e:
        print(f"Error in read guestbook: {e}\nReturning empty list.")
        return []
    
    