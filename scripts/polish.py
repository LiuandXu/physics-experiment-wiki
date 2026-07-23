# polish.py - DeepSeek 文本润色
import os, sys, openai

client = openai.OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY", ""),
    base_url="https://api.deepseek.com/v1"
)

SYSTEM_PROMPT = """你是理工科教材的编辑。对以下 Markdown 格式的课件内容进行优化：
1. 修正 OCR 造成的错别字（特别是公式中的希腊字母、上下标）
2. 统一技术术语
3. 保留所有 LaTeX 公式（\\(...\\) 和 \\[...\\] 不变）、Mermaid 代码块、表格结构、图片路径
4. 将口语化表述改为书面学术风格
5. 不改变章节标题和 Markdown 结构层级
只输出修改后的全文，不添加任何解释说明。"""

def polish_text(text):
    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ],
        temperature=0.2,
        max_tokens=8192
    )
    return resp.choices[0].message.content

def count_formulas(text):
    return {
        "inline_open": text.count("\\("),
        "inline_close": text.count("\\)"),
        "display_open": text.count("\\["),
        "display_close": text.count("\\]"),
    }

if __name__ == "__main__":
    docs_dir = sys.argv[1] if len(sys.argv) > 1 else "docs"
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else None  # None=全部

    if not os.environ.get("DEEPSEEK_API_KEY"):
        print("❌ 未设置 DEEPSEEK_API_KEY 环境变量")
        sys.exit(1)

    files = sorted(
        [(os.path.getsize(os.path.join(dp, f)), os.path.join(dp, f))
         for dp, _, fs in os.walk(docs_dir) for f in fs if f.endswith(".md") and f != "index.md"],
        reverse=True
    )

    target = files if limit is None else files[:limit]
    for size, path in target:
        if size > 5120:
            with open(path, "r", encoding="utf-8") as f:
                raw = f.read()
            before = count_formulas(raw)
            print(f"润色中: {os.path.basename(path)} ({size} bytes)...")
            polished = polish_text(raw)
            after = count_formulas(polished)
            # 公式计数校验
            if before != after:
                print(f"  ⚠️ 公式计数变化! 前:{before} 后:{after}，保留原文")
                continue
            with open(path, "w", encoding="utf-8") as f:
                f.write(polished)
            print(f"  ✅ 已润色: {os.path.basename(path)}")
        else:
            print(f"  跳过(太小): {os.path.basename(path)} ({size} bytes)")
