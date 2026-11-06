# 选帖加热：从帖子到一条在跑的 Spark Ad

到"选帖加热"场景才读。主线跨两个 connector：挑帖子和开授权在 Social Organic，身份核对和建广告在 Ads。分 5 步，每步一条消息、一个产出、最多一个问题。他指定了帖子就跳过第 1 步；他说"直接建"就把 1 到 3 合成一条。

## 1 挑帖子

先问目标（他说了就不问）："这次是想让更多人看到，还是想涨粉 / 让人进主页？"前者走 Video View，后者走 Engagement。要卖货、装 App、收表单的，告诉他那是转化广告，走 tt-ads-launch，本 Skill 挑好的帖子可以带过去。

然后拉候选：

1. 先试 account_user_post_recommend_get，objective_type 按目标（VIDEO_VIEWS / ENGAGEMENT），time 默认 PAST_THREE_MONTHS。成功就用它的 recommendation_level 排序。
2. **报 40130（没授权这个 scope）或空结果就退回手工排**：account_user_post_list_get 取最近 20 条，fields 含 item_id、caption、media_type、video_duration、video_views、reach、likes、comments、shares、full_video_watched_rate、is_ad。排除 media_type PHOTO（Spark Ad 轮播另有流程，第一版不做）和 is_ad 为 true 的。排序：Video View 目标按 full_video_watched_rate 再按 video_views；Engagement 目标按 (likes + comments + shares) / video_views。
3. 候选表给 3 条：日期、文案前 20 字、时长、播放、互动率、一句为什么。竖屏 9 到 34 秒优先；说明你看不到画面，是按数据挑的。

一个问题：投哪一条？他说"你定"就取第一条。

## 2 开广告授权（Organic 侧）

对选定的 item_id：

1. account_user_post_authorize_status_get。返回 40002 "No authorization code exists" 就是没开过；有返回就看状态和到期时间。
2. 没开过或已过期：account_user_post_authorize_setting_update，is_ad_promotable true，authorization_days 默认 30（可选 7、30、60、180、365）。告诉他一句"开了之后帖子状态会变成'可用于广告'，TikTok 会审核一次"。
3. 再 account_user_post_authorize_status_get 读回授权码（authorization code）和到期时间，记下来给第 3 步用。
4. 已经在投的帖子不能关授权；要延期用 account_user_post_authorize_update。

## 3 核对身份（Ads 侧）

先定广告账户：auth_advertiser_get，一个直接用，多个按名字让他选（规则同 tt-ads-launch）。advertiser_info_get 读币种和状态。

然后找能用这条帖子的身份，按顺序：

1. identity_get 带 advertiser_id，**一定传 identity_type 过滤**（先 TT_USER，再 BC_AUTH_TT + identity_authorized_bc_id）。不传类型时它一次返回全部身份、page_info 全 0，测试账户下 127 个里 125 个是 BC_AUTH_TT；传了类型分页才正常。在结果里找 username 等于他账号 username 的那一个。找到：identity_video_get 用这个身份 + item_type VIDEO 翻一下，确认 item_id 在列表里（cursor 分页，count ≤ 20）。
2. 没有对应身份：走授权码。tt_video_authorize_apply 带 advertiser_id + 第 2 步的 auth_code（码里的 + 换成 %2B）；成功后 tt_video_info_get 读帖子信息；然后 identity_get 过滤 identity_type AUTH_CODE 找到新出现的那条身份。tt_video_list_get 可以看这个账户下所有已授权帖子。
3. 两条路都走不通：说清卡在哪（账号没绑到这个 Business Center、授权码还在审核），不编身份 ID。

这一步的产出：一句"用 @xx 这个身份，帖子已经能在广告账户里看到"，然后问："现在建吗？建好是暂停的，你看过再开。"他前面说过"直接建"就不问。

## 4 建加热（Ads 侧）

读 boost-params.md 和 guardrails.md。一条消息先列要建的：目标、预算和币种、市场、时长、用哪条帖子、全部暂停；然后建 campaign → adgroup → ad，逐个读回（campaign_get、adgroup_get、ad_get），核对 tiktok_item_id 和 identity 是不是第 3 步那一个，查审核（ad_review_info_get）。报告：建好了什么、都是暂停、还差什么才能开。

预算不算公式：Video View 和 Engagement 新手 20 到 50 美元一天跑 7 天，换算成账户币种取整，说"大多数人从 X 起步，你定"。低于 20 USD 实测会被拒。

## 5 开和看

只在他明确说"开"之后：摘要一句（名称、预算、币种、市场、开了就花钱），他说是，自上而下 campaign_status_update → adgroup_status_update → ad_status_update 到 ENABLE，哪层失败停下来报。

开了之后他问效果，一条消息三样并行：

- **付费侧**：creative_report_get，report_type VIDEO_INSIGHT，material_type VIDEO，**start_date 和 end_date 必传**（开启日到今天，lifetime true 也要传），filtering.tiktok_item_ids 填这条帖子，metrics_fields 取 spend、impressions、video_play_actions、video_watched_6s、video_views_p100、clicks、ctr、cpm。
- **掉点**：report_video_performance_get，report_type VIDEO，filtering.video_ids 填 Ads 侧的 video_id（ad_get 读回里有），metrics_fields retain、drop_off、ctr。
- **自然侧**：account_user_post_list_get，filters.video_ids 填 item_id，看 video_views（这是自然 + 付费合计）、likes、comments、new_followers 和开之前的差。

输出一张"自然 vs 付费"表：付费带来多少播放、每千次多少钱、6 秒观看率、哪一秒掉得最多；自然侧涨了多少互动和粉丝。一个动作：掉点在前 3 秒就换钩子；6 秒观看率低于行业就换帖子；都好就提"预算可以加 20% 到 30%"。

## 已知坑

- account_user_post_recommend_get 在没授权对应 scope 的账号上报 40130，个人号大概率如此，直接退回手工排，不要重试。
- 授权码审核期间 tt_video_authorize_apply 可能报"码无效"，等审核过再试；码里的 + 一定换 %2B。
- identity_get 不传 identity_type 时分页无效（page_info 全 0），一次 127 条起步；传了 identity_type 分页正常。不要把原始列表给用户看。
- creative_report_get 即使 lifetime true 也要传 start_date 和 end_date，否则报 40002；日期用广告账户时区。
- account_user_post_authorize_setting_update 是写操作，部分客户端会先弹权限确认；读回格式（授权码字段名）本版未实测，以 account_user_post_authorize_status_get 实际返回为准。
- identity_video_get 对 TT_USER / BC_AUTH_TT 的 cursor 是时间戳，对 AUTH_CODE 是分页游标；keyword 只在 AUTH_CODE 下能用。
- 图文帖（CAROUSEL）做 Spark Ad 的 ad_format 是 CAROUSEL_ADS，参数不同，第一版不做，说明一句。
- 帖子 is_ad 为 true 时授权关不掉，要先暂停用它的广告。
