# Website Conversions（独立站）

三条路径共用一套读前置：advertiser_info_get 取币种；pixel_list_get 取 pixel_id 和事件；tool_targeting_search（FUZZY_SEARCH 市场名）取 location_ids；identity_get 取身份；catalog_get 取 catalog_id（Catalog 路径）。

## 路径 1 · 普通 Website Conversions（无 Catalog 或 SKU 少）

campaign_create：

| 参数 | 值 |
|---|---|
| objective_type | WEB_CONVERSIONS |
| budget_mode | BUDGET_MODE_INFINITE（预算放 adgroup） |
| operation_status | DISABLE |
| campaign_name | 商品或"全站" + 事件 + 日期 |
| request_id | 新 64 位整数字符串 |

adgroup_create：

| 参数 | 值 |
|---|---|
| promotion_type | WEBSITE |
| optimization_goal | CONVERT |
| pixel_id / optimization_event | 网站上装的事件叫 CompletePayment、AddToCart、ViewContent；建广告时对应的优化事件名是 SHOPPING、ON_WEB_CART、ON_WEB_DETAIL。购买一律传 SHOPPING（PURCHASE、COMPLETE_PAYMENT 会被拒） |
| billing_event | OCPM |
| bid_type / pacing | BID_TYPE_NO_BID + PACING_MODE_SMOOTH（Lowest Cost；NO_BID 必须配 SMOOTH） |
| budget_mode / budget | BUDGET_MODE_DYNAMIC_DAILY_BUDGET；USD ≥ 20，数值按 routing.md 阶段 4 的区间，用户定 |
| schedule_type / schedule_start_time | SCHEDULE_FROM_NOW + 当前 UTC |
| location_ids | tool_targeting_search 结果 |
| placement_type / placements | PLACEMENT_TYPE_NORMAL + ["PLACEMENT_TIKTOK"]（建后改不了） |
| age_groups / gender / interests | 不填，放宽；只在真正小众品类加 2 到 3 个兴趣 |
| operation_status | DISABLE |

ad_create：adgroup_id + creative_list，一条视频一个 creative（ad_format SINGLE_VIDEO，video_id 来自 file_video_ad_search 或 file_video_ad_upload，identity_id / identity_type，landing_page_url，ad_text，call_to_action）。先读 schema 再填。无素材时跳过 ad，告诉用户素材到了再建。

## 路径 2 · Catalog（SKU 多）

参数在 ads-products/catalog-shopping.md，这里不重复。概要：Smart+ 带目录（campaign catalog_enabled=true + catalog_type ECOMMERCE，adgroup catalog_id + catalog_authorized_bc_id）已对过 schema；普通目录视频购物广告是白名单。

### 旧版说明（保留对照）

smart_plus_campaign_create：objective_type=WEB_CONVERSIONS，sales_destination=WEBSITE，request_id。
smart_plus_adgroup_create：campaign_id、promotion_type=WEBSITE、optimization_goal=CONVERT、pixel_id、optimization_event、bid_type=BID_TYPE_NO_BID、billing_event=OCPM、targeting_spec（市场）、schedule_type=SCHEDULE_FROM_NOW、schedule_start_time、budget_mode=BUDGET_MODE_DYNAMIC_DAILY_BUDGET、budget、request_id；catalog 绑定参数待验证，先读 schema；schema 里找不到绑定 Catalog 的参数，或创建被拒，就退回路径 1 建非 Catalog 版本，并告诉用户 Catalog 版本要在 Ads Manager 补。
smart_plus_ad_create：creative_list，每项带 creative_info.ad_format。
读回：review_smart_plus_campaign，或 smart_plus_campaign_get、smart_plus_adgroup_get、smart_plus_ad_get（普通的 adgroup_get、ad_get 读不到 Smart+ 对象）。

建前必须告诉用户两件改不了或默认开的事：自动版位含 Pangle 和 Global App Bundle（只要 TikTok 就 placement_type=PLACEMENT_TYPE_NORMAL + PLACEMENT_TIKTOK）；自动素材增强可能改视频（可关）。

Smart+ 不挂自动规则（optimizer_rule 对 Smart+ 返回 40002）。普通 PRODUCT_SALES 目标的 Catalog 视频购物广告是白名单功能，不默认走。

## 路径 3 · VBO（在路径 1 或 2 上切）

前提：tool_vbo_status_check 通过，7 天 ≥ 20 次带金额购买。optimization_goal=VALUE，optimization_event=SHOPPING，deep_bid_type=VO_HIGHEST_VALUE（不设 ROAS）或 VO_MIN_ROAS + roas_bid。新建 adgroup，不改老的。部分 VBO 场景白名单，报错就如实说。

## Travel Ads（旅游行业，卡 3）

两条建法：Smart+（smart_plus_campaign_create objective_type WEB_CONVERSIONS，sales_destination WEBSITE，catalog_enabled=true，catalog_type TRAVEL_ENTERTAINMENT；adgroup catalog_id + catalog_authorized_bc_id，catalog 类型 HOTEL / FLIGHT / DESTINATION；targeting_spec 必须给 location_ids 或 zipcode_ids），这条 schema 已核对；普通 campaign_create 加 catalog_enabled=true 是白名单。没有旅游类目录就回到路径 1。

## 身份

identity_get 没有身份时：有已发布 TikTok 帖子就要帖子的广告授权码，tt_video_authorize_apply 后 tt_video_info_get，做 Spark Ad（tiktok_item_id + identity_type + identity_id）；否则让用户在 Ads Manager 绑 TikTok 账号后再建 ad。campaign 和 adgroup 不等身份。

## 读回和开启

adgroup_get 核对事件、预算、出价、状态；creative_ads_preview_create 预览；adgroup_review_info_get 审核；确认后 adgroup_status_update ENABLE。报表 report_integrated_get。
