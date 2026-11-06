# Web Traffic（无事件时的起量路径）

用途：Pixel 没有购物事件，或店铺未授权急着引流。目的是让事件先跑起来，7 天内有购买回传就回到转化路径，不动在跑的 Traffic。

campaign_create：objective_type=TRAFFIC，budget_mode=BUDGET_MODE_INFINITE，operation_status=DISABLE，request_id。

adgroup_create：

| 参数 | 值 |
|---|---|
| promotion_type | WEBSITE |
| optimization_goal / billing_event | 落地页浏览：TRAFFIC_LANDING_PAGE_VIEW + OCPM（默认，更接近真实访问）。点击：CLICK + CPC，bid_type BID_TYPE_NO_BID 也可以；用户要控单次点击成本才 BID_TYPE_CUSTOM + bid_price，数值先 tool_bid_recommend 取，取不到问用户，不自己编。PRD 大盘里点击占 49%、落地页浏览 30%，两条都常用 |
| bid_type / pacing | BID_TYPE_NO_BID + PACING_MODE_SMOOTH |
| budget_mode / budget | BUDGET_MODE_DYNAMIC_DAILY_BUDGET；USD ≥ 20；新客 20 到 50 一天，跑 2 周 |
| schedule | SCHEDULE_FROM_NOW + 当前 UTC |
| location_ids | tool_targeting_search |
| placements | PLACEMENT_TYPE_NORMAL + ["PLACEMENT_TIKTOK"] |
| operation_status | DISABLE |

不需要 pixel_id。ad_create 同 web-conversions.md。

同时做：没有 Pixel 就 pixel_create 并给安装指引；有 Pixel 就让用户补 ViewContent、AddToCart、CompletePayment。约定：pixel_list_get 看到购买事件 7 天内触发，就新建转化 adgroup。
