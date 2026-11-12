# 3 挂链和授权跟进

到第 3 步才读。产出一张进度表和一个动作。读 guardrails.md 再做写操作。

## 进度表

开头说"我去看谁挂了视频、授权到哪一步了"。

1. tto_campaign_get，campaign_ids 填他的活动，读 handle_names（邀请了谁）、video_ids（已挂的视频）、invite_link、country_codes、spark_ads_requested_authorization_days、advertiser_ids。
2. tto_campaign_link_status_get，campaign_ids 填活动（≤ 50 个），可按 handle_names 过滤。每行：post_id、status（APPROVE / 待处理 / 拒绝）、link_request_id、number_of_requests（催了几次）、last_reminded_timestamp。
3. 对每个已挂的 post_id：tto_campaign_video_auth_status_get，读 auth_status（WAITING / 已授权 / 拒绝）、requested_authorization_days、auth_status_updated_time。绑了 advertiser_ids 的活动，达人挂链时自动授权，这里多半已经是通过。

表：

| 达人 | 邀请了 | 挂了视频 | 挂链请求 | Spark 授权 | 下一步 |
|---|---|---|---|---|---|
| @handle | 是 / 否 | post_id 或"还没" | 状态 + 催过几次 | 状态 + 天数 | 一句 |

## 动作只给一个

| 情况 | 动作 |
|---|---|
| 达人发了相关视频但没挂到活动 | 发挂链请求：tto_campaign_link，action LINK，post_id 从 tto_creator_public_video_list_get 拿（视频不能已挂其他活动，达人必须已被邀请） |
| 请求发了 24 小时没回 | 催：同一个 tto_campaign_link LINK，系统当提醒发；**24 小时内不能催，最多催 2 次** |
| 发错了要收回 | tto_campaign_link，action REVOKE，只在达人没处理前有效，每个请求只能撤一次 |
| 视频挂了但没授权（活动没绑广告账户） | 申请授权：tto_campaign_video_auth_apply，post_id、authorization_days（1 到 365，默认 30）。视频必须已标 branded content 并挂到活动 |
| 授权快到期 | 延期：tto_campaign_video_auth_apply，action EXTEND，authorization_days 要延的天数 |
| 达人还没加入 TTO | tto_creator_status_get 显示 NOT_IN：让他邀请达人先加入，或走线下授权码（tt-organic-spark/spark.md 第 3 步） |

每个写动作做之前一句话确认（"给 @xx 发挂链请求？"），他说是再做；他前面说过"都发"就一次做完。做完读回状态再报。

## 达人那边要做什么（告诉用户转达）

达人收到邀请 → 点邀请链接或在 TikTok 里接受 → 发视频时打开"品牌内容"开关并选这个活动，或者发完后挂到活动 → 品牌发的授权请求达人在 TikTok 里同意，可以自己改天数。达人用 MCP 操作的流程在 creator-side.md。

## 已知坑

- tto_campaign_link 对已挂到其他活动的视频报错；先 tto_campaign_link_status_get 核对。
- 催的 24 小时冷却按 last_reminded_timestamp 算，提前催直接报错。
- auth_status WAITING 是达人还没点同意，不是系统问题；达人同意时可以改天数，实际天数以读回为准。
- 绑了 advertiser_ids 且授权天数 > 0 的活动，达人挂链即自动授权；这种活动不用再 auth_apply。
