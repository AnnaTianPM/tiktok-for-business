# 加热参数：Video View / Engagement 的 Spark Ad

建之前才读。这是最简的一套，只为"把一条已有帖子投出去"，不做转化目标。全部先建成暂停（operation_status DISABLE），他看过再开。

读前置：advertiser_info_get 取 currency；tool_targeting_search 用市场名（FUZZY_SEARCH）取 location_ids；identity 和 item_id 来自 spark.md 第 3 步的读回，不凭记忆。

## campaign_create

| 参数 | Video View | Engagement |
|---|---|---|
| objective_type | VIDEO_VIEWS | ENGAGEMENT |
| campaign_name | "Spark · 帖子日期 · 目标" 这类人话名，≤ 512 字 | 同 |
| budget_mode | BUDGET_MODE_INFINITE（预算放 adgroup） | 同 |
| operation_status | DISABLE | DISABLE |

不传 promotion_type。

## adgroup_create

| 参数 | Video View | Engagement |
|---|---|---|
| optimization_goal | ENGAGED_VIEW（6 秒）；他要 15 秒用 ENGAGED_VIEW_FIFTEEN | FOLLOWERS（涨粉）或 PAGE_VISIT（进主页） |
| billing_event | CPV（**只能 CPV**，传 OCPM 被拒） | OCPM |
| bid_display_mode | CPV（必传） | 不传 |
| bid_type | BID_TYPE_NO_BID | BID_TYPE_NO_BID |
| pacing | PACING_MODE_SMOOTH | PACING_MODE_SMOOTH |
| budget_mode | BUDGET_MODE_DAY | BUDGET_MODE_DAY |
| budget | ≥ 20 USD 等值，低了实测被拒 | 同 |
| schedule_type | SCHEDULE_FROM_NOW；他给了档期用 SCHEDULE_START_END + schedule_end_time | 同 |
| schedule_start_time | **任何 schedule_type 都必传**，UTC `YYYY-MM-DD HH:MM:SS`，现在开始就填当前 UTC 时间 | 同 |
| location_ids | tool_targeting_search 读回 | 同 |
| placement_type | PLACEMENT_TYPE_NORMAL | 同 |
| placements | ["PLACEMENT_TIKTOK"] | 同 |
| operation_status | DISABLE | DISABLE |

人群默认放宽（不传年龄、性别、兴趣）；他点名要收窄才加。先读 adgroup_create 的 schema 再填，必填项以 schema 为准。

## ad_create

一条帖子一个 ad，Spark Ads Pull 模式：

| 参数 | 值 |
|---|---|
| adgroup_id | 上一步读回 |
| creatives[0].ad_name | 人话名或 ""（自动用 ad_id） |
| creatives[0].ad_format | SINGLE_VIDEO |
| creatives[0].identity_type | TT_USER / BC_AUTH_TT / AUTH_CODE，按 spark.md 第 3 步找到的那一个 |
| creatives[0].identity_id | 同上 |
| creatives[0].identity_authorized_bc_id | identity_type 为 BC_AUTH_TT 时必传 |
| creatives[0].tiktok_item_id | 帖子 item_id。AUTH_CODE 必传；TT_USER / BC_AUTH_TT 传它就不传 video_id 和 image_ids |
| creatives[0].ad_text | 可不传，用帖子原文案；他要改文案才传，≤ 100 字无 emoji |
| creatives[0].call_to_action | Engagement + PAGE_VISIT 时配合 tiktok_page_category PROFILE_PAGE；Video View 可不传 |
| creatives[0].tiktok_page_category | optimization_goal 为 PAGE_VISIT 时必传，默认 PROFILE_PAGE |
| creatives[0].operation_status | DISABLE |

Spark Ad 不传 image_ids、video_id、landing_page_url。dark_post_status 默认 ON，帖子本来就在他主页上，不用改。

## 读回

campaign_get、adgroup_get、ad_get 各读一次，核对：objective、optimization_goal、budget 和币种、location、tiktok_item_id、identity、三层都是 DISABLE。ad_review_info_get 看审核状态，审核中就说"审核一般几小时内"。

## 已知坑

- Video View 的 billing_event 只能 CPV；bid_display_mode CPV 漏传会报参数错。
- 日预算低于 20 USD 等值被拒，报下限让他定，不自己抬；总预算下限随天数涨（USD 账户 7 天 140）。
- schema 标注非 CBO 下 REACH / VIDEO_VIEWS / ENGAGEMENT 的 BUDGET_MODE_DAY 已 deprecated，推荐的 BUDGET_MODE_DYNAMIC_DAILY_BUDGET 是白名单；实测 BUDGET_MODE_DAY 仍可用。被拒就改 BUDGET_MODE_TOTAL + SCHEDULE_START_END，总预算 = 日预算 × 天数。
- schedule_start_time 漏传直接报必填错，SCHEDULE_FROM_NOW 也要。
- 这两类目标不要往转化目标切，换目标等于重建。
- Engagement + PAGE_VISIT 漏传 tiktok_page_category 会在 ad_create 报错。
- 新广告账户（2026-01-15 之后建的）不能用 CUSTOMIZED_USER 身份建非 Spark 的 TikTok 版位广告，本 Skill 只建 Spark Ad，不受影响；但不要把 CUSTOMIZED_USER 当兜底。
