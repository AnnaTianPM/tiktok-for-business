# tiktok-marketing plugin

三个 TikTok MCP 连接器 + 三个编排 Skill，一个包装完。

| Skill | 连接器 | 一句话 |
|---|---|---|
| tt-ads-launch | Ads | 从一句话建出可投放的广告，9 个阶段，7 类客户 |
| tt-organic-spark | Social Organic + Ads | 账号体检、选帖加热（Spark Ads）、评论、被提及、灵感 |
| tt-tto-creator | TikTok One + Social Organic + Ads | 找达人 → 建合作 → 挂链授权 → 效果 → 达人视频投放 |

## 连接器

- Ads：https://business-api.tiktok.com/open_mcp/tt-ads-mcp-flat
- Social Organic：https://business-api.tiktok.com/open_mcp/tt-ads-mcp-organic-social
- TikTok One：https://business-api.tiktok.com/open_mcp/tto-mcp

三个都是远程 HTTP MCP，装好 plugin 后在 Connectors 页各自登录授权一次。

## 安装

一步装（Claude Code 2.1.292+）：

```
claude plugin install tiktok-marketing --marketplace AnnaTianPM/tiktok-marketing-marketplace
```

会话里：`/plugin install tiktok-marketing --marketplace AnnaTianPM/tiktok-marketing-marketplace`

其他方式：

- Claude Code：`claude --plugin-dir ./tiktok-marketing-plugin`（临时）；长期用把本目录放进一个 marketplace 仓库后 `claude plugin marketplace add owner/repo` + `claude plugin install tiktok-marketing@<marketplace>`。
- claude.ai / Cowork：把本目录打成 zip 在 Customize > Plugins > Add > Upload plugin 上传；或由 Org Owner 在 Organization settings > Plugins & skills 里 Sync from GitHub。

## 校验

```
claude plugin validate ./tiktok-marketing-plugin
```
