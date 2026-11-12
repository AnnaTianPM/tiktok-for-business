# 三个 connector 的工具对照

只连了其中一个 connector、或工具名对不上时读。同一能力优先用 TTO MCP；只连了 Ads MCP 就用右列，注意账户参数名。

## TTO MCP（tto-mcp）↔ Ads MCP（tt-ads-mcp-flat）

| 能力 | TTO MCP | Ads MCP | 参数差异 |
|---|---|---|---|
| 列 TTO 账户 | tto_oauth2_get | tto_oauth2_tcm_get | Ads 只返回 ID 列表没有名字，要名字再 tto_oauth2_info_get |
| 账户详情 | tto_info_get（tto_id） | tto_oauth2_info_get（tto_tcm_account_id） | |
| 品牌档案 | tto_brand_profile_get / create（tto_id） | tto_tcm_brand_profile_get / create（tto_tcm_account_id） | |
| 建活动 | tto_campaign_create（tto_id；campaign_name 必填；spark_ads_requested_authorization_days） | tto_tcm_campaign_create（tto_tcm_account_id；campaign_name 非必填；default_spark_ads_requested_authorization_days） | 授权天数字段名不同 |
| 查活动 | tto_campaign_get | tto_tcm_campaign_get | 都是 page_size ≤ 5 |
| 改活动 | tto_campaign_update | tto_tcm_campaign_update | |
| 挂链请求 | tto_campaign_link（post_id） | tto_tcm_campaign_link（video_id） | 视频参数名不同 |
| 挂链状态 | tto_campaign_link_status_get | tto_tcm_campaign_link_status_get | |
| 申请 / 延长授权 | tto_campaign_video_auth_apply（post_id） | tcm_tt_video_apply（video_id，tcm_account_id） | 两个参数名都不同 |
| 授权状态 | tto_campaign_video_auth_status_get | tcm_tt_video_status_get | |
| 活动报表 | tto_campaign_report_get（country_code 参数） | tto_tcm_report（Country-Code 作为 header，MCP 里按 schema 填） | |
| Spark 推荐 | tto_post_recommend_get（tto_id） | spark_ad_recommend_get（tcm_account_id） | |
| 标签 | tto_creator_category_label_get | tto_tcm_category_label_get | |
| 排行榜 | tto_creator_rank_scoreboard_get | tto_tcm_rank_get | |
| Anchor | tto_anchor_create / get / delete | tto_tcm_anchor_create / get / delete | |
| **找达人** | tto_creator_discover、tto_creator_public_get、tto_creator_public_video_list_get、tto_creator_status_get | **没有** | 只连 Ads 做不了第 1 步，要他给 handle |

## Social Organic MCP（达人侧）

tto_creator_authorized_get、tto_creator_authorized_video_list_get、tto_creator_campaign_join、tto_creator_campaign_video_link、tto_creator_link_request_get、tto_creator_link_request_confirm。用达人自己的账号授权，没有 tto_id。另外两个 connector 里没有对应。

## 建 Spark Ad（只在 Ads MCP）

identity_get、identity_video_get、tt_video_list_get、tt_video_info_get、tt_video_authorize_apply、campaign_create、adgroup_create、ad_create、*_status_update、creative_report_get。参数见 tt-organic-spark/boost-params.md。
