import os
import sys
from github import Github, Auth # PyGithub library dependency, install with `pip install PyGithub`
from operator import itemgetter
import json

TOKEN = os.environ["GITHUB_TOKEN"]          # Personal Access Token
TARGET_REPO = os.environ["TARGET_REPO"]     # e.g. "octocat/my-special-repo"
SKIP_REPO_LIST = ["AdvancedPythonMasterCourse"]
DATA_PATH = ".github/scripts/resources/data.json"
DATA_PCT_PATH = ".github/scripts/resources/data_pct.json"

def get_repos():
    auth = Auth.Token(TOKEN)
    github = Github(auth=auth)
    user = github.get_user()
    repos = user.get_repos(type="public")
    lang_bytes: dict[str, int] = {}
    total_bytes = 0
    to_json = {}

    # --- Language bytes: pickle-cached so we only hit the API once ---
    for repo in repos:
        if repo.name in SKIP_REPO_LIST:
            continue
        lang_bytes = {}
        total_bytes = 0
        langs = repo.get_languages()  # API call – only on first run
        for lang, b in langs.items():
            if not isinstance(b, int):
                continue
            lang_bytes[lang] = lang_bytes.get(lang, 0) + b
            total_bytes += b
        lang_info = {}
        for lang, b in sorted(lang_bytes.items(), key=itemgetter(1), reverse=True):
            pct = round((b / total_bytes) * 100, 2) if total_bytes else 0
            lang_info[lang] = (pct,b)
        to_json[repo.name] = lang_info
    with open(DATA_PATH,"w") as jsonf:
        json.dump(to_json,jsonf,indent=4)

def get_languages_repo_info():
    all_lang = {}
    with open(DATA_PATH,"r") as jsonfile:
        file = json.load(jsonfile)
    for _,languages in file.items():
        for lang,bytes_ in languages.items():
            if(lang in all_lang):
                all_lang[lang] += bytes_[1]
            else:
                all_lang[lang] = bytes_[1]

    total_bytes = sum(all_lang.values())
    to_pct_file = {}
    to_pct_file["others"] = 0
    for language,bytes__ in all_lang.items():
        pct = round((bytes__ / total_bytes) * 100, 2) if total_bytes else 0 
        if(pct < 0.1):
            to_pct_file["others"] += pct
            continue
        to_pct_file[language] = pct

    with open(DATA_PCT_PATH,"w") as pct_file:
        json.dump(to_pct_file,pct_file,indent=4)

if __name__ == "__main__":
    try:
        get_repos()
        print("Get repos successfully")
    except Exception as e:
        print("Error while getting GitHub repos")
        sys.exit(1)
    try:
        get_languages_repo_info()
        print("Get languages repos successfully")
    except Exception as e:
        print("Error while getting lenguages repo info")
        sys.exit(1)