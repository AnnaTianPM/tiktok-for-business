# App Promotion（安装、应用内事件、tROAS、召回、App Traffic）

读前置：advertiser_info_get 币种；app_list_get 取 app_id、platform、skan_allowed、advanced_dedicated_campaign_allowed；app_optimization_event_get（objective APP_PROMOTION、app_promotion_type、optimization_goal）取可用事件名；tool_targeting_search 取 location_ids；identity_get 身份；召回时 dmp_custom_audience_list_get 取人群。

## campaign_create

| 参数 | 值 |
|---|---|
| objective_type | APP_PROMOTION |
| app_promotion_type | APP_INSTALL（拉新）；APP_RETARGETING（召回） |
| campaign_type | iOS 14.5+ 拉新用 IOS14_CAMPAIGN 并传 app_id（每个 campaign 最多 2 个活跃 adgroup）；其他 REGULAR_CAMPAIGN |
| budget_mode | BUDGET_MODE_INFINITE |
| operation_status | DISABLE |
| request_id | 新 64 位整数字符串 |

## adgroup_create 共用

promotion_type APP_ANDROID 或 APP_IOS；app_id；operating_systems 只填一个；billing_event OCPM；bid_type BID_TYPE_NO_BID + pacing PACING_MODE_SMOOTH；budget_mode BUDGET_MODE_DYNAMIC_DAILY_BUDGET，budget ≥ 20 USD（数值按 routing.md 阶段 4 的区间，用户定）；schedule SCHEDULE_FROM_NOW + 当前 UTC；location_ids；placement_type PLACEMENT_TYPE_NORMAL + ["PLACEMENT_TIKTOK"]；operation_status DISABLE；request_id。iOS 14.5+：ios14_targeting IOS14_PLUS，min_ios_version "14.5"。

## 四条路径只改这几项

| 路径 | optimization_goal | 其他 |
|---|---|---|
| MAI 优化安装 | INSTALL | 不传 secondary_optimization_event（TikTok 版位已不支持） |
| AEO 优化应用内事件 | IN_APP_EVENT | optimization_event 取自 app_optimization_event_get；deep_bid_type AEO |
| tROAS / HV | VALUE | optimization_event 购买类事件；deep_bid_type VO_MIN_ROAS + roas_bid，或 VO_HIGHEST_VALUE；vbo_window 默认 SEVEN_DAYS；部分场景白名单 |
| App Retargeting 召回 | IN_APP_EVENT 或 INSTALL | campaign 用 APP_RETARGETING；audience_type NEW_CUSTOM_AUDIENCE；audience_ids；事件取自 app_optimization_event_retargeting_get；iOS 用 ios14_targeting ALL + min_ios_version 14.5 |

App Traffic（只引流到商店页）：campaign objective_type TRAFFIC，adgroup promotion_type APP_ANDROID / APP_IOS + app_id，optimization_goal CLICK，billing_event CPC，bid_type BID_TYPE_NO_BID + pacing SMOOTH。用户要控出价才 BID_TYPE_CUSTOM + bid_price，数值先 tool_bid_recommend 取，取不到就问用户，不自己编。

## ad_create

creative_list 一条视频一个 creative：ad_format SINGLE_VIDEO，video_id，identity，ad_text，call_to_action；App 推广不用 landing_page_url，用 app 的下载链接由系统带。先读 schema 再填。

## 读回和开启

adgroup_get 核对 app_id、事件、出价、状态；adgroup_review_info_get 审核；确认后 adgroup_status_update ENABLE。报表 report_integrated_get，分平台看。

## 已知坑

- iOS 14.5+ 不走专用 campaign 没有 SKAN 数据；专用 campaign 不能用 APP_RETARGETING。
- optimization_goal INSTALL 带 secondary_optimization_event 只能 Pangle 或 Global App Bundle 版位。
- 批量复制 campaign_copy_task_create 后一定 campaign_copy_task_check；单次不超过 20 个对象。
