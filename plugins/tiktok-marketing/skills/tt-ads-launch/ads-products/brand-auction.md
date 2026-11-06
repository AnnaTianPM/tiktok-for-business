# 品牌竞价（Reach、Video View、Engagement）和预订（只读）

读前置：advertiser_info_get 币种；tool_targeting_search 取 location_ids；ad_audience_size_estimate 受众规模；identity_get 身份。

## campaign_create

objective_type REACH / VIDEO_VIEWS / ENGAGEMENT；budget_mode BUDGET_MODE_INFINITE；operation_status DISABLE；request_id。这三个目标的 adgroup 不传 promotion_type。

## adgroup_create

| 路径 | 参数 |
|---|---|
| Reach 频控 | optimization_goal REACH；billing_event CPM；frequency + frequency_schedule（例：2 和 3 = 3 天最多 2 次） |
| Video View 6 秒 | optimization_goal ENGAGED_VIEW；billing_event CPV；bid_display_mode CPV（必传）；15 秒用 ENGAGED_VIEW_FIFTEEN |
| Engagement 涨粉 / 主页访问 | optimization_goal FOLLOWERS 或 PAGE_VISIT；billing_event OCPM |
| Consideration 考虑度 | 没有单独的 objective。用 VIDEO_VIEWS + optimization_goal ENGAGED_VIEW_FIFTEEN（15 秒）起，或 ENGAGEMENT + FOLLOWERS，按用户要"看进去"还是"互动"选；Product Tag 里的 BA Consideration 对应哪个 optimization_goal 待验证，第一版按 15 秒观看建 |

共用：bid_type BID_TYPE_NO_BID + pacing PACING_MODE_SMOOTH（用户要控 CPM 或 CPV 才 BID_TYPE_CUSTOM + bid_price，数值先 tool_bid_recommend 取，取不到就问用户）；budget_mode 用 BUDGET_MODE_DAY（这三个目标的动态日预算是白名单）或有档期用 BUDGET_MODE_TOTAL + SCHEDULE_START_END；日预算 ≥ 20 USD，Video View 实测低于 20 被拒，总预算 ≥ 20 × 天数；location_ids；placement_type PLACEMENT_TYPE_NORMAL + ["PLACEMENT_TIKTOK"]；operation_status DISABLE；request_id。

## ad_create

同 web-conversions.md，品牌广告常用 Spark Ad（tiktok_item_id + identity）。先读 schema。

## 预订（TopView、Top Feed、Pulse、R&F）

只读：rf_contract_query_get 订单和合同；report_integrated_get 实际触达、频次、VTR；bc_invoice_get、bc_account_cost_get 账单。输出预订量对实际量的完成率。

不做：adgroup_rf_create、adgroup_rf_update、rf_order_cancel。用户要改排期或取消，告诉他走 TikTok 销售。

## 已知坑

- Video View 的 billing_event 只能 CPV，传 OCPM 会被拒。
- Reach 的 frequency 上限：每天不超过 4 次；frequency_schedule ≤ 30 天。
- 这三类目标不要往转化目标切，换目标等于重建。
