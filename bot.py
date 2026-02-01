import os
import time
import logging
import tempfile
import requests
import datetime as dt
from typing import List, Dict, Any


TAGS = ["java", "keycloak", "spring-boot", "devops", "networking"]
BASE = "https://dev.to/api/articles"
PER_PAGE = 25
TIMEOUT = 10  # seconds
OUTPUT_FILE = "README.md"


BADGE_PYTHON = "https://img.shields.io/badge/python-3670A0?style=flat&logo=python&logoColor=ffdd54"
BADGE_ACTIONS = "https://img.shields.io/badge/GitHub%20Actions-2088FF?style=flat&logo=github-actions&logoColor=white"
ICON_PYTHON = "https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg"
ICON_GITHUB = "https://raw.githubusercontent.com/devicons/devicon/master/icons/github/github-original.svg"
ICON_LINUX = "https://raw.githubusercontent.com/devicons/devicon/master/icons/linux/linux-original.svg"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("daily-tech-bot")


def top3_for(tag: str) -> List[Dict[str, Any]]:
    try:
        resp = requests.get(BASE, params={"tag": tag, "per_page": PER_PAGE}, timeout=TIMEOUT)
        resp.raise_for_status()
        items = resp.json()
        if not isinstance(items, list):
            logger.warning("Unexpected response for tag %s: %s", tag, type(items))
            return []
        items.sort(key=lambda a: (a.get("positive_reactions_count", 0), a.get("comments_count", 0)), reverse=True)
        return items[:3]
    except requests.RequestException as e:
        logger.error("HTTP error fetching tag %s: %s", tag, e)
        return []
    except Exception as e:
        logger.exception("Unexpected error processing tag %s: %s", tag, e)
        return []


def build_readme(selections: Dict[str, List[Dict[str, Any]]]) -> str:
    now = dt.datetime.now(dt.timezone.utc)
    current_time = now.strftime("%Y-%m-%d %H:%M")
    ts_log = now.isoformat(timespec="microseconds") 

    header = f"""# ☕ Java & Security Daily Digest

![Python]({BADGE_PYTHON}) ![GitHub Actions]({BADGE_ACTIONS})

### 🛠️ Built with:
<code><img height='30' src='{ICON_PYTHON}'></code> <code><img height='30' src='{ICON_GITHUB}'></code> <code><img height='30' src='{ICON_LINUX}'></code>

📅 **Last Update:** {current_time} (UTC)

---
"""
    lines = [header]
    for tag, articles in selections.items():
        pretty_tag = tag.replace("-", " ").title()
        if articles:
            lines.append(f"## 🔖 Top {pretty_tag}")
            lines.append("")
            for a in articles:
                title = a.get("title", "Untitled")
                url = a.get("url") or a.get("canonical_url") or "#"
                reactions = a.get("positive_reactions_count", 0)
                comments = a.get("comments_count", 0)
                lines.append(f"* **[{title}]({url})** — **{reactions}** 👍 · {comments} 💬")
            lines.append("")
    if not any(selections.values()):
        lines.append("## 💡 Daily Note")
        lines.append("Focusing on core engineering principles today. Keep building! 🚀")
        lines.append("")

    
    lines.append(f"<!-- Log-ID: {ts_log} -->")
    lines.append("")

    return "\n".join(lines)


def atomic_write(path: str, content: str, encoding: str = "utf-8") -> None:
    dirpath = os.path.dirname(os.path.abspath(path)) or "."
    fd, tmp_path = tempfile.mkstemp(dir=dirpath, prefix=".tmp_readme_", text=True)
    try:
        with os.fdopen(fd, "w", encoding=encoding) as f:
            f.write(content)
        os.replace(tmp_path, path)
    finally:
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception:
                pass


def main() -> int:
    selections: Dict[str, List[Dict[str, Any]]] = {}
    for t in TAGS:
        selections[t] = top3_for(t)
        time.sleep(0.4)  
    readme = build_readme(selections)
    atomic_write(OUTPUT_FILE, readme)
    logger.info("README written: %s", OUTPUT_FILE)
    print("README.md with layout and ranking generated successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
