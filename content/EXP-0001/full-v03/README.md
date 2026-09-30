# OPC-2 全流程过程版 v03

依据上级 `content.json` 的 `full_v03` 场景表导出 117 秒竖屏静音草稿。`assets/` 是 2026-09-30 对项目6/剧集10工作台的只读回看截图；历史生产素材仍在业务仓数据目录，渲染前会逐项核 SHA-256。

```bash
python3 export_support.py
python3 render_full.py --variant captioned
python3 render_full.py --variant clean
```

默认业务仓路径是 `~/Documents/ChatGPT/AI_Drama`；如不在此处，设置 `AI_DRAMA_ROOT`。渲染需要业务仓自带 FFmpeg 和 macOS 华文黑体。产物写入忽略版本控制的 `output/`。

本版无配音、无数字人，且未做发布 QA。网页录屏导出无帧，故使用预先规划的固定只读回放路径截图；工作台画面明确标为“今日只读回看”。正式发布前需完成口播、逐句字幕校时、原声听审与最终审看。
