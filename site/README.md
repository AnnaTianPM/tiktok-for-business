# site/：AI Agent 接入站生成器

把插件目录当唯一事实来源，生成一套给 AI 读的入口文件和一张给人看的页面，输出到 `../docs/`（GitHub Pages 从 docs 发布）。

## 生成什么

| 产物 | 给谁 | 内容 |
|---|---|---|
| `docs/llms.txt` | AI | 能力索引：连接器、Skills、安装、验证、站点地图 |
| `docs/agent-guide.md` | AI | 分步接入 SOP：检测已装 → 按客户端安装 → 用户自己授权 → 启用 Skills → 免费工具验证 → 交付清单 |
| `docs/skills/market.json` | AI / 程序 | Skills 清单：id、name、category、description、connectors、tool_ids、files、content、url |
| `docs/skills/<name>.md` 与 `docs/skills/<name>/*.md` | AI | 每个 Skill 的 SKILL.md 和它引用的参考文件，原样发布 |
| `docs/connectors.json` | AI / 程序 | 连接器清单（url、鉴权、工具数、免费验证工具） |
| `docs/index.html` | 人 | 一页：复制提示词、能力卡、Skills 卡、各客户端安装步骤 |
| `docs/robots.txt` | AI 爬虫 | 指向 llms.txt 和 agent-guide.md |

## 怎么用

```bash
python3 site/build.py
```

## 以后加能力

- **加一个 Skill**：在 `plugins/tiktok-for-business/skills/` 下新建目录，放 SKILL.md（frontmatter 要有 name、description）和它的参考 md。可选：在 `site.config.json` 的 `skill_categories` 给它一个类别、`skill_examples` 给一句用户示例。跑一次 build。
- **加一个连接器**：在 `plugins/tiktok-for-business/.mcp.json` 加一条，在 `site.config.json` 的 `connectors` 加同名一节（标题、摘要、鉴权方式、工具数、免费验证工具、工具名前缀）。跑一次 build。
- **工具数**：TikTok 的 MCP 端点 tools/list 需要鉴权，所以工具数写在配置里并带日期；有授权时可以把 tools/list 结果存成 `site/tools/<connector>.json`，build 会优先用它统计并做精确的 tool_ids 匹配。
- **换域名**：改 `base_url`，所有绝对链接和复制提示词一起变。

## 没做的

- 不代用户留资、不收集手机号。授权永远由用户自己在浏览器里完成。
