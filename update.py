import requests
import datetime
import os

USERNAME = "0xzhara"
TOKEN = os.getenv("GITHUB_TOKEN")

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

# Top 3 repos by stars
top_repos = sorted(
    repos_data, key=lambda r: r.get("stargazers_count", 0), reverse=True
)[:3]

# Timestamp
now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

# Generate README.md
with open("README.md", "w") as f:
    f.write(f"<h1 align='center'>👋 Hi, I'm {USERNAME}</h1>\n\n")
    f.write("<p align='center'>📊 Auto-updated personal GitHub dashboard</p>\n\n")
    f.write(f"<p align='center'><i>Last updated: <b>{now}</b></i></p>\n\n")

    # Stats
    f.write("## 📈 My Stats\n")
    f.write(f"- 👥 Followers: **{followers}**\n")
    f.write(f"- 🧑‍🤝‍🧑 Following: **{following}**\n")
    f.write(f"- 📂 Public Repos: **{public_repos}**\n")
    f.write(f"- ⭐ Stars (all repos): **{stars}**\n\n")

    # GitHub Analytics Cards
    f.write("## 🚀 GitHub Analytics\n")
    f.write(f"![](https://github-readme-stats.vercel.app/api?username={USERNAME}&show_icons=true&theme=tokyonight&hide_border=true)\n\n")
    f.write(f"![](https://github-readme-stats.vercel.app/api/top-langs/?username={USERNAME}&layout=compact&theme=tokyonight&hide_border=true)\n\n")
    f.write(f"![](https://github-readme-streak-stats.herokuapp.com/?user={USERNAME}&theme=tokyonight&hide_border=true)\n\n")

    # Pinned Projects
    f.write("## 📌 Pinned Projects\n")
    for repo in top_repos:
        name = repo["name"]
        desc = repo["description"] or "No description"
        stars_repo = repo["stargazers_count"]
        url = repo["html_url"]
        f.write(f"- [{name}]({url}) ⭐ {stars_repo}\n  - {desc}\n")
    f.write("\n")

    # Contribution Snake
    f.write("## 🐍 Contribution Snake\n")
    f.write("![snake gif](https://github.com/0xzhara/0xzhara/blob/output/github-contribution-grid-snake.svg)\n\n")

    # Spotify Now Playing
    f.write("## 🎧 Now Playing on Spotify\n")
    f.write("![Spotify](https://novatorem-0xzhara.vercel.app/api/spotify)\n\n")

    # WakaTime Coding Activity
    f.write("## ⏳ Weekly Coding Activity\n")
    f.write("![WakaTime](https://github-readme-stats.vercel.app/api/wakatime?username=0xzhara&layout=compact&theme=tokyonight&hide_border=true)\n\n")

    # GitHub Trophies
    f.write("## 🏆 GitHub Trophies\n")
    f.write("![Trophies](https://github-profile-trophy.vercel.app/?username=0xzhara&theme=tokyonight&no-frame=true&margin-w=5&margin-h=5)\n\n")

    # Social & Visitor Badges
    f.write("## 🌐 Connect with Me\n")
    f.write("[![Website](https://img.shields.io/badge/🌍%20Website-0xzhara-blue?style=for-the-badge)](https://t.me/airdropnobi) ")
    f.write("[![Twitter](https://img.shields.io/badge/Twitter-0xzhara-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/0xzhara) ")
    f.write("[![Telegram](https://img.shields.io/badge/Telegram-Chat-blue?style=for-the-badge&logo=telegram)](https://t.me/airdropnobi)\n\n")

    f.write("## 👀 Profile Visitors\n")
    f.write("![Visitor Count](https://komarev.com/ghpvc/?username=0xzhara&style=for-the-badge)\n\n")

    f.write("---\n")
    f.write("<p align='center'>⚡ Updated automatically by GitHub Actions</p>\n")
