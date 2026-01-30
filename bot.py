import requests
from datetime import datetime
import os

def get_tech_articles():
    
    tags = ['java', 'keycloak', 'spring-boot', 'devops']
    base_url = "https://dev.to/api/articles?tag="
    
    
    content = f"# ☕ Java & Security Daily Digest\n\n"
    
    
    content += "[![Daily Update](https://github.com/alejhomoreno/daily-tech-bot/actions/workflows/daily.yml/badge.svg)](https://github.com/alejhomoreno/daily-tech-bot/actions/workflows/daily.yml) "
    content += "![Python](https://img.shields.io/badge/python-3670A0?style=flat&logo=python&logoColor=ffdd54) "
    content += "![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=flat&logo=github-actions&logoColor=white)\n\n"

    
    content += "### 🛠️ Built with:\n"
    content += "<code><img height='30' src='https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg'></code> "
    content += "<code><img height='30' src='https://raw.githubusercontent.com/devicons/devicon/master/icons/github/github-original.svg'></code> "
    content += "<code><img height='30' src='https://raw.githubusercontent.com/devicons/devicon/master/icons/linux/linux-original.svg'></code>\n\n"

    
    content += f"\n"
    content += f"📅 **Last Update:** {datetime.now().strftime('%Y-%m-%d %H:%M')} (Local Time)\n\n"
    content += "---\n\n"

    found_something = False

    for tag in tags:
        try:
            response = requests.get(f"{base_url}{tag}&top=7&per_page=3", timeout=10)
            articles = response.json()
            if articles:
                found_something = True
                content += f"## 🔖 Top {tag.capitalize()}\n"
                for art in articles:
                    content += f"* **[{art['title']}]({art['url']})**\n"
                content += "\n"
        except Exception as e:
            print(f"Error connecting to API for {tag}: {e}")

    if not found_something:
        content += "## 💡 Daily Note\n"
        content += "Focusing on core engineering principles today. Keep building! 🚀\n"

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ README.md generated successfully.")

if __name__ == "__main__":
    get_tech_articles()
