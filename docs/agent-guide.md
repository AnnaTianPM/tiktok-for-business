# TikTok for Business · AI Agent 接入指引

> 你（AI Agent）将帮用户把 TikTok for Business 的连接器和 Skills 接进他正在用的工具。
> 用户只需要做一件事：在浏览器里用自己的账号完成授权。其余由你执行或引导。
> 本文件由插件自动生成（2026-11-11），能力清单以 https://annatianpm.github.io/tiktok-for-business/llms.txt 为准。

## 0. 先检测，已装就跳过

1. 问用户在用哪个客户端（Claude Code / Claude.ai / Cursor / Codex / 其他）。
2. 检查是否已装：Claude Code 看 `/mcp` 或 `claude mcp list` 里有没有 `tiktok-ads`、`tiktok-organic-social`、`tiktok-one`；Cursor 看 `~/.cursor/mcp.json`；Codex 看 `~/.codex/config.toml`；Claude.ai 看 Connectors 列表。
3. 已装 → 跳到第 3 步验证。未装 → 第 1 步。

## 1. 安装连接器（按客户端）

**Claude Code（推荐，连 Skills 一起装）**

```
/plugin install tiktok-for-business --marketplace AnnaTianPM/tiktok-for-business
```

装完在会话里输入 `/mcp`，对每个连接器点一次认证，浏览器会打开 TikTok 的登录页。

**Claude.ai / Cowork**：设置 → Connectors → 添加自定义连接器，名称和 URL 各填一条：

- `tiktok-ads`：https://business-api.tiktok.com/open_mcp/tt-ads-mcp-flat
- `tiktok-organic-social`：https://business-api.tiktok.com/open_mcp/tt-ads-mcp-organic-social
- `tiktok-one`：https://business-api.tiktok.com/open_mcp/tto-mcp

**Cursor 及其他读 JSON 配置的客户端**：写入 MCP 配置文件（只填 url，不要填任何 header 或 key）：

```json
{
  "mcpServers": {
    "tiktok-ads": {
      "type": "http",
      "url": "https://business-api.tiktok.com/open_mcp/tt-ads-mcp-flat"
    },
    "tiktok-organic-social": {
      "type": "http",
      "url": "https://business-api.tiktok.com/open_mcp/tt-ads-mcp-organic-social"
    },
    "tiktok-one": {
      "type": "http",
      "url": "https://business-api.tiktok.com/open_mcp/tto-mcp"
    }
  }
}
```

**Codex**：追加到 `~/.codex/config.toml`：

```toml
[mcp_servers.tiktok-ads]
url = "https://business-api.tiktok.com/open_mcp/tt-ads-mcp-flat"

[mcp_servers.tiktok-organic-social]
url = "https://business-api.tiktok.com/open_mcp/tt-ads-mcp-organic-social"

[mcp_servers.tiktok-one]
url = "https://business-api.tiktok.com/open_mcp/tto-mcp"
```

写完配置后提醒用户：部分客户端要重启才会加载新的 MCP。

## 2. 授权（用户自己做）

- 首次调用任一连接器的工具时，客户端会弹出 TikTok 的 OAuth 授权页；没有自动打开浏览器的，把客户端打印的授权链接原样给用户，让他在本机浏览器打开。
- 三个连接器分别对应三种账号：TikTok Ads 用 TikTok for Business 账号，Social Organic 用 TikTok 账号，TikTok One 用 TikTok One 账号。用户可能只有其中一两种，缺哪个就只装哪个的 Skill。
- 不要向用户索要密码、验证码、Access Token；不要替用户点"同意"；不要把授权链接里的参数改掉。

## 3. 验证（只读工具，不改任何数据）

| 连接器 | 调这个 | 它做什么 |
|---|---|---|
| TikTok Ads | `auth_advertiser_get` | 列出这个登录能用的广告账户，不改任何东西 |
| TikTok Social Organic | `account_user_get` | 读当前授权账号的基础信息 |
| TikTok One | `tto_info_get` | 读当前 TikTok One 账户信息 |

调通就告诉用户"已接上，用的是账户 XX"。返回 unauthorized 或 401 → 回第 2 步；返回权限不足（如 40130 scope）→ 让用户在授权页勾全需要的权限后重新授权。

## 4. 启用 Skills

- Claude Code 装插件后 Skills 自动可用，不用额外操作。
- 其他客户端：从 https://annatianpm.github.io/tiktok-for-business/skills/market.json 取清单，把用户要用的 Skill 的 `content`（或直接读 `url`）作为系统指引放进会话；Skill 里"到那一步才读"的参考文件在 `https://annatianpm.github.io/tiktok-for-business/skills/<name>/` 下按需读取。
- 当前可用：

- **tt-ads-launch**（广告投放）：试一句「我是独立站卖蜡烛的，想在 TikTok 投广告拉销量，帮我建一条。」
- **tt-organic-spark**（账号经营）：试一句「看看我 TikTok 账号最近哪条视频跑得好，把它加热一下。」
- **tt-tto-creator**（达人合作）：试一句「帮我在美国找 5 个美妆达人，粉丝 10 万以上，发合作邀请。」

## 5. 调用异常

1. 重新 tools/list 刷新工具清单（客户端常缓存旧清单）。
2. 核对工具名拼写和参数结构，以 tools/list 返回的描述为准。
3. 重试一次。仍失败把错误原样告诉用户，依次检查：授权是否过期、客户端是否重启、网络。

## 6. 交付清单

| # | 项 | 完成标准 |
|---|---|---|
| 1 | 连接器已装 | 客户端里能看到 3 个连接器（或用户需要的那几个） |
| 2 | 已授权 | 每个连接器在客户端里显示已连接 |
| 3 | 验证通过 | 第 3 步的只读工具调通，向用户复述账户名 |
| 4 | Skills 可用 | Claude Code 已装插件；其他客户端已把所需 Skill 读入 |

任何一项没完成，说清楚"这项不完成就用不了哪类能力"，不报全部完成。
