# 卡 2 · 独立站电商

在自己网站卖货的 DTC 卖家（Shopify、自建站、跨境）。首投先保证 Pixel 事件，再建转化；只投过 Traffic、"点击多没人买"的小客也从这里进。

## 判定表（本次目标 + 账户状态 → 产品）

| 本次目标 | 账户状态 | 产品 | 说明 | 对用户怎么说 |
|---|---|---|---|---|
| 卖货（只说"投广告"也按这行问） | Pixel 有购物事件且 7 天内触发；catalog_get 有 Feed、SKU 多 | **目录购物广告（Smart+ 带 Catalog，见 ads-products/catalog-shopping.md）** | 默认 | 带商品目录的自动投放（Smart+ 目录广告）：SKU 多时系统自动挑商品展示，前提是商品目录已同步 |
| 卖货 | Pixel 有购物事件；无 Catalog 或 SKU 少 | Website Conversions（非 Catalog） | | 网站转化广告：按网站上的购买优化，适合商品不多或没同步目录 |
| 卖货 | Pixel 有购物事件但近 7 天没触发 | 用户自述每周 ≥ 50 单：仍按购买优化建，并提醒去 Events Manager 核对回传；不到 50 单：先按加购优化 | 按账户事实说明情况 | 你说每周有 60 单，但追踪代码近 7 天没收到购买，可以先按购买优化建，同时去后台核对回传 |
| 卖货 | Pixel 没有购物事件，或没有 Pixel | Web Traffic（落地页浏览）起量，同时装 Pixel 补事件 | 不建转化 | 引流广告：先把人带到网站，让追踪代码攒到购买数据，之后再按购买优化 |
| 卖货，要控回报 | 7 天 ≥ 20 次带金额购买，tool_vbo_status_check 通过 | VBO（在上面两种之上切 optimization_goal=VALUE） | 门槛未满不切 | 按回报优化（VBO）：系统优先找买得多的人，要先有 7 天 20 次带金额的购买 |
| 卖货，成交在 TikTok Shop | gmv_max_store_list_get 有店铺 | 转卡 1 | 两张卡都适用，先问在哪成交 | 你在 TikTok Shop 成交的那部分，走店铺的自动卖货广告，下次可以单独建 |
| 曝光 | 任意 | 品牌竞价，见卡 7 | | 只要曝光的话走品牌广告 |

事件选择：优化购买（SHOPPING）要么 Pixel 近 7 天有购买回传，要么用户自述每周 ≥ 50 单；都不满足先优化加购（ON_WEB_CART）；连加购事件都没有走 Traffic。

不默认推荐：事件没回传就建转化；一上来 VBO 或 Cost Cap；SKU 多却不用 Catalog。

## 资产清单

定方案要查的（阶段 3"你有什么"这一步查）：

| 检查 | 工具 | 缺了怎么办 |
|---|---|---|
| 账户、币种、余额 | advertiser_info_get | 余额 0：可以建，充值后再开 |
| Pixel 和事件 | pixel_list_get | 没 Pixel：pixel_create 后给安装指引（Shopify 装 TikTok 应用即可）；有 Pixel 无购物事件：先补 ViewContent、AddToCart、CompletePayment，期间走 Traffic |
| Catalog 和 Feed | catalog_get、diagnostic_catalog_get | 没 Catalog 且 SKU 多：建议先建（Shopify 应用自动同步）；Feed 报错先修 |
| 在跑 campaign | campaign_get，objective_type 过滤 WEB_CONVERSIONS 和 TRAFFIC | 有：转运营分支（operate.md）；只有 App 等别的目标的 campaign 不算 |
| 并行命中：有没有可用的 TikTok Shop | gmv_max_store_list_get | 有：routing.md 交叉核对，可能转卡 1 或并行提示 |

建之前才查的（阶段 7 建草稿之前查）：

| 检查 | 工具 | 缺了怎么办 |
|---|---|---|
| 落地页可达 | tool_url_validate | 不可达先修 |
| 身份和素材 | identity_get、identity_video_get、file_video_ad_search | 无素材：建 campaign 和 adgroup，ad 等素材到了再建；无身份：按 ads-products/web-conversions.md 的身份处理 |
| VBO 资格（运营用） | tool_vbo_status_check | 不符合：继续 Conversions |

## 首投（这类广告在账户里还没建过）

1. 目标和范围：网站、主推商品或全店、日预算、目标 CPA 或 ROAS、市场。用户不懂 Pixel 时一句话解释并代查。
2. 阶段 3 查到的硬阻塞没解决不往下走；建之前再查"建之前才查"的几项。Pixel 事件决定走转化还是 Traffic；catalog_get 必须查，不能因为用户没提 Catalog 就跳过，查到有 Feed 才走 Catalog 行。
3. 方案一句话：产品（判定表那一行）、优化事件、日预算（按 routing.md 阶段 4 的区间给范围加一个推荐数，不低于 20 USD）、市场、最低成本自动出价（Lowest Cost）、一个广告组起步。Smart+ 时一并说明自动版位含 Pangle 和自动素材增强，用户可以关。
4. 确认后建，参数见 ads-products/web-conversions.md 或 web-traffic.md，全部 DISABLE。
5. 读回 campaign、adgroup、ad；creative_ads_preview_create 给预览；adgroup_review_info_get 看审核。
6. 确认后 adgroup_status_update 开启。告诉用户：次日看消耗和事件数，7 天看购买是否到 50 次，到了再改成按购买优化。

## 运营（已经有在跑的网站转化或引流广告，流程见 operate.md）

这张卡特有的首因顺序，查完再按 operate.md 的通用顺序：
1. 事件回传断：pixel_list_get 看购物事件 activity_status，有点击没购买先查这个
2. 素材疲劳：creative_report_get，CTR 降、频次升
3. 人群饱和：CPM 升、触达不涨，用 Lookalike 扩（dmp_custom_audience_lookalike_create）
4. 出价过低或 Cost Cap 卡住：消耗上不去

加量：7 天 CPA 稳定后 adgroup_budget_update 单次 ≤ 30%；预算加了量不涨就新建广告组扩人群；到"下一步触发"的数再切 VBO 或 Smart+（ads-products/smart-plus.md）。

不做：学习期换事件；只加预算不加素材；改在跑的广告组的事件或人群，要改就新建。

## 下一步触发

- 购买事件出学习期：7 天 ≥ 50 次且 CPA 稳定 → 转运营。
- 浅层事件 7 天 ≥ 50 次 → 新建 adgroup 切 SHOPPING。
- 7 天 ≥ 20 次带金额购买且 VBO 资格通过 → 新建 VBO adgroup。
- Traffic 小客：Pixel 7 天内有购买回传 → 走首投建转化，不动在跑的 Traffic。
