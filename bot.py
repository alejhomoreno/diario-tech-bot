import requests
from datetime import datetime
import os

def get_tech_articles():
    # ALEJHOMORNEO
    tags = ['java', 'keycloak', 'spring-boot', 'devops']
    base_url = "https://dev.to/api/articles?tag="
    
    
    content = f"# ☕ Java & Security Daily Digest\n\n"
    
    
    content += f"\n\n"
    
    
    content += f"📅 Last Update: {datetime.now().strftime('%Y-%m-%d %H:%M')} (Local Time)\n\n"

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
        content += "Today we are focusing on pure practice. Keep coding! 🚀\n"

    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ README.md generated successfully.")

if __name__ == "__main__":
    get_tech_articles()
