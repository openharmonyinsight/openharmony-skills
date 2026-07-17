# 常见问题排查

> **版本**: 1.0.0
> **更新日期**: 2026-04-25

## 扫描执行问题

### Q1: 扫描卡住不动或超时

**现象**: 扫描开始后长时间无输出，或报单规则超时。

**原因**: 大型代码库（5万+文件）在首次扫描时需要构建缓存。

**解决方案**:
```bash
# 指定并行数加速
/check-xts-code-quality /path/to/code --level all --parallel 8

# 先只扫描Critical级别
/check-xts-code-quality /path/to/code --level critical

# 排除无关目录
/check-xts-code-quality /path/to/code --exclude vendor,docs,examples
```

### Q2: 提示"No authentication available"

**现象**: PR模式下报认证错误。

**解决方案**:
1. 安装 oh-gc CLI（推荐）:
   ```bash
   npm install -g @oh-gc-cli
   oh-gc auth:login
   ```
2. 或提供 Token:
   ```bash
   /check-xts-code-quality --pr <URL> --token <YOUR_TOKEN>
   ```
3. 或设置环境变量:
   ```bash
   export GITCODE_TOKEN=<YOUR_TOKEN>
   ```

Token 获取: https://gitcode.com/-/profile/personal_access_tokens

### Q3: 提示"ripgrep not installed"

**现象**: 扫描时提示未安装 ripgrep。

**影响**: 无 ripgrep 时扫描仍可运行，但速度较慢（回退到 Python 正则）。

**解决方案**:
```bash
# Ubuntu/Debian
sudo apt install ripgrep

# macOS
brew install ripgrep

# CentOS/RHEL
sudo yum install ripgrep
```

### Q4: PR扫描报"No changed files"

**现象**: `pr_scanner.py` 返回0个变更文件。

**原因**: PR中不包含 `.ets`/`.ts`/`.js` 等可扫描文件。

**解决方案**: 确认PR确实修改了测试代码文件，而非仅修改文档或配置。

## 报告问题

### Q5: Excel报告打开乱码

**现象**: Excel打开报告显示乱码。

**原因**: 文件编码问题。报告使用 UTF-8 BOM 编码。

**解决方案**:
- 使用 Excel 2016+ 或 WPS 打开
- 如果仍乱码，用 Excel 的"数据"→"从文本导入"，选择 UTF-8 编码

### Q6: 问题数为0的规则没有出现在报告中

**现象**: 某些规则在扫描范围但报告中未显示。

**原因**: 这是 BUG，不应出现。所有本次执行的规则必须全部展示。

**排查**:
1. 检查终端输出的规则列表是否包含该规则
2. 检查 `{SCAN_PATH}/.xts_scan/scan_meta.json` 和 `all_issues.json` 是否存在
3. 如确认是BUG，请提交 issue

### Q7: snippet字段显示为描述文本而非代码

**现象**: Excel中"代码片段"列显示的是"缺少断言"等描述，而非真实代码。

**原因**: scanner 未正确提取代码行。

**排查**: 检查对应scanner的 `snippet` 赋值是否使用了 `lines[line_number - 1]`。详见 `references/TRAPS.md`。

## 扫描结果问题

### Q8: R010报错"无法获取映射表"

**现象**: R010扫描失败或结果为0。

**原因**: R010需要从远程仓库获取3个配置文件构建子系统-部件映射表，网络不通时会失败。

**解决方案**:
- 确认网络可访问 gitee.com
- 如果网络受限，R010会被跳过但不影响其他规则

### Q9: R012签名检测不准确

**现象**: R012误报或漏报签名证书问题。

**原因**: p7b文件是二进制格式，解析依赖正则匹配APL等级标记。

**解决方案**:
- 确认 `.p7b` 文件是标准格式
- 参见 `guides/R012_p7b_signature/R012_FIX_GUIDE.md`

### Q10: Sta工程检测不到

**现象**: `--sta-mode sta` 提示无Sta工程。

**原因**: Sta工程通过 BUILD.gn 模板类型识别：
- `ohos_js_app_static_suite`
- `ohos_js_app_assist_static_suite`
- 目录名以 `Static`/`static` 结尾

**解决方案**: 确认工程BUILD.gn使用了正确的模板类型。

## 性能优化

### Q11: 大型代码库扫描太慢

**解决方案**:
```bash
# 1. 安装 ripgrep（10x+ 加速）
sudo apt install ripgrep

# 2. 排除无关目录
/check-xts-code-quality /path/to/code --exclude vendor,docs,examples,third_party

# 3. 指定规则而非全量
/check-xts-code-quality /path/to/code --rules R001,R003,R201,R202

# 4. 按类别扫描
/check-xts-code-quality /path/to/code --category technical

# 5. 增加并行数
/check-xts-code-quality /path/to/code --parallel 16
```

### Q12: 内存占用过高

**现象**: 扫描大型代码库时内存占用很高。

**原因**: FileContentCache 缓存了所有文件内容（上限80000文件）。

**解决方案**: 减少 `--parallel` 数量（减少进程数=减少内存拷贝），或使用 `--rules` 限制扫描范围。

## 自动修复问题

### Q13: --fix 修复后问题数未减少

**现象**: 执行 `--fix` 后重新扫描，问题数相同或更多。

**原因**: 某些修复可能引入新问题（如R016修复后可能触发R018）。

**解决方案**: 按规则逐个修复而非批量修复，每修复一条规则后验证：
```bash
/check-xts-code-quality /path/to/code --rules R008 --fix
/check-xts-code-quality /path/to/code --rules R008  # 验证
/check-xts-code-quality /path/to/code --rules R016 --fix
/check-xts-code-quality /path/to/code --rules R016  # 验证
```

### Q14: 哪些规则支持自动修复

**当前仅支持6条规则**: R008、R011、R012、R014、R016、R018。

其余23条规则不支持自动修复，需手动处理。详细修复指南见 `guides/FIX_GUIDE.md`。

## 自定义规则问题

### Q15: 自定义规则没有生效

**排查清单**:
1. 确认JSON文件格式正确（无语法错误）
2. 确认 `type` 字段为 `extension` 或 `custom`
3. 确认 `patterns` 中的正则语法正确
4. 确认文件路径正确（`--rules-file` 需绝对路径或相对当前目录）
5. 确认 `scope.file_types` 包含目标文件类型

### Q16: 如何调试自定义规则的正则

```bash
# 在目标文件中手动测试正则
python3 -c "
import re
pattern = r'your_pattern_here'
with open('target_file.test.ets') as f:
    for i, line in enumerate(f, 1):
        if re.search(pattern, line):
            print(f'Match at line {i}: {line.strip()[:80]}')
"
```

## 更多帮助

- [使用指南](USAGE.md)
- [修复指南](../guides/FIX_GUIDE.md)
- [已知陷阱](../references/TRAPS.md)
