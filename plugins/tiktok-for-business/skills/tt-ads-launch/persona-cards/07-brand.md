# 卡 7 · 品牌广告主（触达、观看）

买触达和观看的品牌和代理。竞价部分建 Reach（频控）或 Video View（6 秒）；预订（TopView、Top Feed、Pulse）只做报表和排期核对，不创建、不改、不取消。没有资产门槛，没有冷启动。

## 判定表（本次目标 + 账户状态 → 产品）

| 本次目标 | 账户状态 | 产品 | 说明 | 对用户怎么说 |
|---|---|---|---|---|
| 要触达（只说"投广告"也按这行问） | 自助账户，rf_contract_query_get 无订单 | **Reach（频控）** | 默认 | 触达广告，控制每人看几次：让尽量多的人看到，不重复轰炸 |
| 要观看 | 同上 | Video View（6 秒） | 不用 2 秒 | 观看广告，按看完 6 秒优化：找真正看进去的人 |
| 要触达，预算大或有排期 | rf_contract_query_get 有订单 | TopView / Top Feed / Pulse（预订） | 只做报表，改动走销售 | 开屏和首位这类预订广告走销售签合同，我这边只能帮你看数据，建和改要找销售 |
| 要互动、涨粉 | 任意 | Community Interaction（Engagement） | | 互动广告：涨粉或主页访问 |
| 要考虑人群 | 任意 | Consideration（按 15 秒观看或互动找"看进去的人"） | 参数见 ads-products/brand-auction.md | 考虑度广告：找真正看完、会互动的人，为后面的转化攒人群 |
| 要卖货 | 有 Shop 或 Pixel 事件 | 转卡 1 或卡 2 | 两张卡都适用，先问这次以哪边为主 | 要卖货的话走卖货广告，这次先定品牌 |

不默认推荐：把品牌 campaign 往转化目标切；2 秒观看；改或取消 R&F 订单；给预订客户推竞价替代。

## 资产清单

定方案要查的（阶段 3"你有什么"这一步查）：

| 检查 | 工具 | 缺了怎么办 |
|---|---|---|
| 账户、币种、余额 | advertiser_info_get | 余额 0：可以建，充值后再开 |
| 在跑品牌 adgroup 和近 7 / 30 天触达、频次、CPM、完播率（VTR） | report_integrated_get | 有在跑：转运营分支（operate.md） |
| 预订订单、排期、账单（大客户（KA） 用） | rf_contract_query_get、bc_invoice_get、bc_account_cost_get | 只读 |
| 并行命中：有没有转化类 campaign、Shop 或 Pixel | campaign_get、gmv_max_store_list_get、pixel_list_get | 有且他提到卖货：问这次要曝光还是卖货 |

建之前才查的（阶段 7 建草稿之前查）：

| 检查 | 工具 | 缺了怎么办 |
|---|---|---|
| 受众规模 | ad_audience_size_estimate | 太小：目标频次会失效，放宽定向 |
| 素材数和各素材 完播率（VTR） | creative_report_get、report_video_performance_get | 少于 5 条先补 |
| 行业基准 | report_ad_benchmark_get | 判断 CPM、完播率（VTR） 贵还是便宜 |

## 首投（这类广告在账户里还没建过）

1. 问清：目标（触达、观看、互动）、预算和周期、频次上限、市场。
2. 阶段 3 查到的硬阻塞没解决不往下走；建之前再查"建之前才查"的几项。只查余额和素材，没有硬阻塞。
3. 方案一句话：Reach 用频控（比如 3 天 2 次）起步，或 Video View 6 秒起步；最低成本自动出价（Lowest Cost）；有明确档期用总预算，否则日预算；素材 5 条以上。
4. 确认后建，参数见 ads-products/brand-auction.md，全部 DISABLE。
5. 读回；预览；查审核。
6. 确认后开启；次日看触达和频次。

## 运营（已经有在跑的触达或观看广告，流程见 operate.md）

这张卡特有的首因顺序，查完再按 operate.md 的通用顺序：
1. 频次过高：频次超过设的上限或受众太小（ad_audience_size_estimate），收紧频控或放宽定向
2. 完播率（VTR）掉：素材轮换，creative_report_get、report_video_performance_get
3. CPM 高于基准：report_ad_benchmark_get 对比，放宽定向或换时段
4. 预订大客户：只出预订量对实际量的完成率报表（rf_contract_query_get），改动走销售

加量：Reach 跑稳从频控切目标频次；Video View 6 秒跑稳切 15 秒；预算单次 ≤ 30%。

不做：往转化目标切；改或取消 R&F 订单；用 2 秒观看。

## 下一步触发

- Reach 跑稳 → 从频控切目标频次。
- Video View 6 秒跑稳 → 切 15 秒观看。
- 预订 大客户（KA）：出预订量对实际量、触达、频次、完播率（VTR） 的完成率报表，改动走销售。
