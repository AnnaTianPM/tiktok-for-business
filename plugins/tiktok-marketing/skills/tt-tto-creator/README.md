# tt-tto-creator

TikTok One（TTO）MCP + Social Organic MCP + TikTok Ads MCP 的达人合作 Skill。五步：定账户和品牌档案 → 找达人 → 建合作活动（绑广告账户自动拿 Spark 授权）→ 跟进挂链和授权 → 看效果并把好视频投成 Spark Ad。达人侧的加入、挂链、确认请求也在里面。三个 connector 的工具由 Skill 对照调用。

## 安装

Claude Code：把整个文件夹放到 `~/.claude/skills/tt-tto-creator/`，`/tt-tto-creator` 可手动触发。

claude.ai / Cowork：上传本文件夹的 zip，或作为 plugin 的一个 skill 一起装。

前提：连接 TikTok One MCP（tto-mcp）；建广告要连 TikTok Ads MCP；达人侧要连 Social Organic MCP（用达人自己的账号授权）。

## 试用

> 帮我找几个美国的美妆达人，粉丝 5 万到 50 万。
> 建一个达人合作活动，邀请 @xxx 和 @yyy，视频授权给我的广告账户 30 天。
> 看看哪些达人挂了视频、授权到哪一步了。
> 这个活动效果怎么样？哪条视频值得投？
> 我是达人，想加入这个活动并把我昨天的视频挂上去。

## 结构

- SKILL.md：五步主线、账户阶段、说话方式
- discover.md / campaign.md / link-auth.md / report.md：四步各一份
- creator-side.md：达人侧
- tool-map.md：三个 connector 工具和参数名对照
- guardrails.md / glossary.md
