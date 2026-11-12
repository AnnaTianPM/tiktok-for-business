# 手动 Shop Ads（TikTok Shop，用户点名要自己控商品和出价）

卡 1 判定表第 3 行。占 Shop Ads 不到 1%，只在用户点名时做，并说明绝大多数卖家用 GMV Max。

读前置：gmv_max_store_list_get 取 store_id、store_authorized_bc_id；store_product_get 取商品；identity_get 身份；tool_targeting_search 取 location_ids。

campaign_create：objective_type PRODUCT_SALES；campaign_product_source STORE；budget_mode BUDGET_MODE_INFINITE；operation_status DISABLE；request_id。schema 标注 Product Sales 是白名单功能，被拒就停，回到 GMV Max。

adgroup_create 三种：

| 类型 | 参数 |
|---|---|
| 视频购物 Video Shopping Ads | shopping_ads_type VIDEO；product_source STORE；store_id + store_authorized_bc_id；promotion_type VIDEO_SHOPPING；optimization_goal CONVERT 或 VALUE（VALUE 配 deep_bid_type VO_MIN_ROAS + roas_bid，范围 0.01 到 20） |
| 商品卡 Product Shopping Ads | shopping_ads_type PRODUCT_SHOPPING_ADS；product_source STORE；store_id + store_authorized_bc_id；promotion_type TIKTOK_SHOP；不传 catalog 参数 |
| 直播购物 Live Shopping Ads | shopping_ads_type LIVE；promotion_type LIVE_SHOPPING；identity_id + identity_type 必填；optimization_goal MT_LIVE_ROOM 或 PRODUCT_CLICK_IN_LIVE |

共用：billing_event OCPM；bid_type BID_TYPE_NO_BID + pacing PACING_MODE_SMOOTH；budget_mode BUDGET_MODE_DYNAMIC_DAILY_BUDGET，budget ≥ 20 USD；schedule SCHEDULE_FROM_NOW + 当前 UTC；location_ids；placements 只支持 ["PLACEMENT_TIKTOK"]；operation_status DISABLE；request_id。不支持 spending_power 和 saved_audience_id。

ad_create：视频购物带商品（product_specific_type 和商品 ID），先读 schema。

读回：adgroup_get；审核 adgroup_review_info_get；开启 adgroup_status_update。

## 已知坑

- 店铺独家授权给了别的账户时这里也建不了，先按 gmv-max.md 的授权处理。
- 同一 campaign 下的 adgroup 要么全 CATALOG，要么 STORE / SHOWCASE 混，不能两种都有。
