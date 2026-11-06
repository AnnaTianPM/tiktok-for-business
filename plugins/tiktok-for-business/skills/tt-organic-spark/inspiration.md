# 内容灵感：发什么、带什么词、配什么音乐

到"内容灵感"场景才读。全部只读，一条消息给一张表。先问一句他的品类或关键词（他开场说了就不问）。

| 他要 | 工具 | 怎么用 |
|---|---|---|
| 现在什么热 | discovery_search，is_personalized true 给他账号相关的，false 给全站前 20 | 列前 10 条，标哪几条和他品类相关 |
| 文案带什么 hashtag | account_user_hashtag_suggestion_get，keyword 他的品类词，language 跟他市场 | 给 10 个，带 post_count 和 view_count，分"大词 3 个 + 精准词 5 个" |
| 行业热门 hashtag（Ads 侧） | discovery_trending_list，**默认不调**：返回 200 条含 7 天趋势和示例视频，实测约 48 万字符，没有分页参数 | 他点名要行业榜才调，调了只取前 10 条 hashtag 名和播放数，其余丢弃 |
| 配什么音乐 | discovery_cml_list_get，country_code 他的市场，genre 他点名才传，date_range 7DAY | **返回 100 条约 12 万字符，只看前 10 条**：artist、曲名、rank_position、时长；告诉他这些是商用音乐库里预先授权的，发帖和广告都能用；music_sound_id 留给他发帖时用 |
| 看某条热门视频长什么样 | discovery_detail_get / discovery_video_list（Ads 侧，按 hashtag） | 给 3 条链接 |

输出后一句衔接："要不要我按这些词给 3 个开头钩子？"他要就给，每个一句钩子 + 一句脚本骨架；不要就停。

## 已知坑

- discovery_cml_list_get 约 12 万字符、discovery_trending_list 约 48 万字符，都没有分页；不要全量贴给用户，也不要让它进第二轮上下文，各取前 10 条就够。
- discovery_search 的 is_personalized true 需要 Business Account 数据，个人号可能和 false 一样。
- hashtag_suggestion 的 language 默认 en，他市场是日本、东南亚要传对应值，否则推荐全是英文。
