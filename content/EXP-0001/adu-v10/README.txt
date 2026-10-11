OPC-2 v10 — adu-motion-video 优化试作

定位：个人 OPC AI 漫剧制作经历分享。原稿来自 v09 / content.json，未添加虚构成本、结果或成功案例。

观看：
OPC-2-v10-adu-motion-129s.mp4：1080×1920、60fps 母版。
OPC-2-v10-review-720p.mp4：720×1280、30fps 轻量审阅版；声音与母版同一混音。
本片约 129.42 秒；讲述的是一次制作 60 秒漫剧的经历，两者时长含义不同。

已做：
1. 安装 adu-motion-video 3.14.0-rc.1 及依赖；补齐 FFmpeg 9.0.2，doctor 通过。
2. 使用文档支持的 new / Scene / mk / show / S / setFrame / 字幕接口，并由该 skill 的 audio → mix → render 导出完整视频。
3. 无真人口播素材，因此采用自定义图文场景；不是把整片称作已验证的 01-D 宏模板。
4. 保留 9 章、24 镜头、73 条原字幕的讲述内容，按本地 Eddy 普通话音频重新排时，从原静音稿 185 秒调整为约 129 秒。
5. 统一黑体字形与竖屏边距，浅色章节改用深色字幕；背景按准备、问题、结果区分色调。
6. 真实样本动态圈注、服装前后对照、原片/剪辑版原速对照，定格有说明。
7. 增加旁白、31 个动作/转场音效事件，以及本片原创的低音量合成配乐。未使用付费生成 API。
8. 成本口径保留：前期先充 200 元火山节省计划，本次生成和修改约 75 元，DeepSeek、MiniMax 未计入；继续调优仍需投入。

编辑入口：
project/scenes.js：镜头布局、动态圈注、转场及音效事件。
project/timeline.json：实际音频时间轴；字幕时间来自逐条音频采样长度。
project/config.js / style.css / caption-theme.js：画幅、字体、颜色与字幕。
project/voice.wav / assets/original-underscore.wav：旁白和本片配乐。
project/audio.py / mix_recipe.json：声音合成及混音设置。
subtitles.srt / voiceover.txt：完整字幕与口播文本。
原生 HTML 工程按 renderAt(t) 确定性渲染，不是剪映或 Premiere 工程。

验证范围：
checks.json 保存最终编码文件的完整解码、帧数、响度、真峰值、文件 SHA 与字幕边界检查。
geometry-check.json 检查 73 条字幕的边界及标题/说明文字碰撞。
motion-review.jpg 保存关键运动区间的密集抽帧；layout-review.jpg 为首次布局检查，后续修正以实际 MP4 与单帧检查图为准。
media-provenance.json / media-color.json / color-review.json 保存真实素材、裁切与颜色假设。
原 final/edit 源视频没有完整色彩标签，按 SDR 导入并与同刻直接解码参考进行了对照；不声称已完成原生播放器的专业色彩认证。

未验证：
当前代理不能主观听音，未完成完整人工听审；Eddy 音色自然度、语句停顿、背景音乐舒适度及最终传播效果，需用户连续看听后确认。以上是内容制作人自检，不是独立业务 QA。

许可：
adu-motion-video 的 MIT 许可见 ADU-LICENSE.txt。原创配乐由 compose_music.py 为本片生成，不含第三方采样。历史图像与影片继续沿用本项目的真实素材来源与使用范围。
