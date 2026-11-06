# 卡 1 · TikTok Shop 卖家

有 TikTok Shop 的卖家，用 GMV Max 卖货。新卖家从零建一条，老卖家加量或诊断。手动 Shop Ads 占不到 1%，不默认推。

## 判定表（本次目标 + 账户状态 → 产品）

| 本次目标 | 账户状态 | 产品 | 说明 | 对用户怎么说 |
|---|---|---|---|---|
| 卖货（只说"投广告"也按这行问） | 店铺已授权且 is_gmv_max_available，商品可投 | **GMV Max Product** | 默认 | 店铺的自动卖货广告（GMV Max）：系统自己选商品和视频，按店铺订单优化，新店也能起量 |
| 卖货 | 没有店铺，或店铺 is_gmv_max_available 为 false，或独家授权给了别的账户 | 先给授权或换账户的步骤；急着投走 Web Traffic 引流到店（落地页用店铺或商品的 TikTok Shop 链接，问用户要） | 不能建 GMV Max，不要试 | 你的店铺现在还不能用自动卖货广告（GMV Max），要先在店铺后台把广告授权给这个账户；急着投可以先投引流广告把人带到店里 |
| 卖货，点名要自己控商品和出价 | 店铺已授权 | 手动 Shop Ads（Video / Product Shopping） | 用户点名才做，说明占比极低 | 手动选商品、自己出价的店铺广告：你能控得更细，但绝大多数卖家用自动的效果更好 |
| 直播带货 | gmv_max_identity_get 有 live_gmv_max_available 的身份 | Live GMV Max | 可与 Product 并行 | 直播自动带货广告（Live GMV Max）：开播时把人引进直播间，可以和商品广告一起跑 |
| 直播带货 | 无直播身份 | GMV Max Product，提示先绑直播身份 | | 直播广告要先把直播的 TikTok 账号绑到广告账户，绑好再开 |
| 卖货，但成交在自己网站 | pixel_list_get 有网站事件 | 转卡 2 | 两张卡都适用，先问在哪成交 | 你在自己网站成交的那部分，走网站转化广告，下次可以单独建 |
| 曝光 | 任意 | 品牌竞价 Reach / Video View，见卡 7 | | 只要曝光的话走品牌广告，按多少人看到或看完来算 |

不默认推荐：手动 Shop Ads 当默认；店铺未授权就建 GMV Max；用 Promote（TikTok 站内一键推广）代替 GMV Max。

## 资产清单

定方案要查的（阶段 3"你有什么"这一步查）：

| 检查 | 工具 | 缺了怎么办 |
|---|---|---|
| 账户、币种、余额 | advertiser_info_get | 余额 0：可以建，告诉用户充值后再开 |
| 店铺可用 GMV Max、独家授权 | gmv_max_store_list_get | 无店铺或不可用：给授权步骤，不建。独家授权为空：用户确认后 gmv_max_exclusive_authorization_create 授权给本账户。授权给了别的账户：不动，告诉用户去改授权或换账户 |
| 全店推广是否允许 | gmv_max_store_shop_ad_usage_check_check | 不允许：改为指定商品 |
| 可投商品 | store_product_get（ad_creation_eligible=GMV_MAX） | 无 AVAILABLE 且 UNOCCUPIED 的商品：提示上架或检查审核 |
| 推荐 ROAS 和预算 | gmv_max_bid_recommend_get | 取不到：让用户给盈亏线，ROAS 取其 1.2 倍起 |
| 在跑的 GMV Max | gmv_max_campaign_get | 有：转运营分支（operate.md）；只有别的目标的 campaign 不算 |
| 直播身份（判定表"直播带货"两行要用） | gmv_max_identity_get（live_gmv_max_available）、identity_live_get | 没有：直播带货先绑直播的 TikTok 账号；只投商品不需要 |
| 并行命中：有没有网站购物事件 | pixel_list_get | 有：routing.md 交叉核对，可能转卡 2 或并行提示 |

建之前才查的（阶段 7 建草稿之前查）：

| 检查 | 工具 | 缺了怎么办 |
|---|---|---|
| 发布身份 | gmv_max_identity_get | 没有：用商品图自动生成，不阻塞；直播必须有 |

## 首投（这类广告在账户里还没建过）

1. 目标和范围：全店还是指定商品、日预算、目标 ROAS 或盈亏线。一次问完，缺啥问啥。
2. 阶段 3 查到的硬阻塞没解决不往下走；建之前再查"建之前才查"的几项。店铺授权和可投商品是硬阻塞。
3. 方案一句话：Product GMV Max，全店或 N 个商品，日预算 X，目标 ROAS Y（推荐值），并写明"建好就会开始投放和花钱，余额为 0 时充值后才会花"。预算低于推荐最低值时说明影响，由用户定。
4. 用户看到上一条后说建才建（"直接建"不算，因为建了就花钱）。参数见 ads-products/gmv-max.md。命名：商品或"全店" + 日期。
5. 读回 campaign_gmv_max_info_get 核对范围、预算、ROAS、状态；不一致就改。
6. 告诉用户：GMV Max 创建即进入投放流程（见 gmv-max.md 的暂停处理），次日看消耗和 ROAS，7 天内不改 ROAS。

## 运营（已经有在跑的 GMV Max，流程见 operate.md）

这张卡特有的首因顺序，查完再按 operate.md 的通用顺序：
1. 商品下架或被其他 GMV Max 占用（store_product_get 的 status、gmv_max_ads_status）
2. ROAS 目标高于推荐值（gmv_max_bid_recommend_get 对比 roas_bid）
3. 直播广告：直播没开播或身份失效（identity_live_get）
4. 素材疲劳：商品视频跑超过 2 周（gmv_max_video_get、gmv_max_report_get 按商品看）

报表用 gmv_max_report_get，按 campaign 和商品各拉一次。加预算用 campaign_gmv_max_update，单次 ≤ 30%；加商品、加视频用 gmv_max_creative_update；有直播身份可新建 Live GMV Max 并行。

不做：ROAS 一掉就下调目标（只在确认过高时下调）；只投 1 到 2 个商品；同时改预算和 ROAS；建手动 Shop Ads 代替。

## 下一步触发

- 连续 3 天有消耗且 ROAS 在目标区间 → 转运营。
- 近 7 天 ROAS 比 30 天均值低 20% 以上且消耗不降 → 先换素材和商品。
- 3 天不消耗 → 查余额、审核、ROAS 是否过高、商品是否下架，每次只改一项。
