# 评论运营：自己帖子 + 广告下的评论

到"评论运营"场景才读。两个来源合在一个流程里，用户不用分清哪条是广告评论。

## 1 拉评论

开头说一句"我去拉你最近帖子和广告下面的评论"。

- **自己帖子的评论（Organic）**：先 account_user_post_list_get 取最近 10 条帖子的 item_id 和 comments 数，只对 comments > 0 的帖子调 account_user_comment_list_get：video_id、include_replies true、status ALL、sort_field likes、sort_order desc、max_count 30。超过 500 条的帖子只拿前 500。
- **广告下的评论（Ads）**：有广告账户才查。comment_list_get 必填 search_field ADGROUP_ID + search_value + start_time / end_time（**时间窗 ≤ 30 天**），adgroup_id 从 adgroup_get 取在跑的；返回里每行带 comment_id、ad_id、tiktok_item_id，后面回复要用同一行的三个 ID。没有在跑的广告就跳过，说一句。
- 他只说了某一条帖子就只拉那一条。

## 2 分类

每条评论归一类，一张表给他，每类最多列 5 条，其余给数量：

| 类 | 判断 | 建议动作 |
|---|---|---|
| 咨询 | 问价格、怎么买、发货、尺码、链接 | 回复，文案带答案 |
| 好评 | 夸、想要、tag 朋友 | 点赞，挑 1 到 2 条回一句 |
| 负面 | 质量、服务、退款投诉 | 回复致歉 + 引导私信，不隐藏 |
| 垃圾 / 违规 | 广告、刷屏、辱骂、无关链接 | 隐藏 |
| 其他 | 认不出 | 不动 |

## 3 执行

**回复文案一律先给他看，他说"发"再发。**一条消息列出要发的每条回复（评论原文 + 回复文案），他确认后：

- Organic：account_user_comment_reply_create，video_id + comment_id + text（≤ 1200 字）。点赞 account_user_comment_like_update LIKE。隐藏 account_user_comment_visibility_update HIDE（别人的评论只能隐藏不能删；自己发的才能 account_user_comment_delete）。
- Ads：comment_post_create，advertiser_id、ad_id、tiktok_item_id、comment_id 来自 comment_list_get **同一行**，comment_type REPLY，identity_type 只能 TT_USER 或 CUSTOMIZED_USER（BC_AUTH_TT 被拒），identity_id 从 identity_get 过滤。只能回一级评论。隐藏 comment_status_update，operation HIDDEN，comment_ids 可批量。
- 回复文案要一条一条不一样。短时间内发大量相似内容会被判垃圾直接隐藏，而且不会有通知。超过 10 条回复就分两轮。

做完报告：回了几条、隐藏了几条、哪条失败和为什么。

## 已知坑

- comment_post_create 报 "Internal error." 52404 是 comment_id / ad_id / tiktok_item_id 三者对不上，不是服务挂了；重新从 comment_list_get 同一行取，不要重试同一请求。
- 隐藏的评论里包含系统隐藏的（审核、隐私设置），unhide 可能不生效，读回 status 再说结果。
- account_user_comment_reply_list_get 不支持对已隐藏评论拉回复。
- 评论 webhook（5 分钟内通知）本 Skill 不配置，用户问"能不能自动提醒"就说走 webhook 需要开发对接。
