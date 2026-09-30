# OPC-2 Explorer → Demo Plan → Deterministic Replay → Record

ACTIVE_PROJECT=ai-drama-stadio；实验 EXP-0001；父任务 OPC-1。
目标：一版 45–90 秒真实复盘草稿。只写独立 content-draft 与控制仓本实验文档；不改业务或原素材。新增付费生成/API预算 0；Token、运行费用、人工时间未知。

## Explorer（2026-09-30，正式录制前）
已读 Validation-Report-v2（附件 01a0f062-cbcc-7c9d-9e65-4c0bb6d9a4ab），业务 AGENTS 与控制仓规范。直接媒体地址成功打开，video readyState=4，1280×720，duration=60.018667，error=null；暂停定位34秒，截图 explorer-34s.png，实际目视可见女主与押送官。源 SHA256 与 v2 一致：b7066a812e9801f7b3d4b6ab8874a483bb52ca106851f7e07e681a48b4c16029。

## Demo Plan（先固定再录制）
不操作生成按钮，不修制作页，不录账单账户。正式浏览器记录只展示源片34–41秒，静音、1倍速，自动在41秒暂停。录制前先执行相同回放并确认到达终点。浏览器录屏是回放路径证据；最终草稿直接从核实源文件裁切，避免录屏加载等待及界面遮挡。费用使用脱敏文字卡并标明 v2 E11/E12 摘录，不冒充账单原截图。

## 确定性步骤
1. agent-browser --session opc2-content open 正常媒体地址。
2. 等待 video readyState>=2；muted=true，playbackRate=1，pause，定位34秒并等待seeked。
3. 播放并监听timeupdate，到41秒暂停；保存实际终点、error。
4. 预演通过后 record start explorer-replay.webm；执行同一脚本；record stop。
5. 输出草稿按 content.json 的源时间码与时长用 FFmpeg 裁切，不变速；字幕/文字卡由同一事实源生成。

## 素材位置（交接内部定位，不作为附件交付替代）
源片：/Users/shenzihao/Documents/ChatGPT/AI_Drama/backend-node/data/storage/projects/0006_20260926_亡国公主·全角色重制版/exports/action-v06/jinyang-EP01-action-v06c-720p.mp4
服务：http://localhost:5679/static/projects/0006_20260926_亡国公主·全角色重制版/exports/action-v06/jinyang-EP01-action-v06c-720p.mp4
证据目录：/Users/shenzihao/Documents/ChatGPT/AI_Drama-verification-20260930
正常地址仅一层 /static；制作页重复路径问题依据v2 E08，不重新做完整QA。

## 交付边界
字幕静音版，不加入未经主观听审的原声；无付费TTS。录屏不包含账户或个人页面。仅执行内容产物技术和排版自检，不冒充独立QA，不重新验收业务效果。正式发布未授权。第2次角色交接进入本任务；返回总监时为第3次，不唤醒其他Agent。既有完整QA额度已使用，本任务不新增完整QA，开发返工未发生，不重置历史计数。

## 执行记录补充
预演终点41.108159秒、paused=true、muted=true、error=null。首次录屏回放终点41.126808秒，但record stop因进程PATH找不到ffmpeg而导出失败。agent-browser doctor --offline --quick 10 pass / 0 warn / 0 fail；采用已有业务仓tools/ffmpeg路径重启本任务独立浏览器会话，一次重试。未安装依赖、未修业务播放器。最终导出结果见 self-check.md。

最终录屏限制：一次环境修正后 record stop 返回成功，但 ffprobe 实测 explorer-replay.webm 时长仅0.400000秒，不是完整7秒回放。此文件不纳入可用交付，也没有用于草稿；不再重试或修工具。record-replay.json记录源播放器实际到41.123268秒、静音、暂停、无媒体错误，只证明回放执行，不证明录制正确。可重复播放路径成立，完整浏览器录屏未通过。按原任务授权，草稿采用已核成片直接裁切：源0–8、34–41、46–53秒，输出14–22、22–29、29–36秒；没有浏览器加载等待。交接中保留此限制，不能将草稿称为完整屏幕录制。
