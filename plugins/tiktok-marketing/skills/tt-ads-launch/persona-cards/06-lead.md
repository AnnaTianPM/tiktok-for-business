# 卡 6 · 线索收集（表单、消息、来电、到店）

收表单、咨询、预约、到店的服务型广告主：教育、本地服务、金融、医疗、汽车。没有商品和 App。没落地页用 Instant Form，有落地页加 Pixel 用 Web Form。汽车经销商有车源目录且开通了 Auto Ads 走库存广告，否则按表单或来电走。

## 判定表（本次目标 + 账户状态 → 产品）

| 本次目标 | 账户状态 | 产品 | 说明 | 对用户怎么说 |
|---|---|---|---|---|
| 收表单（只说"投广告"也按这行问） | 没有自有落地页 | **Lead Generation · Instant Form（站内表单）** | 默认；不需要 Pixel | 站内表单广告（Instant Form）：用户不离开 TikTok 就能填，不需要你有网站 |
| 收表单 | 有落地页，Pixel 有表单事件（FORM）或可补 | Lead Generation · Web Form（网站表单） | 质量更可控 | 网站表单广告（Web Form）：把人带到你网站填表，质量更可控，前提是追踪代码能记录表单提交 |
| 收表单 | 有落地页但无 Pixel | Instant Form 先起量，同时装 Pixel | 不选 Web Form | 你有网站但没装追踪代码，先用站内表单起量，同时把代码装上 |
| 收消息、来电、到店 | 任意；多门店要门店资产 | Lead Generation · 消息 / 来电 / 多门店 | 消息类有地区限制，多门店待验证，见 ads-products/lead-gen.md | 消息或来电广告：点一下就聊或打电话，适合要马上沟通的生意；多家门店可以按门店就近投 |
| 卖车，有库存 | 汽车行业，Catalog 有车源 | Auto Ads（汽车库存广告） | 白名单功能，见 ads-products/lead-gen.md；没开通就按表单或来电走 | 汽车库存广告：按你库存里的车型自动展示给附近有购车意向的人，要先开通并同步车源目录 |
| 量够但质量差 | crm_list_get 无 CRM | 先接 CRM 回传，再优化质量 | 不先承诺质量 | 线索够但质量差：先把 CRM 的有效线索回传给 TikTok，系统才能学会找好线索 |
| 曝光 | 任意 | 品牌竞价，见卡 7 | | 只要曝光的话走品牌广告 |

不默认推荐：无 Pixel 选 Web Form；一上来 Cost Cap；表单字段超过 5 个；没对接 CRM 就说能优化质量；金融医疗不提资质。

## 资产清单

定方案要查的（阶段 3"你有什么"这一步查）：

| 检查 | 工具 | 缺了怎么办 |
|---|---|---|
| 账户、币种、余额 | advertiser_info_get | 余额 0：可以建，充值后再开 |
| 线索条款 | term_check、term_get | 未接受：告诉用户要接受条款，term_confirm 要用户明确同意 |
| Instant Form | page_get（business_type LEAD_GEN，status PUBLISHED） | 没有：MCP 建不了表单。替用户写好表单文案（标题、3 到 5 个问题、隐私政策链接、感谢语），让用户在 Ads Manager 建好，再 page_get 确认 |
| 落地页和表单事件 | tool_url_validate、pixel_list_get | 无 FORM 事件：用 Instant Form |
| 行业资质 | bc_advertiser_qualification_get | 金融、医疗缺资质先补，不建 |
| 在跑 campaign | campaign_get，objective_type 过滤 LEAD_GENERATION | 有：转运营分支（operate.md） |

建之前才查的（阶段 7 建草稿之前查）：

| 检查 | 工具 | 缺了怎么办 |
|---|---|---|
| 文案违禁词 | blockedword_check | 命中先改 |
| CRM（运营用） | crm_list_get | 没有：crm_create 对接 |
| 素材和身份 | file_video_ad_search、identity_get | 无素材先建到 adgroup |

## 首投（这类广告在账户里还没建过）

1. 问清：行业、有没有落地页、收哪几个字段、日预算、目标 CPL、市场。字段精简到 3 到 5 个。
2. 阶段 3 查到的硬阻塞没解决不往下走；建之前再查"建之前才查"的几项。条款和表单是硬阻塞。
3. 方案一句话：Lead Generation，Instant Form 或 Web Form，最低成本自动出价（Lowest Cost），日预算按 routing.md 阶段 4 的区间给范围加一个推荐数，不低于 20 USD。
4. 确认后建，参数见 ads-products/lead-gen.md，全部 DISABLE。Instant Form 不存在时 campaign 和 adgroup 先建，ad 等表单建好再建。
5. 读回；预览；查审核。
6. 确认后开启。告诉用户：次日看线索数，线索用 lead_get 或 page_lead_task_create 导出。

## 运营（已经有在跑的线索广告，流程见 operate.md）

这张卡特有的首因顺序，查完再按 operate.md 的通用顺序：
1. 线索质量差而不是量少：lead_get 抽样看，先加筛选字段或转 Web Form，接 CRM 回传（crm_create）后才谈按质量优化
2. 表单问题：字段超过 5 个、表单没发布（page_get 状态）
3. 条款或资质：term_check、bc_advertiser_qualification_get
4. 素材疲劳；CPL 高于行业基准

加量：7 天 ≥ 50 条且 CPL 稳定再加预算 ≤ 30%；量够质量差走第 1 条；到位后开 Smart+ Lead（ads-products/smart-plus.md）。

不做：没对接 CRM 就说能优化质量；学习期换表单类型；一上来 Cost Cap。

## 下一步触发

- 7 天 ≥ 50 条线索且 CPL 稳定 → 转运营。
- 量够质量差 → 加字段、转 Web Form、接 CRM。
