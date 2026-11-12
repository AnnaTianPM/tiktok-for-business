# 卡 5 · 内容型 App（短剧、TikTok Series、小游戏）

短剧、Series、小游戏发行方，一部剧一个 campaign，几乎全是新客。正常路径是 Growth Max 托管投放。

**本版限制**：当前 TikTok Ads MCP 没有 Growth Max 的创建工具，不要用 campaign_create 硬凑。能做什么、怎么给 Ads Manager 步骤、怎么过渡，见 ads-products/growth-max.md。

## 判定表（本次目标 + 账户状态 → 产品）

| 本次目标 | 账户状态 | 产品 | 说明 | 对用户怎么说 |
|---|---|---|---|---|
| 推短剧或小游戏（只说"投广告"也按这行问） | App 已绑，付费事件回传 | **Growth Max（Mini Dramas / Mini Games）**，一部剧一个 campaign | 默认；MCP 建不了，给 Ads Manager 步骤 | 短剧和小游戏的托管投放（Growth Max），一部剧一个计划：目前要在广告后台建，我把步骤给你 |
| 推站内付费剧集 | 有 Series 资产 | Growth Max Series | 同上 | 站内付费剧集的托管投放（Growth Max Series），同样在后台建 |
| 推短剧或小游戏，要现在就用 MCP 建 | 付费事件回传 | 短剧 App：普通 App Promotion AEO 过渡（ads-products/app-promotion.md）；Series 和小游戏：Smart+ Minis（ads-products/smart-plus.md） | 用户同意后才走，说明不如 Growth Max | 先用普通 App 推广按付费优化过渡：现在就能建，但效果不如托管投放 |
| 推短剧或小游戏 | 付费事件没回传 | 先接 MMP，什么都不建 | | 付费事件还没回传给 TikTok，先接上归因平台，不然系统不知道谁在付费 |
| 新剧上线要曝光 | 任意 | 品牌竞价 Video View，见卡 7 | | 新剧上线要曝光的话走品牌观看广告 |

不默认推荐：一个 campaign 投多部剧；预算低到攒不出付费；频繁改目标 ROAS。

## 资产清单

定方案要查的（阶段 3"你有什么"这一步查）：

| 检查 | 工具 | 缺了怎么办 |
|---|---|---|
| 账户、币种、余额 | advertiser_info_get | 余额 0 提示充值 |
| App 对象和付费事件 | app_list_get、app_optimization_event_get | 付费事件没回传：先接 MMP，不建 |
| TikTok Series（站内付费剧集）资产 | identity_native_series_get | 没有就不走 Series 行 |
| 在跑 campaign 和表现 | campaign_get、report_integrated_get | 有：转运营分支（operate.md） |

建之前才查的（阶段 7 建草稿之前查）：

| 检查 | 工具 | 缺了怎么办 |
|---|---|---|
| 内容切片 | identity_video_get、file_video_ad_search | 无切片：先做 5 条高光切片 |

## 首投（这类广告在账户里还没建过）

1. 问清：投哪部剧、目标（付费还是安装）、日预算、目标 ROAS、市场。
2. 阶段 3 查到的硬阻塞没解决不往下走；建之前再查"建之前才查"的几项。付费回传是硬阻塞。
3. 说清两条路（步骤见 ads-products/growth-max.md）：Growth Max 去 Ads Manager 建；或现在用 MCP 建普通 App Promotion AEO 过渡。让用户选。
4. 选过渡才建，参数见 ads-products/app-promotion.md AEO 行，一部剧一个 campaign，全部 DISABLE。
5. 读回；查审核。
6. 确认后开启；次日看消耗和付费 ROAS。

## 运营（已经有在跑的剧集或小游戏广告，流程见 operate.md）

这张卡特有的首因顺序，查完再按 operate.md 的通用顺序：
1. 内容状态：剧集下架、Series 不可用（identity_native_series_get）
2. 切片疲劳：同一批切片跑超过 1 周，换 5 条新高光
3. ROAS 目标过高：付费 ROAS 比 30 天均值低 20% 先换切片，再看目标

Growth Max campaign 的预算和目标在 Ads Manager 改，MCP 只读报表（report_integrated_get）；Smart+ Minis 和普通 App 推广按通用动作改。加量优先加剧集、多剧集并行，预算单次 ≤ 30%。

不做：一个 campaign 投多部剧；频繁改目标 ROAS；预算低到攒不出付费。

## 下一步触发

- 连续 3 天消耗且 ROAS 在区间 → 加预算、加剧集。
- ROAS 比 30 天均值低 20% → 换切片、查内容状态。
