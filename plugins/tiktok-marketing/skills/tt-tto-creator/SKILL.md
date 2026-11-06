---
name: tt-tto-creator
description: 用 TikTok One（TTO）MCP、Social Organic MCP 和 TikTok Ads MCP，帮品牌和代理从"想找达人"到"达人视频在我的广告账户里跑起来"走完一条线。五步：定 TTO 账户和品牌档案 → 找达人（按国家、粉丝、互动率、价位、受众画像筛，看公开画像和近期视频，美国有排行榜）→ 建达人合作活动（campaign 级或品牌级邀请链接，绑广告账户自动拿 Spark 授权，邀请达人）→ 跟进挂链和授权（谁挂了视频、发请求、催、申请或延长 Spark 授权）→ 看效果并把好视频投成 Spark Ad。达人侧的加入活动、挂链、确认请求也在本 Skill 里。TTO 工具在 TTO MCP 和 Ads MCP 各有一份，由本 Skill 对照调用，用户不用分。用户说找达人、KOL、创作者、合作、TTO、TikTok One、Creator Marketplace、达人视频投广告、邀请链接、授权天数 时使用。
---

# tt-tto-creator

## 这个 Skill 做什么

把一个只会说"我想找几个美妆达人拍我们产品"的品牌，带到"达人视频已经授权给我的广告账户，正在作为 Spark Ad 跑"。中间涉及三个 connector：找达人、建活动、授权、报表在 TTO MCP；达人自己加入活动、挂链、确认请求在 Social Organic MCP；最后建广告在 Ads MCP。本 Skill 在对的那一步调对的那个。

## 一条总规则：每条回复只拿这条回复要用的东西

第一条消息前只查 TTO 账户；找达人那一步才拉标签和搜索；建活动前才查品牌档案和广告账户；建广告前才读 tt-organic-spark 的 boost-params.md 或 tt-ads-launch 的参数文件。

## 五步主线

| 步 | 一条消息做什么 | 用户看到 | 读 |
|---|---|---|---|
| 0 账户 | 列 TTO 账户，一个直接用，多个按名字选；看国家和认证状态 | 一句话，并入第一条 | 本文件 |
| 1 找达人 | 问清品类、市场、预算档，按标签和筛选条件搜，出候选表，深看 3 到 5 个 | 候选表 + 一个问题 | discover.md |
| 2 建活动 | 品牌档案有没有，活动类型，绑哪个广告账户、授权几天，邀请谁 | 活动单 + 邀请链接 | campaign.md |
| 3 挂链和授权 | 谁挂了视频、谁没动、发请求或催、授权状态 | 一张进度表 + 一个动作 | link-auth.md |
| 4 效果和加热 | 每条视频自然 vs 付费数据，推荐哪条投，建 Spark Ad | 效果表 + 一个动作 | report.md，建广告时读 tt-organic-spark/boost-params.md |
| 达人侧 | 达人本人要加入活动、挂视频、处理品牌发来的请求 | 一个动作 | creator-side.md |

他从中间进来（"我已经有活动了，看看谁挂了视频"）就直接去那一步，前面的不补问。

## 0 账户

第一条消息前 tto_oauth2_get（TTO MCP）或 tto_oauth2_tcm_get（Ads MCP）列出能用的 TTO 账户。

- 只有一个：直接用，第一条消息说"用的是你的 TikTok One 账户 XX"。
- 多个：按名字列（**测试环境下会有几十上百个、同名的也多**，只列前 10 个不同名字的，让他说名字或 ID）；他说"随便"也不替他挑。
- 定了就 tto_info_get 读 account_name、country、business_verification_status。没过认证（不是 PASSED）先说，有些功能会受限。

建广告要用的广告账户到第 2 步绑定时才查 auth_advertiser_get，规则同 tt-ads-launch。

## 怎么说话

- 用他的品牌说话："你的护发精油"，不说"该品牌方"。达人用 @handle 加显示名称呼。
- 不说内部词：Skill 名、文件名、工具名、字段名、connector 名、JSON 不给用户看。
- 每条消息最多一个问题。原因只说一句。
- **达人数据是公开统计，有延迟**：排行榜更新时间看返回的 last_updated_at，可能是几个月前；说一次。
- **邀请链接是给达人用的**，发给用户时说清"把这个链接发给达人，他点开就能加入"。
- 他改主意回到对应步，不从头来。
- 语言跟随，产品名和英文词不翻译。

## 文件

- [discover.md](discover.md)：找达人：标签、筛选、排行榜、深看画像和视频、核对是否已是 TTO 达人
- [campaign.md](campaign.md)：品牌档案、建活动（CAMPAIGN / BRAND_LINK）、绑广告账户和授权天数、邀请、Anchor
- [link-auth.md](link-auth.md)：挂链状态、发请求 / 催 / 撤回、Spark 授权申请、延期、状态
- [report.md](report.md)：活动报表（自然 vs 付费）、Spark 推荐、交接建广告
- [creator-side.md](creator-side.md)：达人侧：加入活动、挂视频、看和确认挂链请求
- [tool-map.md](tool-map.md)：同一能力在三个 connector 里的工具名和参数名对照。只连了其中一个时读
- [guardrails.md](guardrails.md)：红线和执行硬规则。任何写操作前读
- [glossary.md](glossary.md)：术语对照和对品牌怎么说

## 工具名和 connector

文中优先写 TTO MCP（tto-mcp）的工具名，以 tto_ 开头，账户参数叫 tto_id。Ads MCP（tt-ads-mcp-flat）里同一能力叫 tto_tcm_*，账户参数叫 tto_tcm_account_id，个别参数名不同，见 tool-map.md。达人侧工具在 Social Organic MCP（tt-ads-mcp-organic-social），以 tto_creator_ 开头，用达人自己的 TikTok 账号授权。不同接入方式会带前缀，按会话里实际看到的名字调。
