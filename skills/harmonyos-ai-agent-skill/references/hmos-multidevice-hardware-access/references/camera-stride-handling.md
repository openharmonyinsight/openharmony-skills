# 预览流 stride 处理指南（官方基线）

## 目标

通过 ImageReceiver 获取预览帧数据做二次处理时，正确处理 stride 内存对齐，避免花屏。

来源：[华为开发者文档 - 相机预览花屏解决方案](https://developer.huawei.com/consumer/cn/doc/best-practices/bpta-deal-stride-solution)

## 问题背景

开发者在使用相机服务时，如果需要获取每帧图像做二次处理（例如二维码识别或人脸识别），可以通过 `ImageReceiver` 中 `imageArrival` 事件监听预览流每帧数据。在解析图像内容时，如果未考虑 stride，直接使用 `width * height` 读取图像内容去解析，会导致相机预览花屏。

## stride 概念

在计算机图形学和图像处理中，stride 指的是图像的一行数据在内存中实际占用的字节数。出于内存对齐和提高读取效率的考虑，stride 通常大于图像的 width。

**关键说明**：stride 在不同平台底层上报的值不同，开发者需根据实际业务获取 stride 后做处理适配。通过预览流帧数据的返回值 `image.Component.rowStride` 获取 stride。

### 内存布局示意

以一个 width=3, height=3, stride=4 的图像为例：
- 实际分配内存为 `stride × height` = 4 × 3 = 12 字节
- 而非 `width × height` = 3 × 3 = 9 字节

每行末尾有 `stride - width` 个无效填充字节。如果按 width 读取，会将下一行的部分数据错误地当作当前行的像素，导致花屏堆叠。

## 官方 API

- `image.Component.rowStride`：获取实际 stride 值。
- `image.Component.size.width` / `image.Component.size.height`：获取图像尺寸。
- `image.createPixelMap(buffer, options)`：创建 PixelMap。
- `pixelMap.cropSync(region)`：裁剪 PixelMap。

## 典型案例

定义 1080×1080 分辨率的预览流图像，stride 返回 1088。每行多 8 字节无效像素。

## 使用场景

| 场景 | 触发条件 | 推荐用法 | 为什么要判断 | 不判断的风险 |
| --- | --- | --- | --- | --- |
| ImageReceiver 二次处理 | 获取每帧做 QR/人脸识别 | 检查 `rowStride` 是否等于 `width` | stride ≠ width 时有无效填充字节。 | 花屏堆叠。 |
| 跨平台适配 | 不同设备/平台 | 运行时获取 stride，不硬编码 | stride 因平台而异。 | 某些平台花屏，某些平台正常。 |
| PixelMap 创建 | 从帧数据创建图像 | 先处理 stride 再创建 | 创建尺寸与实际数据不匹配会异常。 | 创建失败或图像错位。 |

## 两种修复方案

### 方案一：拷贝有效像素到新 buffer

```typescript
if (stride !== width) {
  let srcArr = new Uint8Array(component.byteBuffer);
  let dstArr = new Uint8Array(width * height);
  for (let row = 0; row < height; row++) {
    let srcOffset = row * stride;
    let dstOffset = row * width;
    for (let col = 0; col < width; col++) {
      dstArr[dstOffset + col] = srcArr[srcOffset + col];
    }
  }
  let pixelMap = image.createPixelMap(dstArr.buffer, {
    size: { width: width, height: height }
  });
}
```

### 方案二：使用 cropSync 裁剪

```typescript
if (stride !== width) {
  let pixelMap = image.createPixelMap(component.byteBuffer, {
    size: { width: stride, height: height }
  });
  pixelMap.cropSync({ x: 0, y: 0, size: { width: width, height: height } });
}
```

### 方案选择建议

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| 方法一（buffer 拷贝） | 精确控制，不依赖额外 API | 需要额外内存分配 | 需要精确像素数据 |
| 方法二（cropSync） | 代码简洁，利用系统 API | 依赖 PixelMap.cropSync 方法 | 快速修复、系统 API 可用时 |

## 约束

- stride 值因平台而异，不可硬编码，必须运行时通过 `component.rowStride` 获取。
- 当 `stride === width` 时可直接使用 `component.byteBuffer` 创建 PixelMap，无需额外处理。

## 验证清单

- stride = width 时：直接创建 PixelMap 正常。
- stride ≠ width 时：方案一和方案二均能正确去除无效像素。
- 不同平台 stride 值记录并验证。
- 花屏现象消除，图像行对齐正确。

## 官方来源

- [相机预览花屏解决方案（官方）](https://developer.huawei.com/consumer/cn/doc/best-practices/bpta-deal-stride-solution)
