# qa_check.py - QA 检查：控制字符、公式闭合、图片路径、Mermaid 陷阱
import os, re, sys

def run_qa(docs_dir):
    issues = []
    for root, _, files in os.walk(docs_dir):
        for f in files:
            if not f.endswith(".md"):
                continue
            path = os.path.join(root, f)
            with open(path, "r", encoding="utf-8") as fp:
                content = fp.read()

            rel = os.path.relpath(path, docs_dir)

            # 检查 1: 控制字符 / 乱码
            if re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f\uFFFD]', content):
                issues.append(f"乱码/控制字符: {rel}")

            # 检查 2: 行内公式闭合
            if content.count("\\(") != content.count("\\)"):
                issues.append(f"行内公式未闭合: {rel} (\\(={content.count(chr(92)+'(')} \\)={content.count(chr(92)+')')})")

            # 检查 3: 行间公式闭合
            if content.count("\\[") != content.count("\\]"):
                issues.append(f"行间公式未闭合: {rel} (\\[={content.count(chr(92)+'[')} \\]={content.count(chr(92)+']')})")

            # 检查 4: 图片路径是否存在
            for img in re.findall(r'!\[.*?\]\((.*?)\)', content):
                if not img.startswith("http") and not os.path.exists(os.path.join(docs_dir, img)):
                    issues.append(f"图片缺失: {rel} -> {img}")

            # 检查 5: Mermaid 禁用 TD 布局
            if re.search(r'graph\s+TD|flowchart\s+TD', content, re.I):
                issues.append(f"Mermaid 使用 TD 布局: {rel}")

            # 检查 6: Mermaid 禁用 <br/>
            if '<br/>' in content or '<br>' in content:
                issues.append(f"含 <br/>/<br>: {rel}")

            # 检查 7: Mermaid 标签中未转义的 <
            for block in re.findall(r'```mermaid\n(.*?)\n```', content, re.S):
                for line in block.splitlines():
                    label = re.search(r'\["([^"]*)"\]', line)
                    if label and '<' in label.group(1):
                        issues.append(f"Mermaid 标签含未转义 '<': {rel}")
                        break

    if issues:
        print("\n".join("⚠️ " + i for i in issues))
        sys.exit(1)
    else:
        print("✅ QA 检查通过！")

if __name__ == "__main__":
    docs_dir = sys.argv[1] if len(sys.argv) > 1 else "docs"
    run_qa(docs_dir)
