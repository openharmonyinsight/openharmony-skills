# SO崩溃栈分析指南

## 目录

- 概述
- 数据库资源
- 快速查询
  - 1. 查询指定SO库
  - 2. 查询子系统下所有SO库
  - 3. 查看所有映射
- 分析流程
  - 第一步：提取崩溃栈
  - 第二步：识别SO库
  - 第三步：查询子系统归属
  - 第四步：确定责任子系统
  - 第五步：查询责任人
- 常见场景
  - 场景1：单一SO库崩溃
  - 场景2：多个SO库调用链
  - 场景3：未知SO库
- 数据库直接操作
  - 添加新SO库映射
  - 批量导入SO库映射
  - 查询未分配责任人的SO库

---

## 概述

当XTS测试遇到cppcrash或native崩溃时，需要分析崩溃栈中的SO库归属，以确定问题责任子系统。

## 数据库资源

**SO库映射表**: `so_mapping`

包含54个常见OpenHarmony系统SO库的子系统归属信息。

**查询工具**: `scripts/query_db.py so`

## 快速查询

### 1. 查询指定SO库

```bash
# 查询单个SO库
python3 scripts/query_db.py so libace.z.so

# 模糊查询（包含ace的所有SO库）
python3 scripts/query_db.py so ace
```

输出示例：
```
======================================================================
SO库匹配结果 (共3条)
======================================================================

1. libace.z.so
   子系统: ArkUI
   说明: ArkUI框架核心库

2. libace_compat.z.so
   子系统: ArkUI
   说明: ArkUI兼容层

3. libace_napi.z.so
   子系统: ArkUI
   说明: NAPI桥接库
```

### 2. 查询子系统下所有SO库

```bash
# 查询元能力子系统的所有SO库
python3 scripts/query_db.py so 元能力

# 查询ArkUI子系统的所有SO库
python3 scripts/query_db.py so ArkUI
```

输出示例：
```
======================================================================
子系统 '元能力' 的SO库 (共5个)
======================================================================

1. libability_manager.z.so
   说明: Ability管理服务
   责任人: 钟柏松 (00839045)

2. libability_runtime.z.so
   说明: Ability运行时
   责任人: 钟柏松 (00839045)

3. libams.z.so
   说明: Ability管理服务
   责任人: 钟柏松 (00839045)

4. libappmsmgr.z.so
   说明: 应用管理服务
   责任人: 钟柏松 (00839045)
```

### 3. 查看所有映射

```bash
python3 scripts/query_db.py so all
```

## 分析流程

### 第一步：提取崩溃栈

从hilog或cppcrash日志中提取崩溃栈信息：

**hilog日志示例**：
```
04-15 10:23:45.678   1234   5678 E C01800/HiAppEvent: [event] name=CPP_CRASH
04-15 10:23:45.678   1234   5678 E C01800/HiAppEvent: backtrace= 
    #00 pc 00000000000a5b3c /system/lib64/libace.z.so
    #01 pc 00000000000c7a5d /system/lib64/libark_jsruntime.so
    #02 pc 00000000000b3f21 /system/lib64/libability_runtime.z.so
```

**cppcrash文件示例**：
```
Build fingerprint: OpenHarmony/...
Hardware: ...
Revision: ...

*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
ABI: 'arm64'
Timestamp: 2024-04-15 10:23:45.678901234+0800
Process name: com.example.hap
pid: 1234, tid: 5678, name: Thread-1  >>> com.example.hap <<<
uid: 20010042
signal 11 (SIGSEGV), code 1 (SEGV_MAPERR), fault addr 0x0
Cause: [TID:5678][signal:11][Cause:Segmentation fault]

Stack trace:
  #00 pc 00000000000a5b3c /system/lib64/libace.z.so
  #01 pc 00000000000c7a5d /system/lib64/libark_jsruntime.so
  #02 pc 00000000000b3f21 /system/lib64/libability_runtime.z.so
```

### 第二步：识别SO库

从崩溃栈中提取SO库名：
```
libace.z.so
libark_jsruntime.so
libability_runtime.z.so
```

### 第三步：查询子系统归属

```bash
python3 scripts/query_db.py so libace.z.so
python3 scripts/query_db.py so libark_jsruntime.so
python3 scripts/query_db.py so libability_runtime.z.so
```

查询结果：
- libace.z.so → ArkUI子系统
- libark_jsruntime.so → ArkUI子系统
- libability_runtime.z.so → 元能力子系统

### 第四步：确定责任子系统

根据崩溃栈分析：
- **主崩溃库**：#00位置的libace.z.so（ArkUI）
- **调用链**：libability_runtime.so（元能力）→ libark_jsruntime.so（ArkUI）→ libace.z.so（ArkUI）

**定界结论**：
- 问题归属：ArkUI子系统
- 崩溃位置：libace.z.so + 0xa5b3c
- 建议：转交ArkUI责任人分析

### 第五步：查询责任人

```bash
# 查询子系统 SO 库归属与责任人
python3 scripts/query_db.py so --subsystem ArkUI
```

## 常见场景

### 场景1：单一SO库崩溃

**崩溃栈**：
```
#00 pc 00012345 /system/lib64/libwindow.z.so
```

**分析**：
```bash
python3 scripts/query_db.py so libwindow.z.so
# 输出：子系统=窗口
```

**定界**：窗口子系统

### 场景2：多个SO库调用链

**崩溃栈**：
```
#00 pc 000a5b3c /system/lib64/librender_service_client.z.so
#01 pc 000c7a5d /system/lib64/libwindow.z.so
#02 pc 000b3f21 /system/lib64/libability_runtime.z.so
```

**分析**：
```bash
python3 scripts/query_db.py so librender_service_client
# 输出：子系统=图形

python3 scripts/query_db.py so libwindow
# 输出：子系统=窗口
```

**定界**：
- 主崩溃：图形子系统（librender_service_client.z.so）
- 调用链：元能力 → 窗口 → 图形
- 问题归属：图形子系统

### 场景3：未知SO库

**崩溃栈**：
```
#00 pc 00012345 /system/lib64/libunknown_lib.z.so
```

**分析**：
```bash
python3 scripts/query_db.py so libunknown_lib
# 输出：未找到匹配的SO库
```

**处理方式**：
1. 在数据库中添加新映射：
```sql
INSERT INTO so_mapping (so_name, subsystem, description) 
VALUES ('libunknown_lib.z.so', '待分析', '未知库，需进一步分析');
```

2. 根据SO库名推测子系统：
   - libability* → 元能力
   - libwindow* → 窗口
   - librender* → 图形
   - libmedia* → 媒体

3. 查询OpenHarmony源码确认归属：
```bash
# 在源码中搜索
find . -name "libunknown_lib.z.so"
```

## 数据库直接操作

### 添加新SO库映射

```bash
sqlite3 ~/.opencode/skills/ohos-issue-xts-log-analysis/data/xts_rules.db "
INSERT INTO so_mapping (so_name, subsystem, description, owner_name, owner_zhanma)
VALUES ('libnew.z.so', '子系统', '说明', '负责人', '詹码');
"
```

### 批量导入SO库映射

```bash
sqlite3 ~/.opencode/skills/ohos-issue-xts-log-analysis/data/xts_rules.db << 'EOF'
INSERT INTO so_mapping (so_name, subsystem, description) VALUES
('libexample1.z.so', '子系统A', '示例库1'),
('libexample2.z.so', '子系统B', '示例库2');
EOF
```

### 查询未分配责任人的SO库

```bash
sqlite3 ~/.opencode/skills/ohos-issue-xts-log-analysis/data/xts_rules.db "
SELECT so_name, subsystem 
FROM so_mapping 
WHERE owner_name IS NULL;
"
```

### 更新责任人信息

```bash
sqlite3 ~/.opencode/skills/ohos-issue-xts-log-analysis/data/xts_rules.db "
UPDATE so_mapping 
SET owner_name='张三', owner_zhanma='00812345' 
WHERE subsystem='图形';
"
```

## 子系统统计

当前数据库包含54个SO库映射，分布如下：

| 子系统 | SO库数量 | 主要SO库 |
|--------|----------|----------|
| 媒体 | 6 | libmedia.z.so, libavcodec.z.so, libcamera.z.so |
| 图形 | 5 | librender_service_client.z.so, libsurface.z.so |
| 分布式数据 | 5 | libdistributeddata.z.so, librdb.z.so |
| 元能力 | 4 | libability_runtime.z.so, libams.z.so |
| ArkUI | 5 | libace.z.so, libark_jsruntime.so |
| 网络 | 4 | libnetstack.z.so, libhttp.z.so |
| 窗口 | 4 | libwindow.z.so, libwindow_manager.z.so |
| 包管理 | 4 | libbundle.z.so, libbundle_manager.z.so |
| 内核 | 4 | libhilog.z.so, libhiview.z.so |
| 电源管理 | 3 | libpowermgr.z.so, libbattery.z.so |
| 安全 | 3 | libaccesstoken.z.so, libpermission.z.so |
| 事件通知 | 3 | libeventhandler.z.so, libnotification.z.so |
| 账号 | 2 | libaccount.z.so, libosaccount.z.so |
| 用户程序框架 | 2 | libnapi.z.so, libnativeapi.z.so |

## 注意事项

1. **优先级**：崩溃栈#00位置的SO库是主崩溃点，优先分析
2. **调用链**：从下往上（#02→#01→#00）是调用顺序，帮助理解问题上下文
3. **系统库**：/system/lib64/下的库是系统库，/vendor/lib64/下是厂商库
4. **第三方库**：应用私有库（如/data/app/el1/bundle/public/.../libs/）通常不是系统问题
5. **动态更新**：遇到未知SO库时，及时更新数据库映射

## 参考资料

- [崩溃问题专项流程](../modules/L0_PreAnalysis/CrashAnalysis.md)
- [数据库查询手册](../docs/database-schema.md)
- [SKILL.md](../SKILL.md) - 完整分析流程
