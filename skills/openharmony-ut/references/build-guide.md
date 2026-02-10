# 编译指南

## 标准构建命令

```bash
cd ${OH_ROOT}/ && ${BUILD_CMD} <TARGET_NAME>
```

## 快速重建

首次编译后，如果仅修改代码但未修改 GN 文件，使用 `--fast-rebuild` 显著提升编译效率：

```bash
cd ${OH_ROOT}/ && ./build.sh --product-name=rk3568 --build-target <TARGET_NAME> --fast-rebuild
```

**注意**: 首次编译或修改了 BUILD.gn 文件时不能使用 `--fast-rebuild`。

## 编译产物

测试用例编译产物位于：
```
${OH_OUTPUT}/
```

## 编译失败处理

1. 检查 GN 语法是否正确
2. 检查依赖配置是否完整
3. 查看完整编译日志定位错误
4. 修复后使用 `--fast-rebuild` 快速重编译
