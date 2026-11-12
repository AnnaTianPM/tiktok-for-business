# 1 找达人

到第 1 步才读。产出一张候选表和一个问题。

## 先问三件（他开场说了的不问）

1. 推什么、给谁看（品类 + 市场国家）。
2. 要多大的达人（粉丝量级或预算档；不知道就按 1 万到 50 万中腰部起）。
3. 要什么感觉的内容（教程、测评、日常、搞笑；不知道就按品类默认）。

一条消息问完，每题一句，带"不确定就…"。

## 搜

开头说"我去按你的品类和市场搜一轮，再挑几个看细"。

1. **拿标签**：tto_creator_category_label_get，label_type SEARCH。返回 industry_labels（达人接过哪类商单，如 14000000000 美妆个护、14103000000 护肤）和 content_labels（达人日常发什么，如 11002002 美妆教程、11010004 做饭）。按他的品类各挑 1 到 3 个 ID。
2. **搜**：tto_creator_discover，必填 tto_id + country_codes（**必传，多个国家要同一区域**）。常用：industry_label_ids、content_label_ids、min_followers / max_followers、min_engagement_rate（0 到 1，0.03 起算不错）、min_median_views、min_creator_price / max_creator_price（USD）、follower_country_codes（他要受众在哪就填哪）、follower_gender_ratio、follower_age、languages、keyword_search（模糊）。sort_field 按他要的：ENGAGEMENT_RATE 要互动、MEDIAN_VIEWS 要稳定播放、FOLLOWERS 要量级。page_size 先 10，最多 200，总共最多 1000。
3. 返回每条只有 handle_name、display_name、followers_count、likes_count、videos_count。**互动率、中位播放、价格要深看才有。**

## 深看 3 到 5 个

对候选里最像的 3 到 5 个，并行调 tto_creator_public_get（handle_name 精确匹配，不是 TTO 达人会报错）。拿：

- engagement_rate、median_views、followers_count
- creator_price + currency（0 代表没公开报价）
- audience_ages / audience_genders / audience_countries（粉丝画像）和 engaged_audience_*（真正互动的人的画像，更有用）
- reached_audience_followers（看他视频的人里多少不是粉丝，高说明有破圈能力）
- content_labels、industry_labels、creator_labels（如 HIGH_POTENTIAL_TO_DRIVE_SALES 是系统标的带货潜力）
- bio（常带合作邮箱）

要看他最近发什么：tto_creator_public_video_list_get，limit 3 到 5，看 caption、video_views、likes、mentioned_accounts（带了哪些品牌，说明接过谁的单）、collaboration_status。

## 美国市场加一张排行榜

country_codes 是 US 时可以加：tto_creator_category_label_get 换 label_type RANKING 拿排行榜标签（比 SEARCH 少，只有部分行业和内容类），再 tto_creator_rank_scoreboard_get：country_code US、ranking_type BRANDED_CONTENT（按商单内容排）或 ORGANIC_CONTENT、label_id、time_period MONTH、time_period_lookback ONE、page_size 10。返回带 score、starting_price（起步价，USD）、branded_content_engagement_rate、ranking_change。**只有美国有**，返回的 last_updated_at 可能是几个月前，说一句。

## 核对他自己带来的名单

他给了 handle：tto_creator_status_get，handle_names ≤ 20 个一次，返回 IN / NOT_IN。NOT_IN 的不能通过 TTO 邀请和授权，说清"这几个还没加入 TikTok One，要他们先加入，或者走线下授权码"。

## 候选表

| @handle（显示名） | 粉丝 | 中位播放 | 互动率 | 起步价 | 受众（主要年龄 / 性别 / 国家） | 近期内容一句 | 为什么推 |
|---|---|---|---|---|---|---|---|

3 到 5 行，按他最在意的那一列排。表下一个问题："这几个里先邀请谁？"或"要不要换一组条件再搜？"

## 已知坑

- tto_creator_discover 偶发超时（"server isn't responding"），缩小 page_size 到 3 到 5 重试一次就好；不要连续重试。
- country_codes 多个时必须同一区域，不确定就一次一个国家。
- tto_creator_public_get 对非 TTO 达人直接报错，先 tto_creator_status_get 核对。
- discover 返回的 total_number 上限 1000，不代表只有这些人。
- creator_price 为 0 不是免费，是没公开。
- 排行榜 post_count、follower_growth 可能为 0 / null，不要当成"没发过帖"。
