# tt-ads-launch

TikTok Ads MCP 的投放 Skill：对话层按 9 个阶段走（问清情况 → 你的情况 → 你有什么 → 推荐 → 方案单 → 素材 → 建草稿 → 上线），判断层用 7 张客户卡和 7 份产品参数。覆盖 7 类客户：TikTok Shop 卖家、独立站电商、非电商网站、App 增长、内容型 App、线索收集、品牌触达。

## 安装

Claude Code：把整个文件夹放到 `~/.claude/skills/tt-ads-launch/`，新开会话即生效；对话里输入 `/tt-ads-launch` 可手动触发。

claude.ai：设置 → Skills → 上传本文件夹的 zip。

前提：会话里已连接 TikTok Ads MCP（connector 或本地 server 均可），并有可用的广告账户授权。

## 试用

> 我刚开了 TikTok Shop，想投广告卖货，怎么开始？
> 我有个 Shopify 店，Pixel 装了，帮我建个转化广告，一天 50 美元。
> 点击很多但没人买，怎么办？
> 我们是做留学咨询的，没有网站，能在 TikTok 上收表单吗？
> 我们的 App 刚上线，想拉新，一天 200 美元。

## 结构

- SKILL.md：总规则（每条回复只拿这条回复要用的东西）、9 个阶段总览、怎么说话、阶段 0 和 1
- routing.md：阶段 2 到 5（认客户、查账户、推荐、方案单）和识别表、交叉核对表、目标选项表
- build.md：阶段 6 到 8（素材、建草稿、上线）
- operate.md：运营分支（掉量、不消耗、加量、被拒的诊断和动作）
- guardrails.md：红线和执行硬规则
- persona-cards/：7 类客户各一份（判定表、资产清单、首投步骤、运营两件事、下一步触发）
- ads-products/：10 份广告产品参数（前置检查、参数表、读回、已知坑）
- test/：headless 实跑脚本和一次完整对话记录

