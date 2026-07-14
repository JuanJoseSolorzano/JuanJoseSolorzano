import os
import pickle
from github import Github # PyGithub library dependency, install with `pip install PyGithub`
from operator import itemgetter

TOKEN = os.environ["GITHUB_TOKEN"]          # Personal Access Token
TARGET_REPO = os.environ["TARGET_REPO"]     # e.g. "octocat/my-special-repo"
SEPARATOR_TAG = "<details>\n<summary>{0}</summary>\n\n{1}\n\n</details>\n"

def get_repos():
    """
    Fetch the list of repos you want to show.
    This example returns all public repos of the authenticated user.
    Replace this function with any GitHub API query you need.
    """
    #g = Github(TOKEN)
    #user = g.get_user()
    #repos = user.get_repos(type="public")
    # Uncomment to refresh pickle caches after adding new repos:
    #pickle.dump(user, open("user.pkl", "wb"))
    #pickle.dump(repos, open("repos.pkl", "wb"))
    #user = pickle.load(open("user.pkl", "rb"))
    repos = pickle.load(open("repos.pkl", "rb"))

    lines_temp = []
    language_repos_info = {}
    repo_info_list: dict[str, list[str]] = {}
    lang_bytes: dict[str, int] = {}
    lang_list: list[dict[str,int]] = []
    total_bytes = 0

    # --- Language bytes: pickle-cached so we only hit the API once ---
    for repo in repos:
        if repo.name == "AdvancedPythonMasterCourse":
            continue
        language_repo = []
        lang_list = []
        lang_bytes = {}
        total_bytes = 0
        langs = repo.get_languages()  # API call – only on first run
        for lang, b in langs.items():
            if not isinstance(b, int):
                continue
            lang_bytes[lang] = lang_bytes.get(lang, 0) + b
            total_bytes += b
        lang_dict = dict(lang_bytes)
        lang_list.append(lang_dict)
        lang = repo.language if repo.language else "Other"
        language_repo = " | ".join(lang_dict.keys())
        print("------------------------------------------------")
        print(f"REPO: {repo.name}")
        for lang, b in sorted(lang_bytes.items(), key=itemgetter(1), reverse=True):
            pct = round((b / total_bytes) * 100, 2) if total_bytes else 0
            print(f"\t-{lang}: {b:,} bytes ({pct}%)")
        repo_info_list.setdefault(lang, []).append(
            f"- [{repo.name}]({repo.html_url})"
        )
        language_repos_info[lang] = language_repo

    # --- Build markdown sections sorted by language name ---
    for language in sorted(repo_info_list):
        lines_temp.append(
            SEPARATOR_TAG.format(f"{language} - [{language_repos_info[language]}] ", 
                                 "\n".join(repo_info_list[language]))
        )

    # --- Print language stats ---
   

    return lines_temp

def build_markdown(repo_lines):
    header = f"# 🌐 All Perfil Information\n\n**Total:** {len(repo_lines)}\n\n"
    body = ""
    for line in sorted(repo_lines):
        body += line + "\n"
    #body = "\n".join(sorted(repo_lines)) if repo_lines else "No repos yet."
    footer = "\n\n---\n*Auto-updated every hour by GitHub Actions*"
    return header + body + footer

def update_readme(content):
    #g = Github(TOKEN)
    #repo = g.get_repo(TARGET_REPO)
    #path = "README.md"
    with open("_README.md", "w", encoding="utf-8") as f:
        f.write(content)
    #try:
    #    # If README exists, update it (needs its SHA)
    #    existing = repo.get_contents(path)
    #    repo.update_file(path, "🔄 Auto-update repo list", content, existing.sha, branch="master")
    #except:
    #    # Otherwise create it
    #    repo.create_file(path, "📝 Create README with repo list", content, branch="master")

if __name__ == "__main__":
    lines = get_repos()
    md = build_markdown(lines)
    update_readme(md)
    print(f"README updated with {len(lines)} repos.")