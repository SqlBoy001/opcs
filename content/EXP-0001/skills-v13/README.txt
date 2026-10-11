OPC-3 v13 — 官方技能安装与短样片工作流

Completed
已从官方GitHub固定提交安装13个Skill目录：HyperFrames核心/创意等8个、ElevenLabs文字转语音/语音转文字2个、Remotion主入口/字幕/渲染3个。来源与文件校验见skills-lock.json。持久位置 /Users/shenzihao/.agents/skills；当前运行环境已链接，下一轮可自动发现。
Captions AI未识别到可核实的官方Skill。本轮明确用Remotion官方remotion-captions作功能替代，不声称安装了Captions AI。
Remotion实际完成1080×1920、30fps、约15.8秒样片；HyperFrames创意规范用于规划；MiniMax speech-2.8-hd完成四段旁白，速度1.12。重点词按供应商真实字符时间戳逐步变色。

Changed Files
完整工程：/Users/shenzihao/Documents/ChatGPT/OPC-3-content-v13-workflow
控制仓记录：opcs/content/EXP-0001/skills-v13
旧v10/v11/v12和业务原素材保留；没有修改业务源码。
content.json为本样片的编辑真源。各scene包含text、emotion、direction、keywords、visual、真实captions和时间轴。studio/src/content.json是生成副本。speech-plan.json是初始策划快照，不再用于生成。
Opening / Failure / Cost / Takeaway四个独立组件与组合样片均在Studio注册，可以单独预览。JSON控制文案、费用数字、素材、重点词与总结步骤；版式代码负责样式和动作。

使用
打开本机预览：http://localhost:3000/OPC-Pilot（仅服务器运行时可用）。
重新启动：cd studio && npm ci && npm run dev
配置包未包含17MB完整字体与node_modules：首次在其他目录运行 python3 restore-font.py，下载固定提交的开源字体并验证SHA256；字体OFL许可证已包含。本机完整工程无需下载。
不新增TTS的重排：python3 prepare.py
导出新版本：zsh render-pilot.sh /绝对路径/新的文件名.mp4
文字或声线变化时，先在content.json给相应scene更换未用过的id，再指定 python3 synthesize.py 新id。该操作会调用MiniMax收费接口；已有缓存与正文不符会拒绝复用，同一失败请求不自动重试。随后prepare.py按实际声音长度重算时间轴。
本模板当前固定四个场景和15–20秒样片目标；扩展整片需另行规划，不会默认生成全部内容。
分段direction是供策划者阅读的表演说明，未作为可任意控制的MiniMax提示词提交；实际API只用了文案、声线、speed和emotion。效果仍以试听为准。

ElevenLabs同稿入口
python3 compare_elevenlabs.py --check 仅离线检查环境，不收费。
本机配置ELEVENLABS_API_KEY及适合中文的ELEVENLABS_VOICE_ID后，python3 compare_elevenlabs.py 可生成一条同稿候选并保留字符对齐、调用回执。密钥不写入JSON或日志。此入口当前只通过凭证预检/语法检查，未进行真实ElevenLabs生成；没有对两家音质作出胜负结论。

Verification
npm run lint（ESLint＋TypeScript）通过。完整MP4解码通过，四场景无时间空洞，字幕逐字覆盖及范围检查通过，五个关键帧查看无明显遮挡/截字，音量约-16.07 LUFS、真峰值-1.49dBTP。checks.json为内容执行者定向自检，不是独立业务QA或人工听审。
默认下载的Chrome Headless Shell首次启动出现Target closed；使用本机Google Chrome导出成功，脚本已固定该路径。
MiniMax四次调用、129计费字符，按官方标价估算0.04515元，真实账户实扣和Agent运行费用未知。

Known Issues
ElevenLabs缺本机API Key与中文声线选择；未运行双引擎试听。
脚手架开发依赖的npm audit报告10项high，当前无完整自动修复路径；生产依赖npm audit --omit=dev为0项。未发布公网服务，保留两份审计原始报告。
75元沿用用户要求的粗略视频生成修改口径。原v2验证边界仍保留在制作记录中，不新增完整成本审计结论；业务验证PARTIAL不变。

Next Step
先试听本次约16秒样片，判断清晰度、语速、情绪与画面节奏；选定后再展开完整视频。ElevenLabs凭证配置好后可用同一文稿补做对比。
