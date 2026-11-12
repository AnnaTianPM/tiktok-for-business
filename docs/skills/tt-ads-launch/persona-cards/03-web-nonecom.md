# 卡 3 · 非电商网站（订阅、SaaS、服务、内容、金融）

在网站上拉注册、试用、付费、订阅的广告主。没有商品和店铺。首投从注册事件起量，付费够多再切付费；金融、医疗等受限行业先看资质和审核。

## 判定表（本次目标 + 账户状态 → 产品）

| 本次目标 | 账户状态 | 产品 | 说明 | 对用户怎么说 |
|---|---|---|---|---|
| 拉注册或付费（只说"投广告"也按这行问） | Pixel 有注册或付费事件 | **Website Conversions（非 Catalog）：先优化注册；付费 7 天 ≥ 50 次再切付费** | 默认 | 网站转化广告：先按注册优化攒数据，注册够多再改按付费优化 |
| 拉注册或付费 | 无事件 | Web Traffic 起量，同时装 Pixel 和事件 | 不建转化 | 引流广告：追踪代码还没记录注册或付费，先把人引到网站，装好事件再按注册优化 |
| 拉付费，要控回报 | 付费事件带金额，7 天 ≥ 20 次，tool_vbo_status_check 通过 | VBO | 门槛未满不切 | 按回报优化（VBO）：付费带金额且 7 天有 20 次才值得切 |
| 卖机票、酒店 | 旅游行业，有 Catalog | Travel Ads（catalog_enabled） | 白名单，先读 schema | 旅游目录广告：有机票酒店目录时自动展示，需要先开通 |
| 拉 App 用户 | app_list_get 有 App | 转卡 4 | 两张卡都适用，先问主战场在网站还是 App | 你 App 那边的用户，走 App 推广，这次先定网站 |
| 曝光 | 任意 | 品牌竞价，见卡 7 | | 只要曝光的话走品牌广告 |

事件名：注册 ON_WEB_REGISTER，订阅 ON_WEB_SUBSCRIBE，付费 SHOPPING（也可自定义转化）。用户自述每周 ≥ 50 次付费就直接优化付费。

不默认推荐：事件没定义就建转化；付费不够就优化付费或 VBO；给受限行业绕审核的办法。

## 资产清单

定方案要查的（阶段 3"你有什么"这一步查）：

| 检查 | 工具 | 缺了怎么办 |
|---|---|---|
| 账户、币种、余额 | advertiser_info_get | 余额 0：可以建，充值后再开 |
| Pixel 和事件 | pixel_list_get、custom_conversion_list_get | 没注册或付费事件：给事件定义方法；必要时 custom_conversion_create |
| 行业资质 | bc_advertiser_qualification_get | 金融、医疗、借贷缺资质：先补，不建，并给合规提示 |
| Catalog（只有旅游行业要查） | catalog_get | 没有就不走 Travel Ads |
| 在跑 campaign | campaign_get，objective_type 过滤 WEB_CONVERSIONS 和 TRAFFIC | 有：转运营分支（operate.md） |
| 并行命中：有没有 App 对象 | app_list_get | 有：并行提示卡 4，问主战场在网站还是 App |

建之前才查的（阶段 7 建草稿之前查）：

| 检查 | 工具 | 缺了怎么办 |
|---|---|---|
| 文案违禁词 | blockedword_check | 命中先改 |
| 落地页可达 | tool_url_validate | 慢或跳转多先修 |
| 身份和素材 | identity_get、file_video_ad_search | 无素材先建 campaign 和 adgroup，ad 后补 |

## 首投（这类广告在账户里还没建过）

1. 问清：产品类型、目标事件（注册还是付费）、日预算、目标 CPA、市场。受限行业先说一句合规提示。
2. 阶段 3 查到的硬阻塞没解决不往下走；建之前再查"建之前才查"的几项。事件定义和资质是硬阻塞。
3. 方案一句话：Website Conversions，优化注册（或付费），最低成本自动出价（Lowest Cost），日预算按 routing.md 阶段 4 的区间给范围加一个推荐数，不低于 20 USD。
4. 确认后建，参数见 ads-products/web-conversions.md 路径 1，事件换成注册或付费，全部 DISABLE。受限行业文案先过 blockedword_check。
5. 读回；预览；查审核，被拒给原因和修法。
6. 确认后开启。告诉用户：7 天看注册是否到 50 次，到了再新建 adgroup 切付费。

## 运营（已经有在跑的注册或付费广告，流程见 operate.md）

这张卡特有的首因顺序，查完再按 operate.md 的通用顺序：
1. 审核被拒：受限行业被拒是常态，先 ad_review_info_get 读原因，修文案或落地页，必要时 adgroup_appeal
2. 事件回传断：注册或付费事件 activity_status
3. 落地页转化率：点击多注册少，先看落地页再看素材
4. 素材疲劳

加量：注册稳定后加预算 ≤ 30%；注册 7 天 ≥ 50 次再新建广告组切付费；付费带金额且资格通过再切 VBO。

不做：付费不够就切付费或 VBO；审核反复被拒还放量；给受限行业绕审核的改法。

## 下一步触发

- 注册 7 天 ≥ 50 次且 CPA 稳定 → 新建 adgroup 优化付费或订阅。
- 付费带金额 7 天 ≥ 20 次且 VBO 资格通过 → 新建 VBO adgroup。
- Traffic 小客：Pixel 有注册事件回传 → 走首投。
