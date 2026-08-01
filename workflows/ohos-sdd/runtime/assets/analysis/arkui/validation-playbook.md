# ArkUI Validation Playbook

## SpecTest / Host Preview 适用性

适合 Host Preview / Inspector 断言的场景：

- 布局属性、尺寸、位置、对齐、flex
- 通过 `operationSequence` 触发后可观测到的节点状态变化
- 能反映为节点树、节点属性或布局结果的组件行为

不适合或需补充验证的场景：

- 真实设备硬件、系统服务、功耗、时序
- 需要人工视觉判断或像素级比对
- 当前 Host Preview 无法复现的跨平台或多设备差异

不适用时，必须在 `spec.md`、ArkUI Spec for Validation 的 `spec-for-validation.md`、`test-spec.md` 或 gate 证据中写清 N/A 理由和替代验证方式。

## 常用命令

```bash
cd examples/SpecTest
./tools/host_preview/run_feature.sh
./tools/host_preview/run_feature.sh --suite-id <suite-id>
./tools/host_preview/run_feature.sh --case-id <case-id>
./tools/host_preview/run_feature.sh --archive-screenshot
```

## 编译与测试入口

编译根目录必须是 OpenHarmony 代码根目录，而不是 `foundation/arkui/ace_engine` 子目录。

```bash
./build.sh --product-name rk3568 -j8 --build-target ace_engine --ccache --fast-rebuild
./build.sh --product-name rk3568 --build-target //foundation/arkui/ace_engine/test/unittest:unittest --ccache
```

更细的编译目标、测试路径和模块级命令由对应子 profile 定义。

## 在哪些阶段读取

- Design：需要决定验证路径、性能或渲染证据时
- Plan：需要拆 Task 级验证命令时
- Review：需要核对 SpecTest 适用性和最终验证分流时
