# OPC-2 · 90 秒主版

这是交付用的主版。它沿用 `content.json` 的 `full_v03` 14 镜、事实与画面，仅压缩停留时间，并使用 `short_v04` 的 90 秒口播稿。117 秒 v03 保留为过程细节审阅版。

先按 `../full-v03/README.md` 渲染带字幕版与无字版，再运行：

```bash
python3 export_support.py
python3 render_short.py --variant captioned
python3 render_short.py --variant clean
```

本版仍是静音草稿。字幕文件描述屏幕文字；口播尚未录制，配音后须重新校时和审看。工作台截图是今日只读回看。费用、质量与未听审边界沿用 v03 自检和 OPC-1 验证报告。
