# Kimi 本土化与歌词镜头校准

本文件是 `world-execute-me-kimi` 的创作依据。研究快照：2026-10-05。视频中的 Kimi、Moonshot AI、Kimi K3、Kimi Researcher、Kimi Code、Kimi Work、KDA、AttnRes 与 1M context 文案，都按 Moonshot AI / Kimi 官方页面整理。

## 品牌与文化

Moonshot AI 官方将公司成立时间写为 2023 年春季，愿景是“把能量最优地转化为智能”，并强调开放模型与技术理想主义。Kimi 品牌手册把“对未知保持好奇”、前沿感、人文主义和技术严谨放在同一套身份里。因此视频把“启动”理解成好奇心点亮，把“执行”理解成长期任务中不断回到用户目标，而不是一次性的问答。

Kimi 是 Moonshot AI 自研的 AI 助手。官方产品语境包括联网搜索、深度思考、多模态推理、超长文本，以及 Kimi Researcher 的意图澄清—规划—检索—推理—交付链路。Kimi K3 页面把长程编码、知识工作、推理、原生视觉和 1M-token context 作为核心能力；K3 的开放页面同时提供权重、技术报告、MoonEP、FlashKDA 和 AgentEnv。

## 发行版与时间线

- 2024-01-31：Kimi 开放平台进入公测，提供 moonshot-v1 与 128K 上下文 API。
- 2025-09-05：Kimi K2 发布，官方 Agent 演进页将其描述为面向端到端智能体工作的模型。
- 2026-01-27：K2.5；2026-04-20：K2.6；2026-07-16：K3。
- K3 是本片的当前主角：2.8T 参数、原生视觉、1M-token context、Kimi Delta Attention（KDA）与 Attention Residuals（AttnRes），并以开放的 3T-class 模型形态发布。

## 两个创作视角

### AI 专家视角

前 0–73 秒保留歌曲中“启动—参数—预训练—对齐”的节奏，但镜头标签改成 Kimi 技术链：`Moonshot AI` → `Kimi K3` → `1M context` → `native multimodal` → `KDA + AttnRes` → `Kimi Researcher`。数值只承担视觉节拍，不把未公开的训练细节写成事实；配置面板明确显示 provider、context、vision、attention、release、open_weights。

### Kimi 视角

73 秒以后保留原曲中对象变换、小猫、记忆、离线与重连的戏剧结构，把回答改成 Kimi 的产品体验：深度研究、代码与工作流、跨会话上下文、引用与下一步。猫咪是唯一吉祥物；小猫的“记住”对应上下文连续性，“一起探索”对应 Kimi 品牌的未知之境。

## 与音乐的校准

每个段落仍使用 `word_timeline.json` 的词头触发，不改动歌曲时长或音频。镜头语义按听感分成：

1. **启动段**：每个短促词头点亮一组系统日志、参数格或窗口边框。
2. **训练段**：连续音节驱动 token river、loss curve 和 KDA pipeline，画面密度随音乐上升。
3. **部署段**：对象词头继续触发茄子、番茄和小猫道具，但对话内容改为“拆解问题—给出证据—形成方案”，让歌词的具体物件与 Kimi 的能力叙事同时成立。
4. **关系段**：`记住 / 回来 / 一起探索` 对应 memory 文件、1M context 环和 Kimi Researcher 的连续任务；最后的离线与重连保留原曲的情绪落点。

## 官方来源

- [Moonshot AI 关于我们](https://www.moonshot.cn/about)
- [Kimi 新用户指南：Overview](https://www.kimi.com/en/help/new-user-guide/overview)
- [Kimi 品牌手册](https://www.kimi.com/en/resources/kimi-brand)
- [Kimi K3 发布说明](https://www.kimi.com/news/kimi-k3)
- [Kimi K3 开源发布](https://www.kimi.com/news/kimi-k3-open-source)
- [Kimi Agent 演进](https://www.kimi.com/en/help/agent/agent-overview)
- [Kimi Researcher](https://www.kimi.com/help/deep-research/deep-research-overview)
- [Kimi API 概览](https://www.kimi.com/help/kimi-api/api-overview)
- [Kimi 官方下载页](https://www.kimi.com/products/download)
