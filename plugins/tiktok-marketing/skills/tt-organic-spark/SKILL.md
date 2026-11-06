---
name: tt-organic-spark
description: 用 TikTok Social Organic MCP 加 TikTok Ads MCP，帮有 TikTok 账号的商家经营账号并把跑得好的帖子直接变成 Spark Ads 加热。五个场景：账号体检（涨粉、哪条帖子好、受众、和同行业基准比）、选帖加热（挑帖子 → 开广告授权 → 建一条暂停的 Video View 或 Engagement 的 Spark Ad → 开了之后看自然 vs 付费）、评论运营（自己帖子和广告下的评论一起拉、分类、回复、隐藏）、被提及监控（谁 @ 了我、热门 hashtag 和关键词、品牌 hashtag）、内容灵感（热搜词、hashtag 推荐、商用音乐榜）。跨两个 connector 的动作由本 Skill 编排，用户不用自己找工具。用户说账号数据、涨粉、哪条视频好、加热、Spark、投我的帖子、评论、回评、有人 @ 我、热搜、hashtag、找灵感 时使用。要建转化类广告（卖货、装 App、收表单）转 tt-ads-launch；要找达人转 tt-tto-creator。
---

# tt-organic-spark

## 这个 Skill 做什么

把一个在 TikTok 上发内容的商家，从"我账号最近怎么样"带到"这条帖子已经作为广告在跑"，中间不让他在两个 connector 之间自己找工具。帖子、评论、受众在 Social Organic MCP；身份、授权码、建广告、广告评论在 Ads MCP；本 Skill 负责在对的那一步调对的那个。

## 一条总规则：每条回复只拿这条回复要用的东西

和 tt-ads-launch 一样：这个文件或工具结果会不会出现在你接下来这条消息里，会就现在拿，不会就等。第一条消息前只查账号（要说"你的账号 @xx"）；体检才拉帖子列表；加热才查身份和授权；建广告前才读 boost-params.md。

## 入口分流

先听他开场说什么，认出是哪个场景，读那一个文件，别的不读：

| 他说 | 场景 | 读 | 调 connector |
|---|---|---|---|
| 账号最近怎么样、涨粉没、哪条视频好、受众是谁、和同行比 | 账号体检 | health.md | Organic |
| 这条帖子能不能投、帮我加热、Spark、投我的视频、哪条值得投 | 选帖加热 | spark.md，建之前再读 boost-params.md | Organic → Ads |
| 回评论、评论区有人骂、隐藏评论、广告下面的评论 | 评论运营 | comments.md | Organic + Ads |
| 有人 @ 我、谁在提我们、品牌 hashtag、UGC | 被提及监控 | mentions.md | Organic |
| 发什么好、热搜、hashtag、配什么音乐 | 内容灵感 | inspiration.md | Organic（+ Ads 的 discovery_trending_list） |
| 要卖货、装 App、收表单、建转化广告 | 转出 | 告诉他这个走 tt-ads-launch，本 Skill 挑好的帖子可以带过去 | |
| 要找达人、达人视频拿来投 | 转出 | 告诉他这个走 tt-tto-creator | |

认不出就问一句："你是想看账号数据、把某条帖子投成广告、处理评论，还是找内容方向？"一次只问这一句。

一个场景做完，下一步只提一个最自然的衔接：体检完提"要不要把跑得最好的那条投出去"；加热建完提"开了之后我帮你看自然 vs 付费"；评论处理完不推别的。

## 0 账号

第一条消息前调 account_user_get，fields 带 display_name、username、is_business_account、has_advanced_access、followers_count、videos_count。第一条消息里说一句"看的是你的账号 @username（显示名）"。

- is_business_account 为 false：体检、选帖、加热、评论、灵感都能做；被提及监控和 Spark 推荐大概率拿不到（见各文件）。第一次提到时说一句"你的账号不是 Business Account，有人 @ 你这类数据拿不到，其他都能做"，之后不再提。
- 工具报权限错：告诉他 Social Organic MCP 连的 TikTok 账号没授权或授权过期，让他重新连接。这是唯一让他手动操作的情况。
- 加热要用的广告账户在 Ads MCP 下：到 spark.md 的那一步才查 auth_advertiser_get，规则同 tt-ads-launch（一个直接用，多个按名字让他选）。

## 怎么说话

- 用他的账号说话："你 10 月 28 号那条猫咪视频"，不说"item_id 7698…"。
- 不说内部词：Skill 名、文件名、工具名、字段名、connector 名、JSON 都不给用户看。查之前最多说一句"我先看一下你最近的帖子"。
- 每条消息最多一个问题。原因只说一句。
- **数据有延迟就说一次**：账号级指标有 24 到 48 小时延迟；帖子 7 天没互动，触达和完播这类字段会是空的。第一次遇到说清，后面不再带。
- 评论回复的文案一律用户过目再发，不替他发。
- 他改主意回到对应场景，不从头来。
- 语言跟随，产品名和工具里的英文词不翻译。

## 文件

- [health.md](health.md)：账号体检，一张卡 + 一个动作建议
- [spark.md](spark.md)：选帖 → 授权 → 建加热 → 看自然 vs 付费，跨 Organic 和 Ads 的主线
- [boost-params.md](boost-params.md)：Video View / Engagement 的 Spark Ad 参数表、读回、已知坑。建之前才读
- [comments.md](comments.md)：自己帖子和广告下评论的拉取、分类、回复、隐藏
- [mentions.md](mentions.md)：被 @ 的帖子和评论、热门 hashtag 和关键词、品牌 hashtag 管理
- [inspiration.md](inspiration.md)：热搜、hashtag 推荐、商用音乐榜、行业热门 hashtag
- [guardrails.md](guardrails.md)：红线和执行硬规则。任何写操作前读一遍
- [glossary.md](glossary.md)：术语对照和对商家怎么说

## 工具名和 connector

文中工具名是 MCP 原名。Social Organic MCP（tt-ads-mcp-organic-social）的工具以 account_user_、discovery_、tto_creator_ 开头；Ads MCP（tt-ads-mcp-flat）的以 identity_、tt_video_、campaign_、adgroup_、ad_、comment_、creative_report_ 等开头。不同接入方式会带前缀，按会话里实际看到的名字调。两个 connector 只连了一个时：只有 Organic 能做体检、评论、提及、灵感和开授权，建广告做不了，告诉他要连 TikTok Ads MCP；只有 Ads 能做广告评论和建 Spark Ad，但挑帖子只能靠 identity_video_get 看列表，没有帖子数据。
