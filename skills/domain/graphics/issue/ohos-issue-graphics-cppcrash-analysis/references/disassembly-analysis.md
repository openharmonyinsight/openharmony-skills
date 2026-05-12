# 反汇编分析详解

## 使用llvm-objdump反汇编

```sh
# 反汇编整个so
llvm-objdump -ldC path/to/so

# 反汇编偏移范围，附带行号信息
llvm-objdump -ldC --start-address=offset1 --stop-address=offset2 path/to/so
```

## 反汇编分析要点

### 1. 确认崩溃指令

示例：

```
pc: 0000005a57a7e0ec
```

反汇编找到对应的指令：

```
3fe0ec: f9400a88    ldr x8, [x20, #10]
```

### 2. 分析指令操作

- 确认指令类型（加载，存储，算术等）
- 确认涉及的寄存器
- 确认内存访问地址的计算方式

### 3. 结合寄存器现场

从`Registers`部分读取寄存器值，计算实际的访问地址。

示例：

```
x20: 6b6b92503c687c50
崩溃指令：ldr x8, [x20, #0x10]
访问地址：0x6b6b92503c687c50 + 0x10 = 0x6b6b92503c687c60
```

验证计算出的访问地址是否与Reason中的崩溃地址一致。