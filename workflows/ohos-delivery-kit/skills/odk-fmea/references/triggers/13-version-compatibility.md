# 版本配套可靠性故障模式 触发索引

> 两级加载第一级：只读本表做扫描判定；条目触发条件命中后，到 [../13-version-compatibility.md](../13-version-compatibility.md) 读取该 `### ID` 条目详情（大文件可用 Read offset/limit 按锚点局部读）。

| ID | 故障模式 | 触发条件（可判定的代码/设计特征） |
|---|---|---|
| V-01 | 软件版本不匹配（ROM / HAP / Framework Version Mismatch） | 存在高/低版本 ROM 与 HAP 组合运行场景；框架（ArkUI、Ability Runtime）版本与应用版本可不对称；依赖 CCM 配置且无合法性校验与默认值 |
| V-02 | 数据版本不兼容（Data Version Incompatibility） | 数据库 schema 升级/降级路径缺失或跳跃（v1→v3 无 v2）；数据序列化格式/加密编码跨版本变更；数据无版本号与向前兼容解析、无损坏自愈 |
| V-03 | 外部依赖版本不兼容（External Dependency Version Mismatch） | 依赖外部服务（CAAS、华为账号、联系人库、媒体库、意图框架等）版本可变；接口无版本号协商；依赖服务死亡重连后未重新协商版本 |
| V-04 | 跨设备版本不兼容（Cross-Device Version Mismatch） | 多端协同场景（手机/PAD/PC/大屏/手表）ROM 版本差异；协议版本无发现阶段协商（不兼容时拒绝或降级）；特性无按版本分级启用 |
| V-05 | 升级路径中断 / 版本跳跃（Upgrade Path Interrupted / Version Skip） | OTA 升级可被断电/断网中断；独立升级包与 ROM 配套关系无预校验；升级无事务化（原子替换+A/B 回滚）与 filelist/签名完整性校验 |
| V-06 | 配置版本失效（Configuration Version Invalid） | CCM 配置可为空/无效/过期；主题包/壁纸/时钟组件等资源包版本与编辑器版本可不对称；配置读取无合法性校验、默认值降级与原子更新 |
