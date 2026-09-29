# OPCS 操作约束

1. 每次任务先记录 `ACTIVE_PROJECT`、任务目标、允许修改路径、验收条件与预算。控制仓自身任务可用 `ACTIVE_PROJECT=opcs-control-plane`。默认只修改当前项目的登记或文档；业务代码任务必须切换到该项目登记的独立仓库并读取其规范。
2. 开工前读取 README、本文件及适用上级指令、已有任务记录；执行 `git status --short --branch`、`git diff`、`git diff --cached`。保留用户修改；禁止跨项目顺手修改或为单项目改变根目录基础设施。先理解同名文件再增量编辑。
3. 研究、开发、验证、内容按需参与。默认单执行者，必要时一次独立验证，由总控判断结束；未经授权不调用其他 Agent，不建立自动互评网络。用户要求自检时由执行者自检并明确身份，不伪称独立验收。
4. 结论区分事实、观察、推测，以文件、真实产物、运行结果和日志为证。Mock、README 声明及“运行成功”不能直接等于真实效果合格。未核实的已有项目使用 UNCONFIRMED / unverified / PENDING。
5. 阶段使用 [工作流](harness/workflow.md) 的 IDEA、RESEARCH、BUILD、VERIFY、ITERATE、CONTENT、DONE、STOPPED，另有待核实标记 UNCONFIRMED。决策仅用 PENDING、GO、ITERATE、STOP；阶段变化须附证据。
6. 严格遵循 [循环策略](harness/loop-policy.md)：单任务交接最多 6 次、开发返工最多 2 次、完整 QA 最多 1 次、同一错误自动重试最多 2 次。达到上限或其他熔断条件输出 AUTO_LOOP_STOPPED，不能自行清零。返工只处理范围内的 blocking issue，之后仅定向复验加必要的核心 smoke test。
7. 文本约束是软限制；仅运行平台提供可靠用量并有可执行控制时才能硬执行 Token 预算，不得声称 V0 已自动强制执行预算。无计量时明确未知，依据交接和返工计数止损。
8. 不记录密钥、个人信息或付费 API 凭证。付费调用、发布等外部不可逆动作遵守任务授权和运行环境规则。不得以验证为由擅自扩大成本或发布范围。
9. 结束时输出 `Completed / Changed Files / Verification / Known Issues / Next Step`，列明实际命令、通过、失败和未验证项；没有真实运行时标注“尚待运行验证”。不能凭文档修改宣称业务效果通过。
