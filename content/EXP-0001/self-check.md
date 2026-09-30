# OPC-2 内容运营交付自检

检查人：本次内容运营执行者。不是独立QA，不重做OPC-1完整验收。

## Completed
已完成一版78秒、1280×720、24fps、H.264/yuv420p、无音轨的中文字幕MP4草稿，未发布。完成统一content.json、脚本/分镜/证据引用、SRT、Explorer记录与确定性回放路径。实际源文件SHA与v2一致。最终草稿直接复用源成片0–8、34–41、46–53秒，原速呈现。

## Changed Files
独立产物目录：本次运行workdir/content-draft/。控制仓仅新增content/EXP-0001/{content.json,script-storyboard.md,subtitles.srt,demo-plan.md,self-check.md}，追加experiments/EXP-0001-ai-drama-stadio.md的本次证据。未改业务源码、原素材或账户配置。

## Verification
- `python3 content-draft/build.py`：PASS，输出78秒，1,416,630字节（约1.42MB）。
- `python3 content-draft/check.py`：PASS；ffprobe确认1872帧、78.000秒、单视频流；ffmpeg全文件解码exit0，stderr为空。
- 源SHA：b7066a812e9801f7b3d4b6ab8874a483bb52ca106851f7e07e681a48b4c16029。
- 草稿SHA：12947ba2b38160264158abedff7158bb4752626142a172321dbe16feea4833a9。
- 目视draft-contact-sheet.jpg的全部10章中点截图：真实片段有画面，标题/字幕无明显裁切，费用卡限定语可见。文字来自content.json；SRT连续覆盖0–78秒，10段；无旁白，旁白同步不适用。未对1872帧逐帧目视。
- 事实对照：60秒检查版/720p/24fps→v2 E03；动作切镜→E04/E06/Quality；听审未完成→E10/Quality；播放缺陷与直接播放→E08；74.92元→E12/Cost；274.92元含200元套餐→E11/Cost；完整成本未知→Cost；下一步听审及观众反馈→Next Experiment，明确尚未执行。
- 隐私与画面：草稿只有经核实剧情画面和自制文字卡，无账单原截图、账户UI、API Key、个人联系方式或错误界面。没有录屏等待。未加入未经听审原声；本版是静音字幕草稿，不是原片音频质量证明。
- 浏览器播放交付MP4：PASS，readyState=4，duration=78，播放从22秒前进至25.180908秒，error=null，证据draft-playback.json。
- 文档检查：`python3 -m json.tool opcs/content/EXP-0001/content.json`、`git -C opcs diff --check`均通过。
- 工具诊断：`agent-browser doctor --offline --quick`：10 pass/0 warn/0 fail。

## Known Issues
浏览器录屏首次导出因PATH缺ffmpeg失败；使用已有本地ffmpeg修正后导出文件仅0.4秒，完整录屏仍未通过，已弃用、不再重试。源播放器预演和回放日志正常到41秒，但不能以此宣称录屏成功。最终MP4不依赖该录屏；可重复路径、源时间码和异常均在demo-plan.md记录。

原业务仍PARTIAL：动作依赖剪辑，原声音色/情绪/口型未听审，完整制作成本未知，产品页播放问题未修，商业价值未验证。78秒是复盘草稿长度，60秒是被复盘的检查版长度，二者不能混写。账单为v2读取时2026年9月出账中快照，不是最终整集成本。

## Next Step
提交总监/用户审阅，不唤醒验证员，不自动派发下一轮。角色交接进入时2，返回总监时3；已有QA计数沿用且本次新增完整QA=0；新增研发返工=0。新增付费生成/API调用=0；Agent Token/运行费用/人工时间未知，未声称零成本或硬Token限额。正式发布、听审与受众验证均未执行。
