# 4 效果和加热

到第 4 步才读。产出一张效果表和一个动作。他要建广告时再读 tt-organic-spark/boost-params.md（Video View / Engagement）或 tt-ads-launch 的参数文件（转化目标）。

## 效果表

1. tto_campaign_get 读 country_codes。**报表必须带 country_code**，活动有多个国家就每个国家各调一次。
2. tto_campaign_report_get，tto_id、campaign_id、country_code；要按天看就带 start_date / end_date（UTC，start 不早于活动创建时间），返回 daily_stats。page_size 默认 25，最多 100。
3. 每行一条视频，关键字段：creator_info.handle_name、post_info.create_time、video_views（合计）、video_views_organic / video_views_paid、likes / comments / shares 各有 organic 和 paid、engagement_rate_organic / engagement_rate_paid、video_completion_rate_*、six_seconds_views、ad_impressions、ad_cost、ad_cpm、ad_clicks、ad_ctr、ad_conversions、ad_roas。受众分布字段（audience_*）有数时给。

表：

| 达人 | 视频 | 自然播放 | 自然互动率 | 付费播放 | 花费 | CPM | 6 秒观看 | 完播 |
|---|---|---|---|---|---|---|---|---|

表下三句：哪条自然表现最好；付费那几条值不值；一个动作。

## 推荐哪条投

- tto_post_recommend_get，tto_id，objective_type 按他目标（REACH / VIDEO_VIEWS / TRAFFIC / WEB_CONVERSIONS / PRODUCT_SALES / APP_PROMOTION / LEAD_GENERATION），time 默认不传。返回 recommendation_level。新账户或视频少于 10 条会空，空就退回按报表手工排：自然互动率高 + 完播率高 + 还没投过（video_views_paid 为 0）的优先。
- 给 1 到 3 条，每条一句为什么。

## 交接建广告

他说"投这条"：

1. 先核对授权：tto_campaign_video_auth_status_get 为已授权，且活动绑了他要用的广告账户（campaign 的 advertiser_ids）。没绑就先 tto_campaign_update 追加，再 auth_apply，等达人同意。
2. Ads 侧找身份：identity_get **传 identity_type AUTH_CODE**（不传类型会一次返回全部身份且分页失效），找 display_name 或 username 是这位达人 handle 的那一条；tt_video_list_get 核对这条 post_id 在授权列表里。
3. 建：目标是曝光 / 观看 / 涨粉 → 按 tt-organic-spark/boost-params.md 建 Video View 或 Engagement 的 Spark Ad，identity_type AUTH_CODE + identity_id + tiktok_item_id = post_id；目标是卖货 / 装 App / 收表单 → 转 tt-ads-launch，告诉它"素材用 Spark Ad，帖子 ID 是 X，身份是 AUTH_CODE 的 @handle"，它从阶段 7 接。
4. 全部暂停建，读回，他说开才开。

## 已知坑

- 漏 country_code 直接报错；country_codes 为空的活动（没有达人挂链）报表也是空。
- 报表里 null 和 0 不一样：null 是没数据，0 是有数据但为零。给用户时 null 说"暂无"。
- 达人视频被用作 Spark Ad 后，自然侧数据（video_views_organic）和付费侧分开，合计在 video_views。
- API 建的活动报表只能在这里看，TTO 平台看不到，用户问"后台怎么没有"就这么答。
