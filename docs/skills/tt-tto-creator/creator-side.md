# 达人侧：加入活动、挂视频、处理请求

用户是达人本人（或替达人操作）时读。工具在 Social Organic MCP，以 tto_creator_ 开头，用达人自己的 TikTok 账号授权，不需要 tto_id。

## 先看自己

tto_creator_authorized_get 看达人自己的 TTO 画像（display_name、粉丝等，fields 可加）；tto_creator_authorized_video_list_get（limit ≤ 10）看自己视频的 post_id、collaboration_status（NONE 表示没挂任何活动）、数据。

## 三个动作

| 达人要 | 工具 | 说明 |
|---|---|---|
| 加入品牌的活动 | tto_creator_campaign_join，tto_invite_link | 活动级链接要求达人在被邀请名单里；品牌级链接任何 TTO 达人都能加 |
| 把已发的视频挂到活动 | tto_creator_campaign_video_link，post_id + tto_invite_link | 视频不能已挂别的活动；先 join 再 link |
| 看和处理品牌发来的挂链请求 | tto_creator_link_request_get（tto_invite_link）→ 列出 link_request_id、视频、品牌 → tto_creator_link_request_confirm，action APPROVE / REJECT | 没有请求时报 40002 "Found no linking requests"，这是正常的空，不是错误 |

发新视频时直接挂活动：account_user_post_publish 的 post_info.tto_invite_link + is_branded_content true。**本 Skill 不发帖**（见 guardrails.md），告诉达人在 TikTok App 里发，发的时候选品牌内容和活动。

每个写动作前一句话确认，做完读回（tto_creator_authorized_video_list_get 看 collaboration_status 变化）。

## 和品牌侧怎么接

达人挂链后，品牌侧在 link-auth.md 第 3 步能看到 post_id 和 status；绑了广告账户的活动会自动给 Spark 授权。达人同意授权请求是在 TikTok App 里，MCP 这边没有对应工具。
