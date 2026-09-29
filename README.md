# OPCS Control Plane V0

`opcs` 是 OPC 项目的轻量控制仓：记录项目、假设、证据、成本、决策与交接。业务代码仍在各自独立仓库，每个项目只能有一个业务代码真源。V0 只有手动维护的文档、登记表和模板，不包含应用、数据库、自动编排、内容生成器或跨仓同步服务。

## 使用步骤

1. **新想法**：复制 [项目卡片](templates/project.md)，有实际内容时再保存到 `ideas/<项目ID>.md`，写明用户问题与目标。
2. **登记项目**：在 [项目登记表](registry/projects.yaml) 添加唯一 ID、业务仓库和下一步；没有证据的已有项目使用 `UNCONFIRMED`。
3. **研究**：比较现成方案，明确 MVP、可观察的验收阈值与预算；可以直接决定 STOP。
4. **构建**：在项目自己的仓库实现和自测，回填分支、提交与产物证据。
5. **验证**：基于 [验收模板](templates/validation.md) 留存真实结果，有报告时再创建 `evaluations/`。Mock 只证明模拟路径。
6. **决策**：记录 GO / ITERATE / STOP 及依据；证据不足时保持 PENDING。更新登记表的阶段、状态、证据与复核日期。
7. **内容化**：依据验收报告填写 [内容事实源](templates/content.json)，有实际内容时再创建 `content/`；未知结果不能包装为成功。

## 文件导航与隔离

- [操作约束](AGENTS.md)：开工、路径范围、证据与交付要求。
- [有限状态流程](harness/workflow.md)：阶段、产物、跨仓交接。
- [循环与预算策略](harness/loop-policy.md)：单任务软上限与熔断的唯一规则来源。
- [首个漫剧实验](experiments/EXP-0001-ai-drama-stadio.md)：待验证假设与取证计划。
- [AI 漫剧业务仓库](https://github.com/SqlBoy001/ai_drama_stadio.git)：唯一业务代码真源；本仓不迁移或复制其源码，不使用 submodule/subtree。

登记表是项目索引，不是跨仓实时同步机制。项目内实现、运行日志与产物留在项目仓库或授权存储，控制仓只登记可追溯引用；不得跨项目顺手修改。进入业务仓库后读取该仓库自己的规范。

## 登记字段约定

`schema_version: 1`；`projects` 为项目列表。

| 字段 | 含义 |
| --- | --- |
| id / name / repo | 唯一项目 ID、显示名称、唯一业务源码仓库 |
| stage | IDEA、RESEARCH、BUILD、VERIFY、ITERATE、CONTENT、DONE、STOPPED；UNCONFIRMED 专用于未经核实的已有项目 |
| status | unverified（未核实）、active（推进中）、blocked（阻塞）、closed（已结束） |
| owner | 负责人，未指定用 TBD |
| goal / hypothesis | 目标与可被证据否定的假设 |
| next_action | 下一次具体行动，不代表已授权付费或发布 |
| evidence | 证据列表，每项包含 kind、source、checked_at、note；区分事实、观察、推测 |
| cost | token、api_calls、cny、human_hours；只填已核实实际用量，不是预算 |
| decision | PENDING、GO、ITERATE、STOP；不从运行成功自动推导 GO |
| last_reviewed | 最近人工复核登记的日期 YYYY-MM-DD，不等于业务验收日期 |

`null` 表示未知或未测量，`TBD` 表示待明确；空数组表示尚无记录，均不等于零。明确核实为零时才填 0。日期使用带引号的 ISO 日期；有费用时说明币种、口径、时间范围和账单证据。待核实报告放在证据备注，不能直接写进已核实成本。

默认单执行者；必要时一次独立验证，由总控决定结束。单任务交接最多 6 次、开发返工最多 2 次、完整 QA 最多 1 次、同一错误自动重试最多 2 次；达到上限及其他停止条件按循环策略输出 `AUTO_LOOP_STOPPED`。这些是文本软限制，V0 没有平台 Token 预算强制执行能力。

## 本地检查

在仓库根目录执行 `python3 -m json.tool templates/content.json`、`git diff --check`、`git status --short`、`git diff --stat`。如已有 PyYAML，可用 `python3 -c "import yaml; print(yaml.safe_load(open('registry/projects.yaml')))"` 检查解析；无需为此安装依赖。修改后检查相对链接、登记字段与阶段枚举，并对照循环策略人工复核。纯文档控制仓不需要应用构建或付费模型调用。
