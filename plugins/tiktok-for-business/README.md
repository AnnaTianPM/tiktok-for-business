# TikTok for Business · Claude 插件

TikTok for Business 官方 Claude 插件。连上你的广告账户、TikTok 账号和 TikTok One，用一句话完成三件事：

| 你想 | Skill | 用到的连接器 |
|---|---|---|
| 投广告：从一句话到建出能投放的广告 | tt-ads-launch | Ads |
| 经营账号：体检、把好帖子加热成 Spark Ads、回评论、看谁 @ 了你、找灵感 | tt-organic-spark | Social Organic + Ads |
| 找达人：筛达人、建合作、拿授权、把达人视频投出去 | tt-tto-creator | TikTok One + Social Organic + Ads |

## 安装

Claude Code 一步装（2.1.292+）：

```
claude plugin install tiktok-for-business --marketplace AnnaTianPM/tiktok-for-business
```

会话里：`/plugin install tiktok-for-business --marketplace AnnaTianPM/tiktok-for-business`

Cowork：Plugins 页 → Add marketplace → 填 `AnnaTianPM/tiktok-for-business` → 装 **TikTok for Business**。

claude.ai / Cowork 用文件装：Customize > Plugins > Add > Upload plugin，选本目录的 zip。

本地试用：`claude --plugin-dir ./tiktok-for-business`

## 连接器

- Ads：https://business-api.tiktok.com/open_mcp/tt-ads-mcp-flat
- Social Organic：https://business-api.tiktok.com/open_mcp/tt-ads-mcp-organic-social
- TikTok One：https://business-api.tiktok.com/open_mcp/tto-mcp

装好后在 Connectors 页各自登录授权一次。

## 校验

```
claude plugin validate ./tiktok-for-business --profile directory
```
