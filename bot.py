import requests
from datetime import datetime, timezone

TAGS = ['java', 'keycloak', 'spring-boot', 'devops', 'networking']
API_URL = "https://dev.to/api/articles?tag="

BADGE_PYTHON = "https://img.shields.io/badge/python-3670A0?style=flat&logo=python&logoColor=ffdd54"
BADGE_ACTIONS = "https://img.shields.io/badge/GitHub%20Actions-2088FF?style=flat&logo=github-actions&logoColor=white"
ICON_PYTHON = "https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg"
ICON_GITHUB = "https://raw.githubusercontent.com/devicons/devicon/master/icons/github/github-original.svg"
ICON_LINUX = "https://raw.githubusercontent.com/devicons/devicon/master/icons/linux/linux-original.svg"

def get_tech_articles():
    
    now = datetime.now(timezone.utc)
    current_time = now.strftime('%Y-%m-%d %H:%M')
    
    content = f"""# ☕ Java & Security Daily Digest

![Python]({BADGE_PYTHON}) ![GitHub Actions]({BADGE_ACTIONS})

### 🛠️ Built with:
<code><img height='30' src='{ICON_PYTHON}'></code> <code><img height='30' src='{ICON_GITHUB}'></code> <code><img height='30' src='{ICON_LINUX}'></code>

📅 **Last Update:** {current_time} (UTC)

---

"""

    found_something = False

    for tag in TAGS:
        try:
            response = requests.get(f"{API_URL}{tag}&top=7&per_page=3", timeout=10)
            response.raise_for_status() 
            articles = response.json()
            
            if articles:
                found_something = True
                content += f"## 🔖 Top {tag.capitalize()}\n"
                for art in articles:
                    content += f"* **[{art['title']}]({art['url']})**\n"
                content += "\n"
                
        except Exception as e:
            print(f"⚠️ Warning: Could not fetch data for {tag}. Error: {e}")
    
    if not found_something:
        content += "## 💡 Daily Note\n"
        content += "Focusing on core engineering principles today. Keep building! 🚀\n"

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)
    
    print("✅ README.md generated successfully.")

if __name__ == "__main__":
    get_tech_articles()
