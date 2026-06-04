import requests
import re
import os
import datetime

USERNAME = "0xzhara"
TOKEN = os.environ.get("GITHUB_TOKEN", "")

headers = {}
if TOKEN:
    headers["Authorization"] = f"token {TOKEN}"

# Fetch GitHub user data
user_url = f"https://api.github.com/users/{USERNAME}"
repos_url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100"

user_data = requests.get(user_url, headers=headers).json()
repos_data = requests.get(repos_url, headers=headers).json()

followers = user_data.get("followers", 0)
following = user_data.get("following", 0)
public_repos = user_data.get("public_repos", 0)
stars = sum(repo.get("stargazers_count", 0) for repo in repos_data)

# Top repos by stars
top_repos = sorted(
    repos_data, key=lambda r: r.get("stargazers_count", 0), reverse=True
)[:3]

# Timestamp
now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

# Read existing README
readme_path = "README.md"
with open(readme_path, "r") as f:
    readme = f.read()

# Update Featured Projects — replace pin cards
project_cards = []
for repo in top_repos:
    name = repo["name"]
    url = repo["html_url"]
    project_cards.append(
        f'<a href="{url}">\n'
        f'  <img align="center" src="https://github-readme-stats.vercel.app/api/pin/?username={USERNAME}&repo={name}&theme=tokyonight&hide_border=true&bg_color=0d1117&title_color=7aa2f7&icon_color=bb9af7&text_color=c0caf5" />\n'
        f'</a>'
    )
cards_html = "\n".join(project_cards)

# Replace between FEATURED PROJECTS markers
projects_pattern = r"(<!-- PROJECT CARDS -->\n)(.*?)(\n\n</div>)"
if re.search(projects_pattern, readme, re.DOTALL):
    readme = re.sub(projects_pattern, r"\1" + cards_html + r"\3", readme, flags=re.DOTALL)

# Update dynamic stats block
stats_block = f"""<!-- DYNAMIC_STATS:DO_NOT_EDIT -->
<div align="center">

📊 **Followers:** {followers} &nbsp;|&nbsp; **Following:** {following} &nbsp;|&nbsp; **Repos:** {public_repos} &nbsp;|&nbsp; **Stars:** {stars}

<i>Last updated: {now}</i>

</div>
<!-- /DYNAMIC_STATS -->"""

if "<!-- DYNAMIC_STATS:DO_NOT_EDIT -->" in readme:
    readme = re.sub(
        r"<!-- DYNAMIC_STATS:DO_NOT_EDIT -->.*?<!-- /DYNAMIC_STATS -->",
        stats_block,
        readme,
        flags=re.DOTALL,
    )

with open(readme_path, "w") as f:
    f.write(readme)

print(f"✅ README updated — {followers} followers, {public_repos} repos, {stars} stars")
