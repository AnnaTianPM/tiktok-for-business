# Smart+（自动投放：网站、App、线索、Minis）

Smart+ 是自动化层，不是单独的广告目标。它支持三个目标：WEB_CONVERSIONS、LEAD_GENERATION、APP_PROMOTION，不支持 TikTok Shop 卖货（PRODUCT_SALES 会被拒，40002）。本文件只列三个目标各自和普通版不同的参数，共用参数见各产品文件。网站带目录的版本见 catalog-shopping.md。

## 共用

smart_plus_campaign_create：objective_type；budget_optimize_on 默认 true（CBO），budget_mode BUDGET_MODE_DYNAMIC_DAILY_BUDGET + budget；operation_status DISABLE；request_id。budget_mode 和 sales_destination 建后改不了。
smart_plus_adgroup_create 必填：campaign_id、adgroup_name、promotion_type、optimization_goal、bid_type、billing_event、targeting_spec、schedule_type、schedule_start_time、request_id。bid_type BID_TYPE_NO_BID；billing_event OCPM（CLICK 才 CPC）；targeting_optimization_mode 默认 AUTOMATIC，targeting_spec 只给 location_ids；placement 默认自动，建后改不了，用户只要 TikTok 就 PLACEMENT_TYPE_NORMAL + ["PLACEMENT_TIKTOK"]；operation_status DISABLE。
smart_plus_ad_create：creative_list，每项 creative_info.ad_format。
读回：review_smart_plus_campaign，或 smart_plus_campaign_get、smart_plus_adgroup_get、smart_plus_ad_get。
建前告诉用户两件事：自动版位含 Pangle 和 Global App Bundle；自动素材增强可能改视频。都可以关。

## Smart+ Web（卡 2、卡 3 运营段）

campaign：WEB_CONVERSIONS + sales_destination WEBSITE。adgroup：promotion_type WEBSITE；optimization_goal CONVERT + pixel_id + optimization_event（SHOPPING、ON_WEB_REGISTER 等）；要控回报 VALUE + deep_bid_type。首投不用，购买或注册稳定后新建一组切过来。

## Smart+ App（卡 4 运营段）

campaign：APP_PROMOTION + app_promotion_type APP_INSTALL 或 APP_RETARGETING；iOS 14.5+ 用 campaign_type IOS14_CAMPAIGN + app_id。adgroup：promotion_type APP_ANDROID 或 APP_IOS；app_id；optimization_goal INSTALL / IN_APP_EVENT（optimization_event 必填，deep_bid_type AEO）/ VALUE（deep_bid_type VO_MIN_ROAS + roas_bid 或 VO_HIGHEST_VALUE，vbo_window 默认 SEVEN_DAYS）。

## Smart+ Lead（卡 6 运营段）

campaign：LEAD_GENERATION。adgroup：promotion_type LEAD_GENERATION + promotion_target_type INSTANT_PAGE 或 EXTERNAL_WEBSITE；optimization_goal LEAD_GENERATION（站内表单）或 CONVERT + pixel_id + FORM（网站表单）；消息类 promotion_type LEAD_GEN_CLICK_TO_SOCIAL_MEDIA_APP_MESSAGE + messaging_app_type + 账号参数，来电 LEAD_GEN_CLICK_TO_CALL。

## Smart+ Minis（卡 5 的 TikTok Series 和小游戏）

campaign：APP_PROMOTION + app_promotion_type MINIS。adgroup：promotion_type NATIVE_SERIES + native_series_id + identity_id / identity_type（Series 的主持账号），或 MINI_GAME + minis_id；optimization_goal 和 optimization_event 按 app_optimization_event_get。这是 Growth Max 之外、MCP 现在就能建的站内剧集和小游戏路径；短剧 App 本身仍走 Growth Max 或普通 App Promotion。

## 已知坑

- 一个 Smart+ campaign 最多 30 个 adgroup；CBO 开着时各 adgroup 的目标、事件、出价必须一致。
- Smart+ 不能挂自动规则（optimizer_rule 返回 40002）。
- Smart+ 没有 PRODUCT_SALES，Shop 卖货只能 GMV Max。
