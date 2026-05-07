# 覆盖率扫描详解

> APICoverageDetector 工具使用指南 + 异步扫描流程

## 概述

APICoverageDetector 是 OpenHarmony 官方的 API 覆盖率扫描工具，本技能通过异步封装（`scripts/async_coverage_scan.py`）集成于 Phase 2（初始扫描）和 Phase 9（验证扫描）。

异步扫描允许在后台运行覆盖率扫描，同时可以进行其他操作。特别适用于大型子系统或长时间运行的覆盖率分析任务。

---

## APICoverageDetector 工具

### 平台限制

APICoverageDetector 仅支持 Windows 环境（核心为 `.bat` 脚本 + `.exe` 可执行文件）。

| 环境 | 是否可用 | 路径示例 | 说明 |
|------|---------|---------|------|
| Windows 原生 | 可用 | `D:\APICoverageDetector` | 直接运行 |
| WSL | 可用 | `/mnt/d/APICoverageDetector` | 通过 WSL 路径映射访问 Windows 侧工具 |
| Linux 计算云/远程服务器 | **不可用** | — | 只能让用户提供已有的覆盖率扫描结果 |

### 路径配置

**工具路径**：从 `.oh-xts-config.json` 的 `scan_tool_root` 字段读取。若路径不存在，不应自动猜测，而应向用户提供以下选项：
1. 提供正确的 APICoverageDetector 安装路径，更新配置后重试
2. 直接提供已有的覆盖率扫描结果（CSV/XLSX 文件）
3. 跳过覆盖率扫描步骤，直接按用户要求生成测试用例

**路径建议**：推荐将 APICoverageDetector 放在磁盘根目录（如 `D:\APICoverageDetector`），而非嵌套在深层目录中。原因：
- XTS 测试工程目录层级通常很深（如 `test/xts/acts/{subsystem}/{suite}/entry/src/main/ets/...`），文件总量大
- APICoverageDetector 扫描时会生成大量中间文件和结果文件，路径会在此基础之上进一步延伸
- Windows 系统默认路径长度限制为 260 字符，深层嵌套极易触发路径超限，导致扫描失败或结果文件写入不完整

### 主要组件

- `APICoverageDetector_ArkTS.bat`: ArkTS 覆盖率扫描脚本
- `APICoverageDetector_C.bat`: C/C++ 覆盖率扫描脚本
- `arkts_entrance/`: ArkTS 静态检查工具包

### 使用方式

```bash
# Windows - ArkTS 扫描
cd {scan_tool_root}
APICoverageDetector_ArkTS.bat

# Windows - C/C++ 扫描
APICoverageDetector_C.bat
```

### 输出位置

- 扫描结果：`{scan_tool_root}/results/`
- 覆盖率数据：`{skill_root}/.coverage_data/`
- 未覆盖 API 列表：`{skill_root}/.coverage_data/uncovered_apis.json`

---

## 异步扫描工具

### 工具位置（异步扫描封装）

- **主要工具**: `scripts/async_coverage_scan.py`
- **扫描执行器**: `APICoverageDetector/arkts_entrance/arkts_entrance.exe`
- **结果目录**: `APICoverageDetector/results/`
- **日志目录**: `APICoverageDetector/log/`

## 使用方法

### 1. 基本命令

```bash
# 启动异步扫描
python scripts/async_coverage_scan.py start

# 查看扫描状态
python scripts/async_coverage_scan.py status

# 获取扫描结果
python scripts/async_coverage_scan.py results

# 停止扫描
python scripts/async_coverage_scan.py stop
```

### 2. 在Skill中的使用

#### Phase 2 - 初始覆盖率扫描
```python
# 启动异步扫描
success, message, pid = scanner.start_scan()
if success:
    print(f"扫描已启动，PID: {pid}")
    print("可以进行其他操作...")
    
    # 检查进度
    status = scanner.get_status()
    print(f"当前状态: {status['status']}")
    
    # 等待完成（可选）
    while status['status'] == 'running':
        time.sleep(30)
        status = scanner.get_status()
        print(f"进度: {status['progress']['progress_percent']}%")
```

#### Phase 9 - 覆盖率验证
```python
# 启动验证扫描
success, message, pid = scanner.start_scan()
if success:
    print(f"验证扫描已启动，PID: {pid}")
    
    # 等待完成
    while scanner.is_running():
        time.sleep(30)
        status = scanner.get_status()
        print(f"状态: {status['status']}")
    
    # 获取结果
    results = scanner.get_results()
    print(f"扫描完成，结果: {results}")
```

## 扫描流程详解

### 1. 启动流程
1. **验证配置**: 检查配置文件和路径
2. **启动进程**: 后台运行 `arkts_entrance.exe`
3. **发送输入**: 自动配置交互参数
4. **保存状态**: 记录PID和初始状态
5. **启动监控**: 后台线程监控日志和进度

### 2. 监控流程
1. **日志监控**: 实时读取扫描日志
2. **进度解析**: 解析10个扫描阶段
3. **状态更新**: 定期更新状态文件
4. **错误检测**: 检测扫描异常

### 3. 完成流程
1. **进程检测**: 检测扫描进程是否结束
2. **状态更新**: 更新最终状态
3. **结果保存**: 保存扫描结果文件
4. **清理**: 清理临时文件

## 状态说明

| 状态 | 描述 | 处理方式 |
|------|------|----------|
| `idle` | 空闲状态 | 可以启动新扫描 |
| `running` | 扫描中 | 可以监控进度 |
| `completed` | 扫描完成 | 可以获取结果 |
| `failed` | 扫描失败 | 检查错误信息 |

## 进度信息

```json
{
  "current_stage": 4,
  "total_stages": 10,
  "stage_name": "(4/10) 扫描覆盖率",
  "progress_percent": 40,
  "timestamp": "2025-01-16T10:30:00"
}
```

## 扫描阶段

1. `(1/10) count工具` - 统计工具
2. `(2/10) metrics工具` - 指标工具
3. `(3/10) 检查metrics工具结果` - 检查结果
4. `(4/10) 扫描覆盖率` - 扫描覆盖率
5. `(5/10) 汇总覆盖率信息` - 汇总信息
6. `(6/10) 统计覆盖度` - 统计覆盖度
7. `(7/10) 检查参数规格` - 检查参数
8. `(8/10) 检查错误码` - 检查错误码
9. `(9/10) 检查返回值` - 检查返回值
10. `(10/10) 格式化输出` - 格式化输出

## 结果文件

扫描完成后，结果文件保存在：

```
APICoverageDetector/results/
├── open_source/sdk_result.xlsx
├── dynamic/sdk_result.xlsx
└── static/sdk_result.xlsx
```

## 配置要求

确保以下配置正确：

```json
{
  "case_path": {
    "open_source": [
      "{xts_acts_path}"
    ]
  },
  "api_path": {
    "open_source": "%SDK_PATH%\\ets"
  }
}
```

## 最佳实践

1. **启动时机**: 在需要长时间等待时使用异步扫描
2. **进度监控**: 定期检查进度，避免长时间无响应
3. **结果获取**: 扫描完成后及时获取结果
4. **资源管理**: 及时停止未完成的扫描
5. **错误处理**: 监控失败状态，及时处理异常

## 故障排除

### 常见问题

1. **扫描启动失败**
   - 检查配置文件路径
   - 验证测试用例路径
   - 确认可执行文件存在

2. **进度更新异常**
   - 检查日志文件权限
   - 确认日志文件存在
   - 重新启动监控线程

3. **扫描长时间无响应**
   - 检查进程状态
   - 查看日志文件
   - 必要时手动停止

### 调试方法

```bash
# 查看状态
python scripts/async_coverage_scan.py status

# 查看结果
python scripts/async_coverage_scan.py results

# 检查日志
tail -f APICoverageDetector/log/arkts_runner.log
```

## 集成到Skill

在skill的各个phase中，可以通过以下方式集成异步扫描：

```python
# 在Phase 2/Phase 9中使用
from scripts.async_coverage_scan import AsyncCoverageScanner

scanner = AsyncCoverageScanner()

# 启动异步扫描
success, message, pid = scanner.start_scan()
if success:
    # 可以进行其他操作
    # ...
    
    # 检查扫描状态
    while scanner.is_running():
        status = scanner.get_status()
        print(f"扫描进度: {status['progress']['progress_percent']}%")
        time.sleep(60)
    
    # 获取扫描结果
    results = scanner.get_results()
    # 处理结果...
```

这样可以实现高效的异步覆盖率扫描流程。