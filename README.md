# TikTok for Business · Claude plugin marketplace

## Install (Claude Code)

```
claude plugin install tiktok-for-business --marketplace AnnaTianPM/tiktok-for-business
```

Or in two steps:

```
claude plugin marketplace add AnnaTianPM/tiktok-for-business
claude plugin install tiktok-for-business@tiktok-for-business
```

## Install (Cowork)

Plugins page → Add marketplace → `AnnaTianPM/tiktok-for-business` → install **TikTok for Business**.

## Plugins

- **tiktok-for-business**: 3 TikTok MCP connectors (Ads, Social Organic, TikTok One) + 3 skills (tt-ads-launch, tt-organic-spark, tt-tto-creator).

## AI Agent 接入站（docs/）

`docs/` 是给 AI 读的入口站，由 `site/build.py` 从本仓库的插件目录自动生成：`llms.txt`（能力索引）、`agent-guide.md`（分步接入）、`skills/market.json`（Skills 清单）、`connectors.json`、`index.html`（给人看的一页）。

- 加 skill 或 connector 后重新生成：

```
python3 site/build.py
```

- 发布：GitHub → Settings → Pages → Source 选 `main` 分支的 `/docs` 目录。域名改在 `site/site.config.json` 的 `base_url`。
- 给用户的一句话：复制 `index.html` 顶部的提示词发给任何支持 MCP 的 AI 即可。
- 细则见 [site/README.md](site/README.md)。
