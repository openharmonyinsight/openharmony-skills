# 工具链 Wrapper 配方（透明包装注入 flag）

> **Scope**: prebuilt 工具链缺指令集扩展（如 zicsr）时的 wrapper 生成通用配方
> **When**: mode=wrapper 生成 wrapper 脚本时读取
> 来源：实测沉淀（`compiler_fix_playbook.md` §4 提炼工具链 wrapper 通用部分）

## 1. 透明包装原则

- wrapper 只做**透明包装**：`exec 原gcc "$@" <注入flag>`——不 patch prebuilt 二进制本身（patch 二进制不可维护且破坏完整性校验）。
- 原始 gcc 重命名为 `.real`（如 `riscv32-unknown-elf-gcc` → `riscv32-unknown-elf-gcc.real`），wrapper 用原名顶替，下游所有编译命令**无感**，无需逐条改命令。
- 注入前判断参数中**尚未包含**该扩展才追加，避免 `-march` 重复注入。
- 典型场景：prebuilt GCC 的编译器前端（cc1）支持 zicsr 扩展，但默认 `-march` 不暴露 → wrapper 把 `rv32imac` 改写为 `rv32imac_zicsr`。

## 2. 简单 wrapper（固定注入一个 flag）

```bash
#!/bin/sh
# {prefix}gcc wrapper: 注入 -march=rv32imac_zicsr
exec "{path}/{prefix}gcc.real" "$@" -march=rv32imac_zicsr
```

适合 special_flags 固定、所有编译场景都缺同一扩展的情况。

> 注意：末尾追加的 `-march` 会覆盖命令行传入的任何 `-march`（含其已有扩展），仅适合编译参数完全固定的场景；需保留用户 ISA 串时用 §3 参数感知版。

## 3. 参数感知 wrapper（v3，推荐）

解析参数：compile-only（`-c/-S/-E`）时才追加 size 优化 flag；对 `-march=rv32imac...` 的 ISA 串**末尾追加** `_zicsr`（尚未包含时；保留串上已有的其他扩展和版本号，不做整体替换）。分离式传值（`-march rv32imac`）用状态机识别——**只有紧跟 `-march` 之后的参数才是 ISA 串**，其余裸值（源文件名 `rv32imac_test.c`、`-o` 输出名、链接输入等）一律原样转发：

```bash
#!/bin/bash
# {prefix}gcc (wrapper v3)
REAL_GCC="{path}/{prefix}gcc.real"  # 引号：路径含空格（如 "tool chain/gcc.real"）也能执行

# 解析参数: 是否为 compile-only (非 link)
IS_COMPILE_ONLY=false
for arg in "$@"; do
    case "$arg" in
        -c|-S|-E) IS_COMPILE_ONLY=true; break ;;
    esac
done

# 注入 zicsr 到 -march (如果尚未包含) —— 末尾追加而非整体替换，保留已有扩展/版本号。
# 分离式传值（-march rv32imac）用状态机：只有紧跟 -march 之后的参数才是 ISA 串，
# 其余裸值（源文件名 rv32imac_test.c、-o 输出名、链接输入等）一律原样转发。
NEW_ARGS=()
EXPECT_ISA=false
for arg in "$@"; do
    case "$arg" in
        -march)
            NEW_ARGS+=("$arg")
            EXPECT_ISA=true          # 下一个参数是 ISA 值
            ;;
        -march=rv32imac*)
            # -march=rv32imac[已带其他扩展/版本号]：仅追加缺失的 zicsr
            if [[ "$arg" == *zicsr* ]]; then
                NEW_ARGS+=("$arg")          # 已含 zicsr（含版本化 zicsr1p0），原样保留
            else
                NEW_ARGS+=("${arg}_zicsr")  # 如 -march=rv32imac_zifencei → -march=rv32imac_zifencei_zicsr
            fi
            EXPECT_ISA=false
            ;;
        rv32imac*)
            if $EXPECT_ISA; then
                # 紧跟 -march 的 ISA 值（-march rv32imac... 分离式形态）：只追加
                if [[ "$arg" == *zicsr* ]]; then
                    NEW_ARGS+=("$arg")
                else
                    NEW_ARGS+=("${arg}_zicsr")
                fi
            else
                NEW_ARGS+=("$arg")          # 普通裸值（如源文件名 rv32imac_test.c），不动
            fi
            EXPECT_ISA=false
            ;;
        *)
            NEW_ARGS+=("$arg")
            EXPECT_ISA=false
            ;;
    esac
done

# compile-only: 追加 size optimization flags（"$REAL_GCC" 加引号：空格路径）
if $IS_COMPILE_ONLY; then
    exec "$REAL_GCC" "${NEW_ARGS[@]}" -Os -fdata-sections -ffunction-sections
else
    exec "$REAL_GCC" "${NEW_ARGS[@]}"
fi
```

**`-march` 改写效果对照**（追加式，保留原有扩展/版本号）：

| 输入 | 转发为 | 说明 |
|------|--------|------|
| `-march=rv32imac` | `-march=rv32imac_zicsr` | 基础串追加 |
| `-march=rv32imac_zifencei` | `-march=rv32imac_zifencei_zicsr` | 已有 zifencei 保留，追加 zicsr |
| `-march=rv32imac_zicsr` | 原样 | 已含 zicsr，不重复注入 |
| `-march=rv32imac_zicsr1p0` | 原样 | 版本化 zicsr 同样视为已含 |
| `-march=rv32imac2p0` | `-march=rv32imac2p0_zicsr` | 版本化基础串追加 |
| `-march=armv7e-m` | 原样 | 非 rv32imac 目标不动 |
| `-march rv32imac`（分离式） | `-march rv32imac_zicsr` | 紧跟 -march 的值才追加 |
| `-c rv32imac_test.c` | 原样 | 普通源文件名不是 ISA，不动 |
| `-o rv32imac_out.bin` | 原样 | 输出文件名不动 |

## 4. as / ld 也要包

`unknown instruction` 出现在**汇编/链接**阶段时，说明 `as`/`ld` 不认识新指令（cc1 编出的汇编含 csrrw 等）——需为 `as` 和 `ld` 同样建 wrapper（用含该扩展的 binutils 版本顶替），只包 gcc 不够。

## 5. GCC 版本兼容实测要点（RISC-V zicsr 场景）

| 工具链 | 表现 | 处置 |
|--------|------|------|
| GCC 7.3.0（老 prebuilt） | cc1 不认识 `_zicsr`——太旧，不支持该指令集扩展 | wrapper 注入也无效，**换新工具链** |
| GCC 13.2.0（新 prebuilt） | cc1 支持 zicsr，但默认 `-march` 不暴露、as/ld 可能缺 | wrapper 注入 `_zicsr` 即可，必要时 as/ld 也包 |
| 源码编译 riscv-gnu-toolchain | 20-40min，newlib 子模块 fetch 易卡住 | 兜底选项，优先 wrapper/换 prebuilt |

> 教训：打 wrapper 前必须先实测当前工具链**真实版本**（`{prefix}gcc --version` + 测试编译），不要凭假设选方案——实测曾因错误假设版本号（假设 13.2.0 实际 7.3.0）打出 4 个无效 patch 后全部退回。

## 6. 验证与落盘

1. wrapper 生成后**必须用 wrapper 真跑测试编译**：`echo 'int main(){return 0;}' | {wrapper} -x c - -o /dev/null`——编过才算 wrapper 可用。
2. wrapper 路径写入 `workflow_config.yaml` 的 `toolchain.wrapper`，编译命令统一用 wrapper 替代原 gcc。
3. 深入的工具链适配 patch 案例（GT patch 全集）再读 `skills/ohos-dev-build-config/references/compiler_fix_playbook.md` §4。
