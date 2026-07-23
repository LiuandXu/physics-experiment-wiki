# generate_stats.py - 统计页面/公式/图片/代码块，写入 index.md
import os, re, sys

def collect_stats(docs_dir):
    stats = {"pages": 0, "formulas": 0, "images": 0, "code_blocks": 0}
    for root, _, files in os.walk(docs_dir):
        for f in files:
            if not f.endswith(".md"):
                continue
            stats["pages"] += 1
            content = open(os.path.join(root, f), "r", encoding="utf-8").read()
            stats["formulas"] += len(re.findall(r'\$[^$]+\$', content))
            stats["formulas"] += content.count('\\(')
            stats["images"] += len(re.findall(r'!\[.*?\]\(.*?\)', content))
            stats["code_blocks"] += len(re.findall(r'```', content)) // 2
    return stats

def patch_index(index_path, stats):
    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()
    content = re.sub(r'页面数：\s*\d+', f'页面数： {stats["pages"]}', content)
    content = re.sub(r'公式数：\s*\d+', f'公式数： {stats["formulas"]}', content)
    content = re.sub(r'图片数：\s*\d+', f'图片数： {stats["images"]}', content)
    content = re.sub(r'代码块：\s*\d+', f'代码块： {stats["code_blocks"]}', content)
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ 首页统计已更新: {stats}")

if __name__ == "__main__":
    docs_dir = sys.argv[1] if len(sys.argv) > 1 else "docs"
    stats = collect_stats(docs_dir)
    patch_index(os.path.join(docs_dir, "index.md"), stats)
