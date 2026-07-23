# manifest_manager.py - 增量缓存（MD5）
import json, hashlib, os

MANIFEST_PATH = "manifest.json"

def load_manifest():
    if os.path.exists(MANIFEST_PATH):
        with open(MANIFEST_PATH, "r") as f:
            return json.load(f)
    return {"processed": {}}

def save_manifest(manifest):
    with open(MANIFEST_PATH, "w") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

def get_file_md5(path):
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def filter_unprocessed(pdf_files):
    manifest = load_manifest()
    unprocessed = []
    for pdf in pdf_files:
        md5 = get_file_md5(pdf)
        if pdf not in manifest["processed"] or manifest["processed"][pdf]["md5"] != md5:
            unprocessed.append(pdf)
    return unprocessed, manifest

def mark_processed(pdf_path, output_path, manifest):
    manifest["processed"][pdf_path] = {
        "md5": get_file_md5(pdf_path),
        "output": output_path
    }
    save_manifest(manifest)

if __name__ == "__main__":
    m = load_manifest()
    print(json.dumps(m, indent=2, ensure_ascii=False))
