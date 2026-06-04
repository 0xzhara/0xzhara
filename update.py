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

# Update Featured Projects section
projects_lines = []
for repo in top_repos:
    name = repo["name"]
    desc = repo.get("description") or "No description"
    stars_repo = repo.get("stargazers_count", 0)
    url = repo["html_url"]
    projects_lines.append(f"| [{name}]({url}) | {desc} | ⭐ {stars_repo} |")

projects_table = "\n".join(projects_lines)

# Replace Featured Projects table rows
projects_pattern = r"(\| Project \| Description \| Stars \|\n\|[-|]+\|\n)(.*?)(\n\n</div>)"
if re.search(projects_pattern, readme, re.DOTALL):
    readme = re.sub(
        projects_pattern,
        r"\1" + projects_table + r"\3",
        readme,
        flags=re.DOTALL,
    )

# Add/update dynamic stats comment block at the end
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
else:
    # Append before the final footer
    if "<i>⚡ Updated automatically" in readme:
        readme = readme.replace(
            "<i>⚡ Updated automatically by GitHub Actions</i>",
            stats_block + "\n\n<i>⚡ Updated automatically by GitHub Actions</i>",
        )
    else:
        readme += "\n\n" + stats_block

with open(readme_path, "w") as f:
    f.write(readme)

print(f"✅ README updated — {followers} followers, {public_repos} repos, {stars} stars")
