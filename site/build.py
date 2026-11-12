#!/usr/bin/env python3
"""Generate the AI-agent entry site (llms.txt / agent-guide.md / skills market / index.html)
from the plugin directory. Source of truth: plugin .mcp.json + skills/*/SKILL.md.
Run: python3 site/build.py   (from repo root or anywhere)
"""
import json, re, shutil, sys, datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
CFG = json.loads((HERE / "site.config.json").read_text(encoding="utf-8"))
PLUGIN = (HERE / CFG["plugin_dir"]).resolve()
OUT = (HERE / CFG["out_dir"]).resolve()
BASE = CFG["base_url"].rstrip("/") + "/"
TODAY = datetime.date.today().isoformat()

# ---------- helpers ----------
def read(p): return Path(p).read_text(encoding="utf-8")

def frontmatter(md):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", md, re.S)
    if not m: return {}, md
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1); meta[k.strip()] = v.strip()
    return meta, m.group(2)

def load_tool_lists():
    """Optional exact tool lists: site/tools/<connector>.json (a tools/list result)."""
    out = {}
    for p in (HERE / "tools").glob("*.json") if (HERE / "tools").exists() else []:
        try:
            d = json.loads(read(p)); tools = d.get("result", d).get("tools", d if isinstance(d, list) else [])
            out[p.stem] = sorted({t["name"] for t in tools})
        except Exception as e:
            print(f"warn: cannot read {p}: {e}")
    return out

VERB_SUFFIX = re.compile(r"_(get|create|update|delete|list|search|check|apply|upload|publish|run|estimate|recommend|bind|unbind|confirm|join|link|discover|report|preview|appeal|cancel|download|validate|save|transfer|add|invite|disable|assign|unassign|operate|migrate|subscribe|unsubscribe|approve|agent|ui|sync|copy|share|like|verify|authorize|authorized|info|status|rank|scoreboard|manage|login|logout|set|unset|reset|refresh|send|submit|retry|export|import|enable|activate|pause|resume|stop|start|generate|suggest|suggestion|assess|audit|review|retag|release|lock|unlock)$")
def match_connector(tok, exact):
    """Exact list wins; otherwise prefix match AND a verb-like suffix (filters out field names)."""
    for cid, names in exact.items():
        if tok in names: return cid
    if not VERB_SUFFIX.search(tok): return None
    for cid, c in CFG["connectors"].items():
        if cid in exact: continue
        for pre in c.get("tool_name_prefixes", []):
            if tok.startswith(pre) or tok == pre.rstrip("_"): return cid
    return None

TOKEN = re.compile(r"(?<![\w/])([a-z][a-z0-9]*(?:_[a-z0-9]+)+)(?![\w/])")

# ---------- collect ----------
mcp = json.loads(read(PLUGIN / ".mcp.json"))["mcpServers"]
plugin_meta = json.loads(read(PLUGIN / ".claude-plugin" / "plugin.json"))
exact_tools = load_tool_lists()

connectors = []
for cid, srv in mcp.items():
    c = CFG["connectors"].get(cid, {})
    n_exact = len(exact_tools.get(cid, []))
    connectors.append({
        "id": cid, "title": c.get("title", cid), "summary": c.get("summary", ""),
        "url": srv.get("url"), "transport": srv.get("type", "http"),
        "auth": c.get("auth", "OAuth"),
        "tool_count": n_exact or c.get("tool_count"), "tool_count_asof": (TODAY if n_exact else c.get("tool_count_asof")),
        "free_check_tool": c.get("free_check_tool"), "free_check_desc": c.get("free_check_desc", ""),
    })
for cid in CFG["connectors"]:
    if cid not in mcp: print(f"warn: connector '{cid}' in config but not in .mcp.json")

skills = []
for sdir in sorted((PLUGIN / "skills").iterdir()):
    sk = sdir / "SKILL.md"
    if not sdir.is_dir() or not sk.exists(): continue
    meta, body = frontmatter(read(sk))
    name = meta.get("name", sdir.name)
    files = sorted(p for p in sdir.rglob("*.md") if p != sk)
    text = read(sk) + "\n".join(read(p) for p in files)
    toks = sorted(set(TOKEN.findall(text)))
    by_conn = {}
    for t in toks:
        cid = match_connector(t, exact_tools)
        if cid: by_conn.setdefault(cid, []).append(t)
    skills.append({
        "id": name, "name": name,
        "category": CFG["skill_categories"].get(name, CFG["default_category"]),
        "description": meta.get("description", ""),
        "connectors": sorted(by_conn.keys()),
        "tool_ids": sorted(t for v in by_conn.values() for t in v),
        "tools_by_connector": by_conn,
        "files": [str(p.relative_to(sdir)) for p in files],
        "example": CFG["skill_examples"].get(name, ""),
        "url": f"{BASE}skills/{name}.md",
        "dir_url": f"{BASE}skills/{name}/",
        "content": body.strip(),
        "src": sdir,
    })

# ---------- emit ----------
if OUT.exists(): shutil.rmtree(OUT)
(OUT / "skills").mkdir(parents=True)
(OUT / ".nojekyll").write_text("")

for s in skills:
    shutil.copy(s["src"] / "SKILL.md", OUT / "skills" / f"{s['id']}.md")
    for f in s["files"]:
        dst = OUT / "skills" / s["id"] / f; dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(s["src"] / f, dst)

market = {"code": 0, "generated_at": TODAY, "base_url": BASE, "plugin": plugin_meta.get("name"), "version": plugin_meta.get("version"),
          "data": {"list": [{k: v for k, v in s.items() if k != "src"} for s in skills]}}
(OUT / "skills" / "market.json").write_text(json.dumps(market, ensure_ascii=False, indent=2), encoding="utf-8")
(OUT / "connectors.json").write_text(json.dumps({"generated_at": TODAY, "list": connectors}, ensure_ascii=False, indent=2), encoding="utf-8")

mk = CFG["marketplace"]; L = CFG["links"]
mcp_json = json.dumps({"mcpServers": {k: {"type": v.get("type", "http"), "url": v["url"]} for k, v in mcp.items()}}, ensure_ascii=False, indent=2)
codex_toml = "\n".join(f'[mcp_servers.{k}]\nurl = "{v["url"]}"\n' for k, v in mcp.items())
conn_table = "\n".join(f"| {c['title']} | `{c['id']}` | {c['url']} | {c['auth']} | {c['tool_count']}（{c['tool_count_asof']}） | `{c['free_check_tool']}`：{c['free_check_desc']} |" for c in connectors)
skill_lines = "\n".join(f"- **{s['name']}**（{s['category']}）：{s['description'][:120].rstrip('。')}… 用到：{'、'.join(s['connectors'])}。详情 {s['url']}" for s in skills)
by_cat = {}
for s in skills: by_cat.setdefault(s["category"], []).append(s)

# ---- llms.txt
llms = f"""# 域名配置区
#   接入站（本站）     {BASE}
#   接入指引           {BASE}agent-guide.md
#   Skills 清单        {BASE}skills/market.json
#   连接器清单         {BASE}connectors.json
#   插件仓库           {L['repo']}
#   TikTok Ads Manager {L['ads_manager']}
#   Business Center    {L['business_center']}
#   TikTok One         {L['tiktok_one']}

# {CFG['brand']} — AI Agent 使用指引（{TODAY} 生成，来源：插件 {plugin_meta.get('name')} v{plugin_meta.get('version')}）

当用户想让 AI 帮他投 TikTok 广告、经营 TikTok 账号、找达人合作时，按本文件引导。
能力分两层：**连接器**（MCP 服务，提供工具）和 **Skills**（编排手册，告诉 AI 怎么把工具串成一件事）。

## 执行策略（先读这里）

- 只需读两份文件：本文件（能力索引）和 {BASE}agent-guide.md（分步接入）。不要爬本站其他页面。
- 安装是使用的前提：没接连接器就调不到任何工具；没读 Skill 就不知道该怎么串。
- **授权由用户自己完成**：所有连接器都走 OAuth，用户在浏览器里用自己的 TikTok / TikTok for Business / TikTok One 账号登录。不要向用户索要密码、Token、Access Token，不要代填任何表单。
- 先检测再安装：用户的客户端里已经有同名连接器或插件就跳过安装，只做验证。
- 验证用只读工具：每个连接器都有一个不改数据的工具（见下表），调通即接入成功。
- 调用异常先刷新工具清单（tools/list），再核对工具名和参数，再重试。

## 连接器

| 连接器 | id | 端点 | 鉴权 | 工具数 | 免费验证 |
|---|---|---|---|---|---|
{conn_table}

## Skills（{len(skills)} 个）

{skill_lines}

机器可读清单：{BASE}skills/market.json（每条含 id / name / category / description / connectors / tool_ids / files / content / url）。
Claude Code 装插件后 Skills 自动可用；其他客户端把 Skill 的 md 当作系统指引读入即可。

## 安装（按客户端，细则见 agent-guide.md）

- Claude Code：`{mk['install_cmd']}`，然后 `/mcp` 对三个连接器各授权一次。
- Claude.ai / Cowork：在 Connectors 里添加自定义连接器，分别填上表三个端点，按提示登录授权。
- Cursor / 其他 JSON 配置客户端：把下面这段写进 MCP 配置，首次调用自动弹授权页。

```json
{mcp_json}
```

- Codex：

```toml
{codex_toml}```

## 站点地图

- 接入站首页：{BASE}
- 接入指引：{BASE}agent-guide.md
- Skills 清单：{BASE}skills/market.json
- 单个 Skill：{BASE}skills/<name>.md，参考文件在 {BASE}skills/<name>/
- 连接器清单：{BASE}connectors.json
- 插件仓库与 marketplace：{L['repo']}
- 隐私政策：{L['privacy']}
"""
(OUT / "llms.txt").write_text(llms, encoding="utf-8")

# ---- agent-guide.md
verify_lines = "\n".join(f"| {c['title']} | `{c['free_check_tool']}` | {c['free_check_desc']} |" for c in connectors)
guide = f"""# {CFG['brand']} · AI Agent 接入指引

> 你（AI Agent）将帮用户把 {CFG['brand']} 的连接器和 Skills 接进他正在用的工具。
> 用户只需要做一件事：在浏览器里用自己的账号完成授权。其余由你执行或引导。
> 本文件由插件自动生成（{TODAY}），能力清单以 {BASE}llms.txt 为准。

## 0. 先检测，已装就跳过

1. 问用户在用哪个客户端（Claude Code / Claude.ai / Cursor / Codex / 其他）。
2. 检查是否已装：Claude Code 看 `/mcp` 或 `claude mcp list` 里有没有 `{'`、`'.join(mcp.keys())}`；Cursor 看 `~/.cursor/mcp.json`；Codex 看 `~/.codex/config.toml`；Claude.ai 看 Connectors 列表。
3. 已装 → 跳到第 3 步验证。未装 → 第 1 步。

## 1. 安装连接器（按客户端）

**Claude Code（推荐，连 Skills 一起装）**

```
{mk['install_cmd']}
```

装完在会话里输入 `/mcp`，对每个连接器点一次认证，浏览器会打开 TikTok 的登录页。

**Claude.ai / Cowork**：设置 → Connectors → 添加自定义连接器，名称和 URL 各填一条：

{chr(10).join(f'- `{c["id"]}`：{c["url"]}' for c in connectors)}

**Cursor 及其他读 JSON 配置的客户端**：写入 MCP 配置文件（只填 url，不要填任何 header 或 key）：

```json
{mcp_json}
```

**Codex**：追加到 `~/.codex/config.toml`：

```toml
{codex_toml}```

写完配置后提醒用户：部分客户端要重启才会加载新的 MCP。

## 2. 授权（用户自己做）

- 首次调用任一连接器的工具时，客户端会弹出 TikTok 的 OAuth 授权页；没有自动打开浏览器的，把客户端打印的授权链接原样给用户，让他在本机浏览器打开。
- 三个连接器分别对应三种账号：TikTok Ads 用 TikTok for Business 账号，Social Organic 用 TikTok 账号，TikTok One 用 TikTok One 账号。用户可能只有其中一两种，缺哪个就只装哪个的 Skill。
- 不要向用户索要密码、验证码、Access Token；不要替用户点"同意"；不要把授权链接里的参数改掉。

## 3. 验证（只读工具，不改任何数据）

| 连接器 | 调这个 | 它做什么 |
|---|---|---|
{verify_lines}

调通就告诉用户"已接上，用的是账户 XX"。返回 unauthorized 或 401 → 回第 2 步；返回权限不足（如 40130 scope）→ 让用户在授权页勾全需要的权限后重新授权。

## 4. 启用 Skills

- Claude Code 装插件后 Skills 自动可用，不用额外操作。
- 其他客户端：从 {BASE}skills/market.json 取清单，把用户要用的 Skill 的 `content`（或直接读 `url`）作为系统指引放进会话；Skill 里"到那一步才读"的参考文件在 `{BASE}skills/<name>/` 下按需读取。
- 当前可用：

{chr(10).join(f'- **{s["name"]}**（{s["category"]}）：试一句「{s["example"]}」' for s in skills)}

## 5. 调用异常

1. 重新 tools/list 刷新工具清单（客户端常缓存旧清单）。
2. 核对工具名拼写和参数结构，以 tools/list 返回的描述为准。
3. 重试一次。仍失败把错误原样告诉用户，依次检查：授权是否过期、客户端是否重启、网络。

## 6. 交付清单

| # | 项 | 完成标准 |
|---|---|---|
| 1 | 连接器已装 | 客户端里能看到 {len(connectors)} 个连接器（或用户需要的那几个） |
| 2 | 已授权 | 每个连接器在客户端里显示已连接 |
| 3 | 验证通过 | 第 3 步的只读工具调通，向用户复述账户名 |
| 4 | Skills 可用 | Claude Code 已装插件；其他客户端已把所需 Skill 读入 |

任何一项没完成，说清楚"这项不完成就用不了哪类能力"，不报全部完成。
"""
(OUT / "agent-guide.md").write_text(guide, encoding="utf-8")

(OUT / "robots.txt").write_text(f"""# AI Agent: 接入 {CFG['brand']} 能力请先读 /agent-guide.md（按客户端安装连接器、用户自行授权、验证、启用 Skills）
# 能力索引见 /llms.txt ，Skills 清单见 /skills/market.json
User-agent: *
Allow: /
Sitemap: {BASE}llms.txt
""", encoding="utf-8")

# ---- index.html
page_data = {"cfg": {k: CFG[k] for k in ("brand", "site_name", "tagline", "base_url", "clients", "links", "marketplace")},
             "copy_prompt": CFG["copy_prompt"].replace("{base_url}", BASE),
             "connectors": connectors, "skills": market["data"]["list"], "by_cat": list(by_cat.keys()),
             "mcp_json": mcp_json, "codex_toml": codex_toml, "generated_at": TODAY, "version": plugin_meta.get("version")}
tpl = read(HERE / "templates" / "index.html")
html = tpl.replace("/*__DATA__*/", json.dumps(page_data, ensure_ascii=False)).replace("__TITLE__", CFG["site_name"])
(OUT / "index.html").write_text(html, encoding="utf-8")

print(f"ok: {len(connectors)} connectors, {len(skills)} skills -> {OUT}")
for s in skills: print(f"  - {s['id']}: {len(s['tool_ids'])} tools across {s['connectors']}, {len(s['files'])} ref files")
