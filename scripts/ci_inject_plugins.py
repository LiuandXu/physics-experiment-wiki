# ci_inject_plugins.py - CI 动态注入插件
from ruamel.yaml import YAML

yaml = YAML()
yaml.preserve_quotes = True
with open("mkdocs.yml", "r", encoding="utf-8") as f:
    config = yaml.load(f)

plugins = config["plugins"]
if not isinstance(plugins, list):
    plugins = [plugins]

names = {p if isinstance(p, str) else list(p.keys())[0] for p in plugins}
if "minify" not in names:
    plugins.append({"minify": {"minify_html": False, "minify_js": True, "minify_css": True}})
if "git-revision-date-localized" not in names:
    plugins.append({"git-revision-date-localized": {"type": "date"}})

config["plugins"] = plugins
with open("mkdocs.yml", "w", encoding="utf-8") as f:
    yaml.dump(config, f)
print("✅ CI 插件已注入")
