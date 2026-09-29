# 验收报告：TBD

- 项目 ID / 实验 ID / 任务 ID：TBD
- 验证者 / 日期：TBD
- 验证身份：TBD（独立验收或执行者自检，必须如实标注）
- 验证范围：TBD（首次全量 QA 或列明问题的定向复验）

## Hypothesis｜假设

待验证假设及反证条件：TBD。执行前约定验收阈值与样本量，不根据结果临时改标准。

## Test Environment｜环境

仓库、分支、提交、系统、依赖版本、模型与参数、真实/Mock 模式、样本来源、授权：TBD。不记录密钥或个人信息。

## Test Steps｜步骤

1. 前置条件和输入：TBD。
2. 具体操作与可复现命令：TBD。
3. 预期阈值、实际输出和重复次数：TBD。

## Evidence｜证据

- 事实：TBD（产物路径、日志、账单及采集日期）
- 观察：TBD（样本边界与人工评估记录）
- 推测：TBD（尚未证明的解释）

Mock 只证明模拟路径，无法证明真实模型的效果；README 描述和程序运行成功也不代表效果合格。

## Results｜结果

| 维度 | 状态（PASS / PARTIAL / FAIL / NOT TESTED） | 阈值、实际结果与证据 |
| --- | --- | --- |
| 功能 | NOT TESTED | TBD |
| 质量 | NOT TESTED | TBD |
| 成本 | NOT TESTED | TBD |
| 价值 | NOT TESTED | TBD |

AI 图片/视频可选检查：角色与场景一致性、动作与剧情连贯性、生成失败率（失败数/总尝试数）、重试次数、单条成本（含失败分摊）、人工时间、可发布程度。逐项记录样本、评分规则、阈值和证据；不适用时说明原因。

## Cost｜成本

预算 / 实际 Token、API 次数、人民币、人工时间：TBD。记录时间范围、币种、模型单价来源、账单与失败重试；未知不等于零。没有可靠用量数据时说明只能软限制。

## Issues｜问题

- `blocking_issues`：待填写；每项包含 ID、范围内验收条款、复现步骤、预期、实际、证据。
- `suggestions`：待填写；建议不触发自动执行。
- `allow_retry`：false（默认不自动执行，按预算、授权和循环计数给出理由）。
- 累计计数与停止信号：TBD，遵循 [循环策略](../harness/loop-policy.md)。

## Conclusion｜结论

QA 结果：TBD（PASS / PARTIAL / FAIL / BLOCKED）。

建议决策：TBD（GO / ITERATE / STOP），依据：TBD。未完成验收时登记表保持 PENDING，不能因为模板存在而变更决策。

## Next Experiment｜下一次实验

下一步假设、输入样本、预算上限、验收阈值与待授权动作：TBD。返工仅定向复验列明阻塞问题和必要核心 smoke test，不重启全量审计。
