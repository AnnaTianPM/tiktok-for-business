# 目录购物广告（Catalog Ads，独立站 SKU 多）

卡 2 的默认产品。两条建法，先走第一条，它的参数已对过 schema；第二条是白名单。

## 路径 1 · Smart+ 带商品目录（schema 已核对）

读前置：catalog_get 取 catalog_id 和它所属的 BC（catalog_authorized_bc_id）；pixel_list_get 取 pixel_id 和购物事件；tool_targeting_search 取 location_ids；diagnostic_catalog_get 看 Feed 健康。

smart_plus_campaign_create：

| 参数 | 值 |
|---|---|
| objective_type | WEB_CONVERSIONS |
| sales_destination | WEBSITE（建后改不了） |
| catalog_enabled / catalog_type | true / ECOMMERCE |
| budget_optimize_on / budget_mode / budget | 默认 CBO 开：BUDGET_MODE_DYNAMIC_DAILY_BUDGET + 日预算（建后 budget_mode 改不了） |
| operation_status | DISABLE |
| request_id、campaign_name | 新 64 位整数字符串；目录 + 日期 |

smart_plus_adgroup_create：

| 参数 | 值 |
|---|---|
| promotion_type | WEBSITE |
| catalog_id / catalog_authorized_bc_id | 来自 catalog_get，两个都必填 |
| optimization_goal / optimization_event / pixel_id | CONVERT / SHOPPING / 来自 pixel_list_get；要控回报用 VALUE + deep_bid_type VO_MIN_ROAS + roas_bid 或 VO_HIGHEST_VALUE |
| bid_type / billing_event | BID_TYPE_NO_BID / OCPM |
| targeting_optimization_mode / targeting_spec | AUTOMATIC；targeting_spec 里只给 location_ids（和语言）。要拉老客才 MANUAL + shopping_ads_retargeting_type LAB1/LAB2 + shopping_ads_retargeting_actions_days |
| placement_type / placements | 默认自动，含 Pangle 和 Global App Bundle，建后改不了。用户只要 TikTok：PLACEMENT_TYPE_NORMAL + ["PLACEMENT_TIKTOK"] |
| schedule_type / schedule_start_time | SCHEDULE_FROM_NOW + 当前 UTC |
| operation_status / request_id | DISABLE / 新值 |

smart_plus_ad_create：creative_list，每项 creative_info.ad_format；目录广告的商品由系统从目录取，视频可用自己的帖子或素材库。先读 schema 再填。

读回：review_smart_plus_campaign，或 smart_plus_campaign_get、smart_plus_adgroup_get、smart_plus_ad_get。

建前告诉用户：自动版位含 Pangle，自动素材增强可能改视频，两样都可以关。

## 路径 2 · 普通目录视频购物广告（白名单）

campaign_create objective_type PRODUCT_SALES + campaign_product_source CATALOG（schema 标注 Product Sales 是白名单功能）；adgroup_create shopping_ads_type VIDEO、product_source CATALOG、catalog_id、catalog_authorized_bc_id、shopping_ads_retargeting_type OFF、promotion_type WEBSITE、optimization_goal CONVERT + pixel_id + SHOPPING，其余同 web-conversions.md 路径 1。创建被拒（权限类错误）就不再试，退回路径 1。

## 退路

路径 1 报错且不是参数错误（比如账户没开通 Smart+ 目录广告）→ 退回 web-conversions.md 路径 1 建非目录版本，告诉用户目录版本要在后台开通后再加。SKU 少（几十个以内）本来就不走这里。

## 已知坑

- 目录和 Pixel 要绑定为事件源（catalog_eventsource_bind_get 能查），没绑的目录广告拿不到购物数据。
- Feed 有报错（diagnostic_catalog_get）先修，否则商品不展示。
- Smart+ 对象不能挂自动规则（optimizer_rule 返回 40002）。
