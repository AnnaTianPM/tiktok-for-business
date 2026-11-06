# 账号体检

到"账号体检"场景才读。目标是一张"最近 30 天"卡和一个动作建议，一条消息给完。

## 查三样，开头先说

开头一句"我去看三样：账号整体、最近的帖子、你这个行业的平均水平"，然后并行调：

1. **账号整体**：account_user_get，start_date 到 end_date 取最近 30 天（最多回看 60 天），fields 取 followers_count、daily_new_followers、daily_lost_followers、video_views、unique_video_views、profile_views、likes、comments、shares、engagement_rate、bio_link_clicks（有链接才有）。受众字段 audience_ages、audience_genders、audience_countries、audience_activity 只在粉丝 ≥ 100 时有数，粉丝少就不要。
2. **最近的帖子**：account_user_post_list_get，fields 必须含 item_id，再加 create_time、caption、media_type、video_duration、video_views、reach、likes、comments、shares、full_video_watched_rate、average_time_watched、is_ad、share_url。max_count 最大 20；要更早的用返回的 cursor 再翻一页，最多翻两页。
3. **行业基准**：account_user_benchmark_get，business_category 从他的生意里认（卖货 SHOPPING_AND_RETAIL，美妆 BEAUTY，餐饮 RESTAURANTS_AND_BARS，App SOFTWARE_AND_APPS，服务 PROFESSIONAL_SERVICES，认不出用 OTHERS）。返回的是同类账号的平均互动率、平均粉丝、平均播放等。

## 体检卡

| | |
|---|---|
| 账号 | @username，粉丝数（30 天净增 ±N） |
| 发了多少 | 30 天 N 条，视频 N 条、图文 N 条 |
| 跑得最好的 3 条 | 日期 + 文案前 20 字 + 播放 + 互动率，按播放排 |
| 互动率 | 你的 vs 行业平均（benchmark 的 average_engagement_rate），高了低了一句话 |
| 受众 | 粉丝 ≥ 100 才有：主要年龄段、性别、前 3 国家、活跃时段 |
| 流量来源 | 单条帖子的 impression_sources 有数时给：推荐页 / 关注页 / 搜索 / 主页占比 |

卡下面三句：现在什么情况；最该做的一件事（见下）；一句衔接。

## 动作建议只给一个

按命中的第一条给：

| 看到 | 建议 |
|---|---|
| 有 1 到 2 条播放明显高于其他（≥ 3 倍） | "这条可以投成广告放大" → 衔接 spark.md |
| 完播率普遍低、平均观看 < 3 秒 | 前 3 秒换钩子，视频缩到 9 到 34 秒 |
| 搜索来源占比高 | 文案里多放关键词和 hashtag → inspiration.md |
| 评论多但没回 | 去回评论 → comments.md |
| 粉丝涨但主页访问低 | 简介和置顶要能承接 |
| 30 天只发了 ≤ 3 条 | 先把发布频率提到每周 2 到 3 条 |

## 已知坑

- is_business_account 为 false 的个人号：account_user_get 和 post_list_get 都能用，但 engagement_rate 这类聚合字段可能缺；缺就自己算 (likes + comments + shares) / video_views。
- 帖子 7 天没人看过，reach、full_video_watched_rate、average_time_watched、impression_sources、audience_countries 会是空；别报成 0，说"这条最近没互动，细分数据暂时没有"。
- 帖子数据发布 365 天后停更。
- video_views 是自然 + 付费合计。is_ad 为 true 的帖子正在被广告使用，体检时标一下。
- 图文帖（media_type PHOTO）video_duration 为 0，不要拿去算完播率。
- 账号级指标有 24 到 48 小时延迟，end_date 默认是昨天。
