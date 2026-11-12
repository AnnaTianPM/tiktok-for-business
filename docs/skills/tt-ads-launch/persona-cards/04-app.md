# 卡 4 · App 增长

拉 App 安装和应用内事件的广告主。首投绑 App 接 MMP，先 MAI（优化安装）起量，事件够了切 AEO（优化应用内事件），有金额购买再切 tROAS / HV。受限行业大客和平台型电商 App 只做运营，不写首投。

## 判定表（本次目标 + 账户状态 → 产品）

| 本次目标 | 账户状态 | 产品 | 说明 | 对用户怎么说 |
|---|---|---|---|---|
| 拉安装和应用内事件（只说"投广告"也按这行问） | App 已绑、MMP 回传正常，关键事件 7 天 ≥ 50 次 | **App Promotion · AEO（优化应用内事件）** | 默认 | App 推广，按 App 里的关键动作优化（注册、付费）：你的事件回传够多，可以直接按动作找人 |
| 拉安装和应用内事件 | 新 App，或事件不足 50 次 / 7 天 | App Promotion · MAI（优化安装），达标后切 AEO | | App 推广，先按安装优化：事件还不够 50 次，先攒安装，够了再改按动作优化 |
| 拉安装和应用内事件 | 有安装回传，没有事件回传 | MAI（优化安装） | 不选 AEO | App 推广，按安装优化：你只有安装回传，先这样跑 |
| 拉安装和应用内事件 | 连安装回传都没有 | 先接归因平台（MMP），什么都不建 | | 你的归因平台还没把安装回传给 TikTok，这一步必须先接上，不然投了也看不到结果 |
| 拉购买，要控回报 | 带金额购买 7 天 ≥ 30 次，tool_vbo_status_check 通过 | tROAS（目标 ROAS）或 HV（最高价值） | 门槛未满不切 | 按回报优化：要先有 7 天 30 次带金额的购买 |
| 召回老用户 | dmp_custom_audience_list_get 有安装人群 | App Retargeting | 拉新跑稳后可以同时跑 | 召回广告：把装过没用的人拉回来，拉新跑稳后可以同时开 |
| 只引流到商店页 | 任意 | App Traffic | | 商店页引流广告：只把人带到应用商店页，不优化安装，一般不如直接按安装优化 |
| 有网站版 | pixel_list_get 有网站事件 | 转卡 3 | 两张卡都适用，先问这次以哪边为主 | 你网站那边的用户，走网站转化广告，这次先定 App |
| 新品上线要曝光 | 任意 | 品牌竞价，见卡 7；预订只报表 | | 新品要曝光的话走品牌广告 |

iOS 14.5 以上要走专用 campaign，每天约 90 次安装才有 SKAN 数据；iOS 和 Android 各一个 adgroup，不混。

不默认推荐：无事件回传选 AEO；一上来 tROAS / HV；批量复制没有上限；给平台型客户写首投。

## 资产清单

定方案要查的（阶段 3"你有什么"这一步查）：

| 检查 | 工具 | 缺了怎么办 |
|---|---|---|
| 账户、币种、余额 | advertiser_info_get | 余额 0：可以建，充值后再开 |
| App 对象和 MMP | app_list_get、app_info_get | 没 App：app_create 并绑 MMP，给用户步骤 |
| 可用优化事件 | app_optimization_event_get（objective APP_PROMOTION、app_promotion_type、optimization_goal） | 没事件：只做 MAI |
| 再营销事件和人群（召回用） | app_optimization_event_retargeting_get、dmp_custom_audience_list_get | 无人群：用 App 活动建 |
| 行业资质、配额（大客用） | bc_advertiser_qualification_get、campaign_quota_info_get | 缺资质不建；配额满先清理 |
| 在跑 campaign | campaign_get，objective_type 过滤 APP_PROMOTION | 有：转运营分支（operate.md） |
| 并行命中：有没有网站事件 | pixel_list_get | 有：并行提示卡 3 |

建之前才查的（阶段 7 建草稿之前查）：

| 检查 | 工具 | 缺了怎么办 |
|---|---|---|
| VBO 资格（运营用） | tool_vbo_status_check | 不符合：继续 AEO |
| 素材和身份 | file_video_ad_search、identity_get | 无素材先建到 adgroup |

## 首投（这类广告在账户里还没建过）

1. 问清：平台（iOS、Android、都投）、目标（安装还是事件）、日预算、目标 CPI、归因平台（MMP，比如 AppsFlyer、Adjust）用的哪家、市场。
2. 阶段 3 查到的硬阻塞没解决不往下走；建之前再查"建之前才查"的几项。App 对象和安装回传是硬阻塞：没有安装回传不建。
3. 方案一句话：App Promotion，先优化安装（MAI），最低成本自动出价（Lowest Cost），日预算按 routing.md 阶段 4 的区间给范围加一个推荐数，iOS 和 Android 各一个广告组，iOS 14.5 以上单独一个 campaign。
4. 确认后建，参数见 ads-products/app-promotion.md，全部 DISABLE。
5. 读回；预览；查审核。
6. 确认后开启。告诉用户：分平台看，7 天安装到 50 次且事件有回传就切 AEO。

## 运营（已经有在跑的 App 推广，流程见 operate.md）

这张卡特有的首因顺序，查完再按 operate.md 的通用顺序：
1. 归因回传断：app_optimization_event_get 看事件是否仍可用，报表里有安装没事件
2. iOS 专用 campaign 数据少：每天不到约 90 次安装，SKAN 数据看不出来，先看 Android
3. 目标过高：AEO 事件太深或 tROAS 目标高于历史，消耗缩
4. 素材疲劳；受限行业被拒率上升

加量：MAI 稳定切 AEO、AEO 稳定切 tROAS 都新建广告组；加预算 ≤ 30%；有安装人群开 Retargeting。大客批量：campaign_copy_task_create 单次 ≤ 20 个对象，预算超源对象 3 倍要确认，完成后 campaign_copy_task_check。

不做：学习期换目标；iOS 和 Android 混一组；被拒率上升还继续复制；批量无上限。

## 下一步触发

- MAI 7 天 ≥ 50 次安装且事件回传（iOS 每日 ≥ 90 次）→ 新建 adgroup 切 AEO。
- AEO 出学习期后带金额购买 7 天 ≥ 30 次 → 新建 adgroup 切 tROAS / HV。
- 拉新成本涨且有安装人群 → 新建 Retargeting adgroup。
