# 官方 ChatCut 与组合技能：能力核对

核对日期：2026-10-11。ACTIVE_PROJECT：opcs-control-plane / EXP-0001 content comparison。范围：只读官方资料及本文件；无付费调用、无安装、无新视频实测。验收：区分官方能力声明、本地实测与建议；不据技能数量推断质量、速度或成本。本地历史实测证据见后文。

## 对象与结论

比较对象是 chatcut.io / ChatCut-Inc 的官方 ChatCut Desktop，不是其他同名开源项目。现有“四工具”也不等于四个已调用服务：本次项目实际链路为 Remotion + MiniMax F 配音 + MiniMax 时间戳 + remotion-captions 相关方法；ElevenLabs 尚未调用，Captions AI 官方技能尚未确认。此项目状态来自主执行者，具体产物证据应与下文官方文档分开核对。

判断：组合方案主要增加对素材、数据、代码和渲染流程的直接控制；ChatCut 提供现成的可编辑项目工作台。两条路线功能大量重叠，不能概括成“ChatCut 只能剪辑、组合方案才能动画/字幕/批量”。尚无同素材、同规格、同验收口径的对照实验，不能判定哪条路线更快、更便宜或质量更高。

## 官方资料支持的能力

| 对象 | 已核对的能力 | 对本任务的意义与边界 |
| --- | --- | --- |
| ChatCut Desktop | 官方应用连接 Agent；自动注册本地 `chatcut_desktop` MCP，并同步匹配的编辑技能。 | 是本地桌面集成；当前指导明确不再用历史 hosted 插件替代。桌面实际工具以当前会话为准。[Desktop 指南](https://chatcut.io/desktop-plugin) |
| ChatCut 产品 / hosted 插件 | 官网展示时间线手工修改、字幕、动效、配音及技能复用；官方仓库说明媒体导入、时间线修改、转录、字幕、生成与导出。 | 支持集成工作流的判断；官网宣传不等于本机已验收，hosted 文档也不能直接证明 Desktop 功能完全一致。[官网](https://chatcut.io/)、[官方仓库](https://github.com/ChatCut-Inc/agent-plugin) |
| ChatCut hosted 动效 | 可直接写 JSX，暴露可编辑文字/颜色/媒体属性；使用 `useCurrentFrame`、`spring` 和 Remotion 工具。 | “ChatCut vs Remotion”并非完全独立的技术二选一。当前文档另列导出 CSS 限制，不能只看预览推定导出正确。[官方 MG 合同](https://github.com/ChatCut-Inc/agent-plugin/blob/main/codex/skills/create-motion-graphics/SKILL.md) |
| ChatCut hosted 导出 | 视频、音频、字幕、XML；提交任务并追踪完成状态；需要报告不支持或丢弃的元素。 | 此技能明确只适用 `chatcut` hosted MCP，Desktop 使用自身指令和工具，不能混用或推定无损互通。[导出技能](https://github.com/ChatCut-Inc/agent-plugin/blob/main/codex/skills/export/SKILL.md) |
| HyperFrames | HTML 合成、逐帧 seek/capture、CLI 渲染；Studio 有预览、时间线、属性面板，编辑写回项目文件。 | 可作为代码化视频与动画的另一种实现。不能说它“没有时间线/可视化编辑”，也不能据确定性渲染宣传保证任意资源组合永不出错。[Engine](https://hyperframes.heygen.com/packages/engine)、[Studio](https://hyperframes.heygen.com/packages/studio) |
| Remotion | React 组件接受输入 props，数据可决定内容、宽高、时长、帧率；Studio 可编辑参数；字幕有导入、转录、展示和烧录/SRT 导出路径。 | 适合把统一 content.json 映射到复用模板；模板、字幕时序与音画验收仍须实现和维护。[参数化视频](https://www.remotion.dev/docs/parameterized-rendering)、[字幕文档](https://www.remotion.dev/docs/captions/) |
| ElevenLabs | TTS with timestamps 返回音频及字符级起止时间。 | 是可选配音/时间对齐组件，不是整套剪辑系统；能力存在不代表本项目使用过或比 MiniMax 中文配音更好。[官方接口](https://elevenlabs.io/docs/api-reference/text-to-speech/convert-with-timestamps/) |
| Captions AI | 官方产品包含整片 AI Edit、字幕、翻译、B-roll、风格化编辑等。 | 是独立产品；不能与 Remotion 的 captions 包/技能混为一谈，也不能将其产品能力记为当前环境已安装可调用。[官网](https://captions.ai/) |

## 工作流取舍（基于上述能力的推断，非跑分）

- 人持续修改镜头、单段音频、字幕布局并希望立即看到项目：ChatCut 的现成工作台通常更贴合交付形式，但仍需验证本机预览与导出。
- 同一事实源生成不同画幅、不同文案、多个版本，并要求代码审阅和重跑：Remotion 或 HyperFrames 更便于把规则留在项目内；代价是依赖、素材路径、字体、同步和渲染检查由我们维护。
- HyperFrames 与 Remotion 都覆盖画面编排和渲染，没必要每条片强行串联二者。保留当前已跑通的 Remotion 路线，只有明确的 HTML/动画需求才评估 HyperFrames，可减少一次无必要迁移。
- 配音是独立选择：先按现有 MiniMax F 做交付；若需要更合适的声音，再用同一段中文做有预算的盲听比较。仅安装 ElevenLabs 技能不能证明声音提升。
- ChatCut 可以成为人工精修与审片入口，程序化方案生成素材或成片；但扁平 MP4 导入不会自然还原可编辑字幕/动画层。需要可编辑交接时必须设计分层素材和时间线映射。

## 成本与验证边界

未核实两条路线在相同任务上的实际账单、Agent 用量、人工时间或端到端耗时，故不给成本数字或“更省钱”结论。订阅价、开源许可证、一次 API 单价都不能单独代表整片制作成本。

Completed：已核对以上官方页面。Changed Files：本文件。Verification：官方网页只读核对；仓库 README/AGENTS、git status、git diff、git diff --cached 已读。Known Issues：未运行 Desktop/hosted API、未进行版本兼容性测试或 A/B 渲染；当前文档不代表历史版本。Next Step：补充已存在的本地验证证据；如需选型结论，用相同已批准素材做一次限定预算的对照，不从旧单例故障泛化现版本可靠性。


## 本项目实际跑过的结果

### 旧 ChatCut 链路

- 2026-09-21 的 80 秒工程导入了 16 段原始视频和 16 段独立旁白。第 13 段旁白从 60.0 秒移到 60.6 秒，其他 31 片段保持不变，输出波形验证了真实起点。可编辑多轨与局部改动已经实测，不是只看产品宣传。[桌面验收](</Users/shenzihao/Documents/ChatGPT/AI_Drama/docs/chatcut-desktop-acceptance-20260921.md>)
- 31 条文字作为可编辑 Motion Graphic 片段迁移；该次是整句时间段，不能当作原生字幕卡或逐字字幕的验收。[字幕验收](</Users/shenzihao/Documents/ChatGPT/AI_Drama/docs/chatcut-subtitle-acceptance-20260921.md>)
- 工作台已有素材指纹、独立时间线、导出回传、文件 SHA 和人工版本审核；后续又接入本地 ASR/VAD 队列。新 v14 仍是独立内容工程，尚未接入同一回传审核链路。[回传验收](</Users/shenzihao/Documents/ChatGPT/AI_Drama/docs/chatcut-pipeline-acceptance-20260921.md>)、[后续开发记录](</Users/shenzihao/Documents/ChatGPT/AI_Drama/docs/progress.md:358>)
- 历史 80 秒 v5/v6 曾出现孤立单帧黑画面，最终用 FFmpeg 后处理修复；更晚的原创 15 秒案例又通过了黑帧扫描。因此只能记录具体旧版本问题，不能泛化为 ChatCut 当前一定导出不稳定。[历史全片检查](</Users/shenzihao/Documents/ChatGPT/AI_Drama/docs/chatcut-full-review-20260921.md>)、[15 秒案例验证](</Users/shenzihao/Documents/ChatGPT/AI_Drama/docs/productions/do-not-open-v01/EP01/qc_report.v03.md>)
- 旧 80 秒片按每镜 5 秒安排，16 个旁白后静音区间约 1.4–2.5 秒；这是当时的排片/素材结果，不是 ChatCut 产品无法调整节奏。[实际扫描结果](</Users/shenzihao/Documents/ChatGPT/AI_Drama/backend-node/data/acceptance/chatcut-20260921/v7-validation.json>)

### 本次组合方案

- v13 中 HyperFrames 主要用于制作规范；成片实际由 Remotion 渲染。ElevenLabs 仅做凭证预检，尚未调用。未识别到 Captions AI 官方 Skill，使用 Remotion 字幕方案作为明确替代。[v13 执行记录](</Users/shenzihao/Documents/ChatGPT/OPC-3-content-v13-workflow/README.txt>)
- v14 九章全部使用用户确认的 MiniMax F 音色，24 个镜头、70 条字幕，由供应商逐字时间戳重排。120.576 秒的 1080p 原版与 720p 对话版均通过完整解码；这不是全片主观听审或逐帧语义验证。[输出检查](</Users/shenzihao/Documents/ChatGPT/OPC-3-content-v14-F/output-checks.json>)、[时间轴检查](</Users/shenzihao/Documents/ChatGPT/OPC-3-content-v14-F/timeline-checks.json>)
- 本轮 9 次 TTS 共 1221 计费字符，按所记录单价估算 0.42735 元，只是本轮语音合成估算，不含此前设计/激活、运行与人工成本，也不是两套方案成本对比。[费用记录](</Users/shenzihao/Documents/ChatGPT/OPC-3-content-v14-F/cost-ledger.json>)
- MiniMax F 可以作为独立音频导入 ChatCut；不需要更换剪辑工具才能使用这个音色。此为基于既有 WAV 导入实测的可行性判断，当前没有创建新的 ChatCut F 工程。

## 针对当前项目的建议

1. OPC 实验复盘、费用卡、前后对比和系列栏目：保留当前 Remotion + MiniMax F + 逐字字幕，继续积累可复用版式。
2. AI 漫剧正片、对白与镜头节奏精修：保留 ChatCut，继续使用已经接好的素材和审核流程。
3. HyperFrames 与 Remotion 按任务择一承担主要画面制作；ElevenLabs 保留为备用试听渠道；暂不为工具数量再引入 Captions AI。
4. 不以一次成片或 Skill 数量认定审美、耗时、稳定性、成本的全面胜出。后续需要整体换工具时，再做同一素材、同一修改要求的对照。

补充验收：主执行者已核对本地实际 JSON 扫描、局部修改差异和新工程输出记录。本轮无付费调用、无视频生成、无工程迁移、无业务源码修改。业务验证状态不变。
