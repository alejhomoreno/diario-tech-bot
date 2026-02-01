import requests, datetime, time
TAGS = ["java","keycloak","devops","networking"]
BASE = "https://dev.to/api/articles"
def top3_for(tag):
    r = requests.get(BASE, params={"tag":tag,"per_page":30})
    r.raise_for_status()
    items = r.json()
    items.sort(key=lambda a: (a.get("positive_reactions_count",0), a.get("comments_count",0)), reverse=True)
    return items[:3]

def build_readme(selections):
    ts = datetime.datetime.isoformat(timespec='microseconds')+'Z'
    lines = ["# Noticias técnicas", f"> **Log ID:** {ts}", ""]
    for tag, articles in selections.items():
        lines.append(f"## {tag}")
        for a in articles:
            lines.append(f"- [{a['title']}]({a['url']}) — **{a.get('positive_reactions_count',0)}** 👍")
        lines.append("")
    return "\n".join(lines)

if __name__ == "__main__":
    sel = {t: top3_for(t) for t in TAGS}
    readme = build_readme(sel)
    open("README.md","w",encoding="utf-8").write(readme)



