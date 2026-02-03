# OpenHarmony Distributed System Security Rules

## Terminology
- **主体侧 (Subject/Client)**: 业务发起的客户端
- **客体侧 (Object/Server)**: 响应业务请求的服务端
- **可信关系**: 设备间经过认证建立的信任关系

## Security Rules Checklist

### Rule 1: Object-side Authorization Control
涉及安全隐私的业务流程，禁止使用主体侧可控参数来控制客体侧关键流程，客体侧关键业务流程需在客体侧独立授权。

**Check points:**
- 禁止主体侧传递"是否弹框"标识字段来控制客体侧是否授权弹框
- 默认用户授权弹框必须弹框
- 免授权业务必须在客体侧主动注册到分布式设备管理服务
- 业务执行结束需清理免授权和预授权配置

**Related modules:** 分布式设备管理, 分布式软总线

---

### Rule 2: State Machine Context Validation
业务状态机执行必须校验上下文合法性，禁止状态机直接从中间态启动执行，禁止主体侧报文直接控制客体侧状态机流程。

**Check points:**
- 客体侧必须校验用户已经授权后，才能执行后续流程
- 禁止跳过前置状态直接进入中间态
- 对于用户感知不明显的认证方式（如超声波），必须额外校验授权状态

**Related modules:** 分布式设备管理, 分布式软总线

---

### Rule 3: No Plaintext Sensitive Data Transmission
禁止空口明文传递敏感隐私数据或者隐私数据完整hash，如PIN码，秘钥等。

**Check points:**
- 检查所有网络传输的数据包
- PIN码、秘钥必须加密传输
- 禁止传输敏感数据的完整hash

**Related modules:** 分布式设备管理, 分布式软总线, ALL

---

### Rule 4: Resource Access Parameter Validation
涉及到资源申请和访问的外部可控制输入参数，必须严格校验合法性，例如内存申请，文件访问路径等。

**Check points:**
- 内存申请大小必须校验
- 文件路径需校验路径跳转、截断、上翻等操作
- 避免访问到业务不需要的资源

---

### Rule 5: Anti-Brute Force Protection
用户鉴权流程需要在客体侧做防暴力保护，禁止业务无限重试引入暴力破解风险。

**Check points:**
- 必须实现重试次数限制
- 必须实现重试延迟机制
- 鉴权失败需记录和告警

---

### Rule 6: Server-side Security Logic
用户权限校验和防暴力方案，需要在服务端实现，禁止在客户端（调用方进程）实现对应逻辑。

**Check points:**
- 权限校验逻辑必须在服务端
- 防暴力逻辑必须在服务端
- 客户端只能做UI展示，不能做安全决策

---

### Rule 7: Trusted Relationship Lifecycle Minimization
可信关系生命周期最小化，包括可信关系授予范围，维持时长等，只给必须的进程授予可信关系，可信关系使用完毕销毁。

**Check points:**
- 业务开始前授予权限
- 业务结束清理权限
- 避免权限残留被后续业务复用
- 权限范围必须精细化

---

### Rule 8: Trusted Relationship Verification
可信关系判断必须依赖安全基础模块，例如HiChain，禁止私自实现可信判断方法。

**Check points:**
- 同账号可信关系判断：必须依赖HiChain查询凭据类型
- 点对点认证：必须通过HiChain导入PIN码绑定校验
- 分布式平台业务：可信关系查询必须来自DM ACL授权列表
- 禁止自行传输和比对账号信息或PIN码

**Related modules:** 分布式设备管理, 分布式软总线

---

### Rule 9: Trusted Relationship Persistence Timing
可信关系的落盘记录必须在安全模块认证完成后进行，禁止落盘后修改可信关系。

**Check points:**
- 禁止在认证完成前记录可信关系
- 禁止过程中记录可信等级或认证结果
- 禁止在后续流程中修改或补充主客体信息

**Related modules:** 分布式设备管理, 分布式软总线

---

### Rule 10: Secure Random Secrets
安全认证的公共秘密（例如PIN码）必须是安全随机数，禁止异常或者特定情况下返回固定值。

**Check points:**
- PIN码生成必须使用加密安全的随机数生成器
- 禁止在错误路径返回固定值
- 检查所有返回secret的代码路径

**Related modules:** 分布式设备管理, 分布式软总线

---

### Rule 11: Resource Cleanup
安全相关业务流程使用结束，彻底清理相关资源，包括缓存，随机秘钥，随机数，监听器，设备间网络连接等。

**Check points:**
- 业务结束必须清理缓存
- 清理随机秘钥和随机数
- 移除监听器
- 关闭设备间网络连接

**Related modules:** 分布式设备管理, 分布式软总线

---

### Rule 12: Sensitive Data Authorization and Audit
敏感数据和硬件使用前，需要用户授权，使用中，明示用户，使用后，需要有使用记录。

**Check points:**
- 使用前必须获得用户授权
- 使用中必须明示用户（UI指示）
- 使用后必须记录审计日志

---

### Rule 13: Minimal Permission Configuration
进程和文件权限配置最小化，禁止使用不需要的权限，禁止授权范围过大，例如不需要分布式功能的sa配置启用rpc能力，文件权限赋予用户组其他用户。

**Check points:**
- 只申请必需的权限
- 不需要分布式功能的SA禁止启用rpc能力
- 文件权限禁止赋予用户组其他用户
- 检查SA配置和文件权限设置

---

### Rule 14: Secure Switch Default Values
控制业务流和权限的开关标记，默认值应该是非法值，禁止默认值放通。

**Check points:**
- 所有控制业务流的开关，默认值必须是"禁用"或"非法"
- 禁止默认值设置为"放通"状态
- 必须显式启用才能放通

---

### Rule 15: Device Legitimacy Verification
华为设备间的业务认证，必须做设备合法性校验，校验激活证书链，避免非法设备通过分布式业务获得高等级权限或者分布式能力。

**Check points:**
- 必须校验激活证书链
- 验证设备合法性
- 防止非法设备获得高权限

---

### Rule 16: User Isolation for Distributed Trust
分布式业务在设备间的可信关系，需要基于用户进行隔离，分布式业务需要校验当前双端业务所在前台用户之间有业务所需可信关系时，分布式业务才能进行；如果发生用户切换，被切换到后台的用户下的分布式业务需要中断。

**Check points:**
- 可信关系必须基于用户隔离
- 必须校验双端前台用户的可信关系
- 用户切换时必须中断后台用户的分布式业务

---

### Rule 17: Business-level Key Isolation
分布式软总线传输秘钥，需要针对业务进行隔离，不同业务使用不同秘钥，禁止使用设备级传输秘钥。

**Check points:**
- 不同业务必须使用不同传输秘钥
- 禁止使用设备级传输秘钥
- U0用户下的SA通信，传输秘钥需做到用户级隔离

---

### Rule 18: Legacy Protocol Cleanup
分布式业务为了历史兼容性，可能对历史不安全协议进行了放通处理，引入安全风险，需要进行大数据打点评估现网使用量足够小后，进行兼容代码的删除。

**Check points:**
- 识别历史不安全协议的兼容代码
- 确认是否有大数据打点评估
- 确认现网使用量是否足够小
- 制定删除不安全兼容代码的计划

---

## Quick Reference Keywords

When reviewing code, check for these patterns that may indicate violations:

- **跨设备传输** (Cross-device transmission) → Check Rules 3, 8, 15, 17
- **状态机** (State machine) → Check Rule 2
- **授权/鉴权** (Authorization/Authentication) → Check Rules 1, 5, 6, 8, 12
- **PIN码/秘钥** (PIN/Secret) → Check Rules 3, 8, 9, 10
- **资源申请** (Resource allocation) → Check Rule 4
- **权限配置** (Permission config) → Check Rules 7, 13
- **开关标记** (Switch/Flag) → Check Rule 14
- **用户切换** (User switch) → Check Rule 16
- **兼容代码** (Compatibility code) → Check Rule 18
