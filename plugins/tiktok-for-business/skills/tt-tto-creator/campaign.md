# 2 建达人合作活动

到第 2 步才读。读 guardrails.md。产出一张活动单，建完给邀请链接。

## 先查两样

1. **品牌档案**：tto_brand_profile_get（tto_id）。有就列名字让他选；没有就建（见下）。活动级邀请链接可以不用档案只给 brand_name，品牌级（BRAND_LINK）必须有档案。
2. **要绑的广告账户**（他要达人视频拿来投才查）：auth_advertiser_get 列出，按名字选，规则同 tt-ads-launch。绑了之后达人挂链时这些账户自动拿到 Spark 授权，不用再要授权码，这是整条线最省事的一步，要主动推荐。

## 建品牌档案（没有才建）

tto_brand_profile_create：tto_id、brand_name（≤ 60 字）、brand_industry_id、brand_website（https:// 开头）、logo_url（1:1，≤ 5 MB，JPG / PNG / GIF）、tiktok_account_url（可选，https://www.tiktok.com/@ 开头，有就填，达人能看到）。

**brand_name、brand_industry_id、logo_url 建后不能改**，建之前把这三项列出来让他确认一次。brand_industry_id 的取值表以文档"Brand Profile industry IDs"为准，测试中未逐一验证；先试用 tto_creator_category_label_get 返回的 industry_labels 里的 ID，报错就让他给行业名再查。

## 活动单（建之前给他看）

| | |
|---|---|
| 活动类型 | CAMPAIGN（活动级链接，视频归到这个活动，可定向邀请）或 BRAND_LINK（品牌级链接，任何达人都能挂到你品牌下，需要品牌档案）。默认 CAMPAIGN |
| 名称 | "产品名 - 一句描述"，≤ 120 字，达人会看到 |
| 描述 | 产品定位、目标人群、核心卖点，≤ 1000 字，达人会看到 |
| 品牌 | 档案名或 brand_name |
| 绑定广告账户 | 账户名；绑了就要填授权天数 |
| 授权天数 | spark_ads_requested_authorization_days，1 到 365，默认建议 30；0 代表不自动授权 |
| 邀请达人 | handle 列表（第 1 步选的），≤ 100 个一次；留空 = 任何达人都能加入 |
| 通知达人 | send_notification true 会发站内信 |
| Anchor | 可选，见下 |

他说"建"再建：tto_campaign_create，tto_id、campaign_name、campaign_description、campaign_type、brand_profile_id 或 brand_name、advertiser_ids + spark_ads_requested_authorization_days、handle_names、send_notification、anchor_id。读回 campaign_id。

然后 tto_campaign_get，campaign_ids 填刚建的，读 invite_link、country_codes、handle_names。报告：活动建好了，邀请链接是 X，把它发给达人；绑了哪些广告账户、授权几天。

## 追加达人或广告账户

tto_campaign_update，必填 tto_id、campaign_id、campaign_type。handle_names 和 advertiser_ids 都是**追加不是替换**；handle_names 只对 CAMPAIGN 类型有效。名称、描述、品牌建后不能改。

## Anchor（他要视频下方挂网页链接才做）

tto_anchor_create：anchor_type WEB_ANCHOR、anchor_sub_type DESTINATION、anchor_title 从 WATCH_NOW / LEARN_MORE / SHOP_NOW / GET_OFFER / CONTACT_US / JOIN_NOW / APPLY_NOW 等选、anchor_name（内部名，≤ 32 字）、country_code、category_label_id（1 到 35 的品类表，如 16 美妆个护、10 食品饮料、12 服务）、call_to_action.landing_page_url（要是产品或服务详情页，否则审核不过）、upload_type UPLOAD_BY_URL + thumbnail_url（210×375，≤ 2 MB）。

**只在没有 TikTok Shop 的国家可用**：美国、英国、印尼、泰国、越南、菲律宾、马来西亚、新加坡、沙特都不行。他的市场在这几个里就说"你这个市场用不了 Anchor，达人视频里带链接要走 TikTok Shop"。anchor 只对 anchor 所在国家的观众可见。tto_anchor_get 看已有的，tto_anchor_delete 只能删 DRAFT 状态的。

## 已知坑

- tto_campaign_get 的 page_size 和 campaign_ids 都最多 5；测试账户下有近万个活动，**不要翻页找**，一律让他给活动名或 ID，或者用本次会话里建的 ID。按名字搜不支持。
- campaign_type 为 BRAND_LINK 时 handle_names 和 send_notification 无效。
- 绑了 advertiser_ids 就必须传授权天数，漏传报参数错。
- advertiser_ids 要和 TTO 账户同一个 Business Center、同一法人或同一登录邮箱。
- business_account_handle（达人点链接能直接私信品牌）是白名单功能，报错就不传。
- API 建的活动在 TTO 平台上能看到，但报表只能通过 API 看，平台上看不到。
