# dual_group_interleave_test 基础设施验证

- **日期**: 2026-06-05
- **设备**: DAYU200 (RK3568), serial `7001005458323933328a027ce0003800`
- **固件**: OpenHarmony master daily build
- **测试二进制**: `dual_group_interleave_test`（19 步骤，28 个 dump 阶段）

## 验证项

| 基础设施能力 | 结果 | 备注 |
|-------------|------|------|
| NativeToken 权限获取 | PASS | `INPUT_DEVICE_CONFIGURATOR` + `INPUT_MONITORING` 权限生效 |
| Server 绕过 (OnDisplayInfo) | PASS | `UpdateDisplayInfo` 调用成功（返回 -201 是预期行为） |
| Server 绕过 (OnWindowGroupInfo) | PASS | `UpdateWindowInfo` 调用成功 |
| Server 绕过 (CheckBindDevicePermission) | PASS | `BindDeviceToDisplayGroupByDisplay` 调用成功 |
| .so 部署路径 `/system/lib/` | PASS | libmmi-server.z.so + libmmi-service.z.so 替换后服务正常 |
| SELinux permissive | PASS | `/dev/uinput` 访问和 IPC 均无拒绝 |
| compile_test.py 交叉编译 | PASS | 产物在 `code/out/rk3568/multimodalinput/input/` |
| SCP + hdc file send 部署链 | PASS | 通过 Windows 跳板机成功推送 |
| Phase-based hidumper 捕获 | PASS | 28 个 dump 阶段全部捕获，dump 文件 ~145KB |
| DumpG 3 秒 sleep | PASS | 外部脚本 1 秒轮询，无遗漏 |
| hdc shell 命令拆分 | PASS | 避免单引号包裹后不再报 `no closing quote` |

## 遇到的问题及修复

| 问题 | 原因 | 修复 |
|------|------|------|
| dump 全程为空 | Phase 文件路径 `phase.txt` vs `dual_group_phase.txt` 不匹配 | 统一路径 |
| hdc shell `no closing quote` | `hdc shell 'cmd1 && cmd2'` 语法 | 拆成多条 hdc 命令 |
| 二进制路径找不到 | 以为在 `out/rk3568/` 实际在 `code/out/rk3568/` | 跟踪 compile_test.py 的 BUILD_DIR |

## dump 数据完整性

```
总 dump 阶段: 28
有效捕获:     28/28 (100%)
dump 文件大小: ~145KB
包含段落:      RuntimeBindings, DisplayGroups, PointerStateByGroup,
              KeyboardStateByGroup, SequenceSnapshots, SoftCursorRS,
              PointerStyleByWindow, PointerDrawingRS (Display Info + Cursor Info)
```
