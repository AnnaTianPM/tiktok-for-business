# Growth Max（短剧、Series、小游戏）

当前 TikTok Ads MCP 没有 Growth Max 的创建、更新工具（tool 列表里搜不到 growth max）。本版处理：

1. 资产确认走 MCP：app_list_get、app_optimization_event_get 看付费事件回传，identity_video_get、file_video_ad_search 看切片。
2. 建投给 Ads Manager 步骤：App 推广 → Growth Max → 选类型（Mini Dramas / Series / Mini Games）→ 选剧集 → 预算和目标 ROAS 用系统推荐值 → 5 条以上切片 → 一部剧一个 campaign。建好后用 campaign_get 和 report_integrated_get 帮用户看。
3. 用户要现在用 MCP 建：短剧 App 走 ads-products/app-promotion.md 的 AEO 行，optimization_event 选付费或解锁事件；TikTok Series 和小游戏走 ads-products/smart-plus.md 的 Smart+ Minis（NATIVE_SERIES 或 MINI_GAME）。两条都说明是 Growth Max 之外的替代，效果不保证。
4. 运营只读：report_integrated_get 看各 campaign 消耗和付费 ROAS。

MCP 加了 Growth Max 工具后，把这一节换成参数表。
