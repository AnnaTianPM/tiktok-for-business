# GMV Max（TikTok Shop）

## 前置检查（顺序固定）

1. gmv_max_store_list_get：选 is_gmv_max_available=true 的店，记下 store_id、store_authorized_bc_id。看 exclusive_authorized_advertiser_info：为空 → 用户确认后 gmv_max_exclusive_authorization_create 授权给本账户（不花钱）；是本账户 → 直接用；是别的账户 → 不动，告诉用户去改授权或换账户，这张卡到此为止。
2. Product 全店：gmv_max_store_shop_ad_usage_check_check 看 promote_all_products_allowed；不允许就改指定商品。
3. 指定商品：store_product_get（ad_creation_eligible=GMV_MAX），只取 status=AVAILABLE 且 gmv_max_ads_status=UNOCCUPIED 的 item_group_id，最多 400。
4. 身份：gmv_max_identity_get。Product 可不传（用商品图）；传就取 product_gmv_max_available=true 的，0 到 20 个。Live 必须恰好 1 个 live_gmv_max_available=true 的身份。
5. gmv_max_bid_recommend_get 取 roas_bid 和 budget 推荐值。

## 参数预设 · Product

| 参数 | 值 |
|---|---|
| shopping_ads_type | PRODUCT |
| optimization_goal | VALUE（唯一可选） |
| deep_bid_type | VO_MIN_ROAS（唯一可选），roas_bid 必填，一位小数 |
| roas_bid | 推荐值；用户给盈亏线时取其 1.2 倍起，不高于推荐值很多 |
| budget | 日预算，不低于推荐最低值；用户坚持更低就照用户的并说明影响 |
| product_specific_type | ALL（全店）或 CUSTOMIZED_PRODUCTS + item_group_ids |
| product_video_specific_type | AUTO_SELECTION（identity_list 可选）；用户点名用指定帖子才 CUSTOM_SELECTION + item_list |
| schedule_type / schedule_start_time | SCHEDULE_FROM_NOW，当前 UTC 时间 "YYYY-MM-DD HH:MM:SS" |
| request_id | 新的 64 位整数字符串 |
| campaign_name | 商品名或"全店" + 日期 |
| store_id / store_authorized_bc_id | 来自 store_list |

Live 只改：shopping_ads_type=LIVE，identity_list 恰好一个直播身份，不传 product_* 参数。

## 暂停处理

campaign_gmv_max_create 没有 operation_status，建即进入投放。所以：
- 预算和 ROAS 必须在建之前得到用户确认（"让用户看到要建什么"和"用户明确说开"合在这一步，说清"建了就会开始花钱"）。
- 余额为 0 的账户可以先建，不会消耗；提醒充值后自动开始。
- 用户要先建后看：建完立刻 campaign_gmv_max_info_get 读回，再问是否暂停；暂停用 campaign_gmv_max_update 改状态（该参数待验证，失败就如实说并给 Ads Manager 路径）。

## 读回和运营

- 读回：campaign_gmv_max_info_get 核对 product 范围、budget、roas_bid、status。
- 报表：gmv_max_report_get，按 campaign 和商品各拉一次。
- 改预算 / ROAS：campaign_gmv_max_update，一次只改一项，预算单次 ≤ 30%。
- 加视频：gmv_max_creative_update。

## 已知坑

- Smart+ 没有 PRODUCT_SALES 目标，API 直接拒（40002）。Shop 卖货只能走 GMV Max。
- 店铺独家授权给了别的广告账户就建不了，先换账户或改授权。
- 商品被其他 GMV Max campaign 占用（gmv_max_ads_status 非 UNOCCUPIED）不能再选。
