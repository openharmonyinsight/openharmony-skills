# ArkTS-Sta Playground

通过 ArkTS-Sta Playground HTTP API 执行或编译 ArkTS-Sta 代码片段，用于快速验证静态语法、调试最小复现和批量检查 `.ets` 示例。

## 适用范围

- 适合：自包含 ArkTS-Sta 片段、语言特性验证、预期编译失败用例、批量小样例检查。
- 不适合：完整 OpenHarmony 工程构建、HAP 打包、SysCap/权限/资源配置验证、设备运行时行为验证。
- 注意：代码会发送到远端接口，不要提交敏感、未公开或客户代码。

## 快速使用

```bash
pip install -r scripts/requirements.txt

python3 scripts/run_playground.py assets/test_simple.ets
python3 scripts/run_playground.py --code "let x: number = 42; console.log(x);"
python3 scripts/run_playground.py --json --code "console.log('Hello');"
```

## 批量检查

```bash
mkdir -p results
for file in test/*.ets; do
    python3 scripts/run_playground.py --json "$file" > "results/$(basename "$file" .ets).json"
done
```

## 输出说明

`--json` 输出字段：

- `success`：远端编译退出码为 `0`。
- `has_error`：远端编译退出码非 `0`。
- `output`：远端返回的编译输出或运行输出。
- `error`：请求失败或编译失败时的错误文本。

对于负向语法用例，需要检查 `output` 是否命中预期规则，不能只看 `has_error: true`。

## 远端接口

```text
https://arkts-play.cn.bz-openlab.ru:10443/compile
```
