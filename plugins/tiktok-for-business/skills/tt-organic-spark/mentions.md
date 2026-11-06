# 被提及监控：谁在说我们

到"被提及监控"场景才读。全部在 Social Organic MCP，**只对 Business Account 有数据**；个人号第一次进来就说"你的账号不是 Business Account，这部分拿不到，要先在 TikTok 里切成商家账号"，然后不再提。

## 一张"最近 90 天提及"卡

开头说"我去看三样：谁 @ 了你、评论里谁提你、大家配什么词"，并行调：

1. account_user_mention_post_list_get，fields 取 item_id、create_time、caption、likes、comments、shares、views、creator_handle_name、video_link；number_of_days 90；sort_field LIKES；max_count 20。
2. account_user_mention_comment_list_get，fields 取 comment_text、comment_likes、commenter_display_name、video_link、comment_create_time；sort_field COMMENT_LIKES；max_count 20。
3. account_user_mention_top_hashtag_list_get 和 account_user_mention_top_word_list_get，各取前 20。

卡：提及帖子数、总播放、点赞最高的 3 条（谁、文案前 20 字、数据、链接）；评论提及数和最热 3 条；前 10 个 hashtag 和前 10 个词。下面两句：这些内容里哪几条值得去互动或要授权（衔接：要拿别人的帖子投广告要授权码，走 spark.md 第 3 步的授权码路径）；哪几个词可以进你自己的文案。

## 品牌 hashtag

他想长期追某几个 hashtag：

1. account_user_mention_hashtag_verify_list_get（username）看哪些 hashtag 合格（至少出现在 3 条相关帖子里）。
2. account_user_mention_hashtag_add（username，hashtags ≤ 10 个一次，总共 ≤ 50 个），含完整 handle 的 hashtag 不用验证。说一句"开通后 24 小时才有数据，7 天内不能删"。
3. 之后用 account_user_mention_hashtag_video_list_get 看带这些 hashtag 的帖子，可按单个 hashtag 过滤（大小写敏感）。account_user_mention_hashtag_manage_list_get 看已开通的，account_user_mention_hashtag_delete 删。

## 已知坑

- 新账号、测试账号没有提及数据，verify_list 会空，不要当工具坏了。
- 提及只算公开帖、90 天内、发帖人不是未成年；返回最多 1000 条，按点赞取。
- 只有 @ 没有其他文字的评论会被降权。
- regions 过滤要用文档里的地区码，不确定就不传。
