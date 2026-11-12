# tt-organic-spark

TikTok Social Organic MCP + TikTok Ads MCP 的账号经营和 Spark Ads 加热 Skill。五个场景：账号体检、选帖加热（挑帖子 → 开授权 → 建暂停的 Video View / Engagement Spark Ad → 看自然 vs 付费）、评论运营、被提及监控、内容灵感。跨 connector 的动作由 Skill 编排。

## 安装

Claude Code：把整个文件夹放到 `~/.claude/skills/tt-organic-spark/`，新开会话即生效；`/tt-organic-spark` 可手动触发。

claude.ai / Cowork：上传本文件夹的 zip，或作为 plugin 的一个 skill 一起装。

前提：会话里连接了 TikTok Social Organic MCP（tt-ads-mcp-organic-social），加热还要连 TikTok Ads MCP（tt-ads-mcp-flat）并有广告账户授权。

## 试用

> 我账号最近一个月怎么样？
> 哪条视频值得投一下？帮我加热，一天 30 美元。
> 帮我看看评论，有要回的我来确认。
> 最近有人 @ 我们吗？
> 做蜡烛的，发什么内容、带什么 hashtag？

## 结构

- SKILL.md：入口分流、总规则、账号阶段、说话方式
- health.md：账号体检
- spark.md：选帖 → 授权 → 身份 → 建 → 看效果（跨 Organic / Ads）
- boost-params.md：Video View / Engagement Spark Ad 参数、读回、坑
- comments.md / mentions.md / inspiration.md：三个独立场景
- guardrails.md / glossary.md
