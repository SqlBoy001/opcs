# v08 内容运营自检

Completed：完成用户2026-10-08授权的字幕与收尾定向修改，180秒静音审阅稿。没有新生成、业务修改或对外发布。

Changed Files：content.json新增recap_v08；本目录生成/渲染/检查脚本、口播、SRT、费用说明；实验登记补充。旧v07与业务源媒体保留。

Verification：
- `python3 prepare.py`、`python3 render.py --preview`、`python3 render.py`已运行，20个镜头、180秒、720×1280、24fps、4320帧，无音轨。
- `python3 check.py`通过：全片解码无错误，69条字幕连续覆盖0–180秒且不跨所属镜头；口播、SRT与统一事实源一致；15个原始素材SHA一致。
- `python3 review_frames.py`从最终编码视频抽取20个代表帧，两张拼图均已由执行者查看，另看字幕样例和5个新结尾全尺寸预览。重点检查黑框移除、字体、长句边界、费用数字与总结内容；不是全4320帧人工逐帧验收。
- 渲染时每条字幕实际测量宽度，不超过648px，苹方SC Semibold（系统字体collection index 11），最小字号31px。旧视频前130秒只替换1104px以下字幕区并重编码；源v07 SHA与已交付版本一致。
- `python3 -m py_compile`与`git diff --check`通过。预览只读取首帧后主动关闭解码器，出现预期Broken pipe提示；正式导出与完整解码无此错误。

Artifact：4943210 bytes，SHA256 `177ed58df50125ee4ab2c0a5aea88ffd787364d5bb06424d81f6b77094a3cf55`。

Known Issues：静音，尚未配音或添加音效。费用为用户指定的亲历粗估：200元为前期套餐充值，约75元为本次火山视频现金，DeepSeek/MiniMax等未计；没有刷新实时云账单，也没有逐请求全成本归因。视频中的未来优化没有报价保证。

Next Step：用户审阅本版字幕及后半段节奏。业务验证仍PARTIAL，本次是内容运营定向自检，不是新增独立业务QA；历史交接/返工/完整QA计数保留。新增付费生成/API调用0，Agent运行费用与人工时间未计量。
