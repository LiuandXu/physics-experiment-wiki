# build_nav.py - 扫描 docs/ 生成 mkdocs.yml nav 块
import os, re

def extract_h1(path):
    with open(path, encoding="utf-8") as f:
        for line in f:
            m = re.match(r"^#\s+(.+)", line.strip())
            if m:
                return m.group(1)
    return None

def scan_docs(docs_dir):
    nav = [{"首页": "index.md"}]
    for f in sorted(os.listdir(docs_dir)):
        if not f.endswith(".md") or f == "index.md":
            continue
        title = extract_h1(os.path.join(docs_dir, f)) or f.replace(".md", "")
        nav.append({title: f})
    return nav

def to_yaml(nav, indent=2):
    lines = []
    pad = " " * indent
    for item in nav:
        for k, v in item.items():
            lines.append(f"{pad}- {k}: {v}")
    return "\n".join(lines)

if __name__ == "__main__":
    docs_dir = "docs"
    nav = scan_docs(docs_dir)
    print("nav:")
    print(to_yaml(nav))
