# Lead Generation（表单、消息、来电）

读前置：advertiser_info_get 币种；term_check 线索条款；page_get（business_type LEAD_GEN，status PUBLISHED）取 page_id；pixel_list_get 取 FORM 事件；tool_targeting_search 取 location_ids；identity_get 身份。

## campaign_create

objective_type LEAD_GENERATION；budget_mode BUDGET_MODE_INFINITE；operation_status DISABLE；request_id。

## adgroup_create

| 路径 | 参数 |
|---|---|
| Instant Form（站内表单） | promotion_type LEAD_GENERATION；promotion_target_type INSTANT_PAGE；optimization_goal LEAD_GENERATION；billing_event OCPM；不传 pixel_id；ad 层用 page_id |
| Web Form（网站表单） | promotion_type LEAD_GENERATION；promotion_target_type EXTERNAL_WEBSITE；optimization_goal CONVERT + pixel_id + optimization_event FORM；billing_event OCPM。没有 FORM 事件只能 optimization_goal CLICK（不传 pixel），这时不如 Instant Form |
| TikTok 私信（1P） | promotion_type LEAD_GEN_CLICK_TO_TT_DIRECT_MESSAGE；optimization_goal 默认 CLICK；用账户已绑的 TikTok 身份。只对 APAC、LATAM 注册的广告主开放，其他地区白名单 |
| 第三方消息（3P：WhatsApp、Messenger、Zalo、LINE） | promotion_type LEAD_GEN_CLICK_TO_SOCIAL_MEDIA_APP_MESSAGE；optimization_goal CONVERSATION（按开聊优化）或 CLICK；messaging_app_type 决定账号参数：WHATSAPP 传 phone_region_code + phone_region_calling_code + phone_number（tool_phone_region_code_get 取区号，号码要和 MMT 绑的一致）；MESSENGER 传 messaging_app_account_id = Facebook Page ID；LINE 传 LINE Business ID；ZALO 传 Official Account ID 或电话。CONVERSATION 时不能选 LINE、IM_URL，且可能要 message_event_set_id（ctm_message_event_set_get 查 matched_event_set）。只对 APAC 注册的广告主开放 |
| 来电 | promotion_type LEAD_GEN_CLICK_TO_CALL；optimization_goal CLICK |

共用：bid_type BID_TYPE_NO_BID + pacing PACING_MODE_SMOOTH；budget_mode BUDGET_MODE_DYNAMIC_DAILY_BUDGET，budget ≥ 20 USD；schedule SCHEDULE_FROM_NOW + 当前 UTC；location_ids；placement_type PLACEMENT_TYPE_NORMAL + ["PLACEMENT_TIKTOK"]；operation_status DISABLE；request_id。

## 多门店（Multiple Location，PRD 约 1%）

MCP 里没有单独的多门店工具。做法：一个 campaign 下按门店各建一个广告组，location_ids 用 tool_targeting_search 查到的城市或 zipcode_ids（美国支持邮编），表单或来电按上面的路径，名称带门店名。门店资产（Business Center 里的门店列表）能否直接引用待验证，查不到就按上面手工分组。

## Auto Ads（汽车库存广告，白名单）

campaign_create objective_type LEAD_GENERATION 或 WEB_CONVERSIONS，catalog_enabled=true（schema 写明只对 Automotive Ads 用），需要车源目录（catalog_get 看有没有汽车类目录）。adgroup 和 ad 层的车源参数先读 schema；创建被拒（权限类）就停，告诉用户要先开通，这次按表单或来电走。

## Instant Form 不存在时

MCP 没有建表单的工具。替用户写好表单：标题、3 到 5 个问题（姓名、电话、一个筛选问题）、隐私政策链接、感谢语。让用户在 Ads Manager 的 Instant Form 编辑器里建好并发布，再 page_get 确认拿到 page_id。campaign 和 adgroup 可以先建，ad 等表单。

## ad_create

Instant Form：creative_list 里带 page_id、video、identity、ad_text、call_to_action。Web Form：landing_page_url 为表单页。先读 schema 再填。

## 线索导出

lead_get 按 page_id 或 adgroup 读；大量用 page_lead_task_create + page_lead_task_download。接 CRM：crm_list_get 看有没有，crm_create 建事件集，之后才谈按质量优化。

## 已知坑

- 线索条款没接受，create 直接失败；term_confirm 要用户明确同意。
- 表单字段多于 5 个线索量明显掉。
- Smart+ Lead（smart_plus_campaign_create objective LEAD_GENERATION）放在运营阶段，首投不用。
