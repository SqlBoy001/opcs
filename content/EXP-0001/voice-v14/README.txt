OPC-3 v14 — F 音色完整视频

Completed
用户确认 F 后，完整九章使用同一个 MiniMax 音色设计 ID：ttv-voice-2026101119460226-UTBhn2Xo。
模型 speech-2.8-hd，速度 1.0，情绪 auto，与用户确认的正式口播参数相同。
保留 v12 的完整脚本与真实素材，把 v13 暖白、墨黑、朱红版式扩展至 24 个镜头。
全片约 120.57 秒，1080×1920，30 fps；70 条字幕依据供应商逐字时间戳对齐。无背景音乐。
成本页保留九月账户 274.92 元、其中节省计划 200 元，以及本版生成修改约 75 元。
视频不展示成本审计备注；事实与范围边界仍在生产记录中保留，不改变业务 PARTIAL 验证结论。

Changed Files
项目目录：/Users/shenzihao/Documents/ChatGPT/OPC-3-content-v14-F
content.json 是完整正文、音色参数与镜头结构的编辑真源；speech-plan.json 仅为初始快照。
timeline.json、studio/src/full-content.json、subtitles.srt 是 prepare_full.py 依据真实音频生成的时间轴。
FullFilm.tsx 为数据驱动的整片模板，引用已验证素材；未新增业务画面、未修改业务源码。
旧版本保留，选声记录在 OPC-3-voice-natural-20261011/selected-voice.json。

使用
预览：http://localhost:3001/OPC-Full-F（本机服务运行时有效）。
启动：cd studio && npm run dev -- --port=3001
重排已有音频：python3 prepare_full.py
导出：zsh render-full.sh /绝对路径/新文件名.mp4
重新配音会收费：先在 content.json 修改正文并为变化章节使用新 ID，再指定 python3 synthesize.py <ID>。
生成器复用已有音频前核对正文、音色和语速；失败请求不会自动重试。
本机 node_modules 复用 v13 的锁定依赖。迁移机器时运行 npm ci；原视频素材按 media-source.json 的本地证据路径恢复，不会自动重做业务生成。

Verification
npm run lint（ESLint 与 TypeScript）通过。
时间轴：24 镜头连续、逐字覆盖 651 字符、70 条字幕范围检查通过。
初版逐镜抽帧已查看；提示词页改为人物细节图配文字摘录，避免把图片误作提示词截图。
完整视频解码、输出音量与交付文件大小见 output-checks.json（导出后生成）。
人工已批准 F 正式短段音色；整片听感仍待用户审阅。本轮为内容执行者定向自检，不是独立业务 QA。

Known Issues
HyperFrames usage 返回 unknown / usage_request_failed；制作与导出沿用现有 Remotion 4.0.534。
九次 MiniMax 合成，1221 计费字符，按 3.5 元/万字符估算 0.42735 元；真实账户现金扣款未核对。
沿用已经激活的 F 音色，无新增音色设计或复刻。历史首次使用费与前期试听成本不算作本轮新合成费用。
Agent Token 与运行费用没有可靠计量；不宣称完整制作成本已审计。

Next Step
用户审阅完整视频的口播节奏、字幕与画面同步；未对外发布。
