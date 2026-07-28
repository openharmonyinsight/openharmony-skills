# Graphic 子系统通用配置

> **子系统信息**
> - 名称: Graphic (图形图像)
> - Kit包: @kit.ArkGraphics2D
> - 测试路径: test/xts/acts/graphic/acts_graphicXTSDrawing*
> - 语法模式: ArkTS-Dyn（动态语法）
> - 版本: 1.0.0
> - 更新日期: 2026-07-01

## 一、子系统通用配置

### 1.1 API Kit 映射

```typescript
// Drawing 模块导入
import { drawing } from '@kit.ArkGraphics2D';
import { common2D } from '@kit.ArkGraphics2D';
```

### 1.2 测试路径规范

历史用例参考: `${OH_ROOT}/test/xts/acts/graphic/acts_graphicXTSDrawing`
API参考文档: `D:\drawing_docs_file\arkgraphics2d_md\`
API声明文件: `${OH_ROOT}/interface/sdk-js/api/@ohos.graphics.drawing.d.ts`
开发指南: `${OH_ROOT}/docs/zh-cn/application-dev/reference/apis-arkgraphics2d/`

### 1.3 权限申请约束

**必须申请的权限**：
- 无需特殊权限

**权限申请时机**：
- 不适用（Drawing模块无需权限申请）

### 1.4 开发阶段定义

| 阶段 | 操作 | 涉及 API |
|------|------|----------|
| 阶段1 | 创建绘图对象 | Brush, Pen, Path, Matrix, Canvas, Typeface, Font, Region |
| 阶段2 | 设置对象属性 | setColor, setAlpha, setStrokeWidth, setShader, setPathEffect 等 |
| 阶段3 | 验证属性值 | getColor, getAlpha, getStrokeWidth, getShader, getPathEffect 等 |
| 阶段4 | 执行绘图操作 | drawPath, drawRect, drawCircle, drawText, clipPath 等 |
| 阶段5 | 释放资源 | restore, reset, close 等 |

### 1.5 通用测试设计规则

**Graphic 子系统特有测试设计约束**：
1. **属性设置验证**：所有设置类接口（setColor, setAlpha 等）必须使用对应的获取接口（getColor, getAlpha）验证设置的值是否正确
2. **边界值测试**：颜色值边界（0, 255）、透明度边界（0, 255）、浮点数精度（误差小于 0.01）
3. **对象创建验证**：使用 `expect(obj).assertNotNull()` 验证对象创建成功
4. **异常处理**：所有异常必须使用 try-catch 捕获，并验证错误码（如 401）
5. **浮点数比较**：浮点数比较使用 `Math.abs(actual - expected).assertLess(0.01)` 进行精度校验
6. **单线程模型**：Drawing 模块为单线程模型策略，需要调用方自行管理线程安全和上下文状态的切换
7. **接口参数测试**：字符串（覆盖空字符串和非空字符串）、数组（覆盖空数组和非空数组）、枚举值（覆盖所有枚举值）、boolean（覆盖true和false)、参数有多个类型覆盖所有参数类型
8. **返回值验证**：返回值是boolean类型（请覆盖true和false类型）、返回值是数组类型Array（覆盖返回值为空数组和非空数组）
9. **极值场景**：验证number类型参数的极值Number.MAX_VALUE、Number.MIN_VALUE、-Number.MAX_VALUE
10. **连续调用场景**：连续多次调用验证接口功能
11. **联合调用场景**：如果接口有依赖或者关联，完成相关依赖或者关联接口联合调用的测试场景



### 1.6 动静态语法差异（转写指南）

> 基础静态语法规范见 `references/conventions/arkts_standards.md` 和 `modules/L2_Generation/generator/arkts_static_constraints.md`，以下为 Graphic 子系统特有的动静态差异。

#### 1.6.1 类型映射差异
| 动态语法 | 静态语法 | 说明 |
|----------|----------|------|
| `number` | `int` 或 `double` | 根据实际语义选择，颜色值为 int，坐标为 double |
| `common2D.Color` | `common2D.Color` | 颜色对象类型保持一致 |

#### 1.6.2 场景差异
| 场景 | 动态语法 | 静态语法 | 说明 |
|------|----------|----------|------|
| ERROR_401 测试 | 生成 | 不生成 | 静态语法编译时已检查类型 |
| null/undefined 参数测试 | 生成 | 不生成 | 静态语法编译时已检查 |

#### 1.6.3 Graphic 子系统特有差异
- 颜色值使用 `common2D.Color` 对象，包含 `alpha`, `red`, `green`, `blue` 四个属性
- 浮点数参数需考虑精度问题，比较时使用误差范围（小于 0.01）
- 矩阵变换操作需注意变换顺序的影响（前乘 pre 和后乘 post 的区别）
- 使用屏幕物理像素单位 px

## 二、模块文件索引

### 开发阶段与模块映射

| .d.ts 中的声明 | 知识库文件 | API 参考文档 | 说明 | 开发阶段 |
|----------------|------------|--------------|------|----------|
| class Brush | [Drawing.md](./Drawing.md) | arkts-apis-graphics-drawing-Brush.md | 画刷对象 | 阶段1 |
| class Pen | [Drawing.md](./Drawing.md) | arkts-apis-graphics-drawing-Pen.md | 画笔对象 | 阶段1 |
| class Path | [Drawing.md](./Drawing.md) | arkts-apis-graphics-drawing-Path.md | 路径对象 | 阶段1 |
| class Canvas | [Drawing.md](./Drawing.md) | arkts-apis-graphics-drawing-Canvas.md | 画布对象 | 阶段1 |
| class Matrix | [Drawing.md](./Drawing.md) | arkts-apis-graphics-drawing-Matrix.md | 矩阵对象 | 阶段1 |
| class Typeface | [Drawing.md](./Drawing.md) | arkts-apis-graphics-drawing-Typeface.md | 字体对象 | 阶段1 |
| class Font | [Drawing.md](./Drawing.md) | arkts-apis-graphics-drawing-Font.md | 字体设置 | 阶段1 |
| class Region | [Drawing.md](./Drawing.md) | arkts-apis-graphics-drawing-Region.md | 区域对象 | 阶段1 |
| class ShaderEffect | [Drawing.md](./Drawing.md) | arkts-apis-graphics-drawing-ShaderEffect.md | 着色器效果 | 阶段1 |
| class ColorFilter | [Drawing.md](./Drawing.md) | arkts-apis-graphics-drawing-ColorFilter.md | 颜色过滤器 | 阶段1 |
| class MaskFilter | [Drawing.md](./Drawing.md) | arkts-apis-graphics-drawing-MaskFilter.md | 遮罩过滤器 | 阶段1 |
| class PathEffect | [Drawing.md](./Drawing.md) | arkts-apis-graphics-drawing-PathEffect.md | 路径效果 | 阶段1 |
| class ImageFilter | [Drawing.md](./Drawing.md) | arkts-apis-graphics-drawing-ImageFilter.md | 图像过滤器 | 阶段1 |
| class TextBlob | [Drawing.md](./Drawing.md) | arkts-apis-graphics-drawing-TextBlob.md | 文本块 | 阶段1 |
| class RoundRect | [Drawing.md](./Drawing.md) | arkts-apis-graphics-drawing-RoundRect.md | 圆角矩形 | 阶段1 |
| class SamplingOptions | [Drawing.md](./Drawing.md) | arkts-apis-graphics-drawing-SamplingOptions.md | 采样选项 | 阶段1 |
| class ShadowLayer | [Drawing.md](./Drawing.md) | arkts-apis-graphics-drawing-ShadowLayer.md | 阴影层 | 阶段1 |
| class Lattice | [Drawing.md](./Drawing.md) | arkts-apis-graphics-drawing-Lattice.md | 格子对象 | 阶段1 |
| class PathIterator | [Drawing.md](./Drawing.md) | arkts-apis-graphics-drawing-PathIterator.md | 路径迭代器 | 阶段1 |
| class Tool | [Drawing.md](./Drawing.md) | arkts-apis-graphics-drawing-Tool.md | 工具类 | 阶段1 |
| class PointUtils | [Drawing.md](./Drawing.md) | arkts-apis-graphics-drawing-PointUtils.md | 点工具类 | 阶段1 |
| class RectUtils | [Drawing.md](./Drawing.md) | arkts-apis-graphics-drawing-RectUtils.md | 矩形工具类 | 阶段1 |
| class TypefaceArguments | [Drawing.md](./Drawing.md) | arkts-apis-graphics-drawing-TypefaceArguments.md | 字体参数 | 阶段1 |

### API 快速查找

| API 名称 | .d.ts 声明 | 知识库文件 |
|----------|------------|------------|
| setColor / getColor | class Brush / class Pen | [Drawing.md](./Drawing.md) |
| setAlpha / getAlpha | class Brush / class Pen | [Drawing.md](./Drawing.md) |
| setStrokeWidth / getStrokeWidth | class Pen | [Drawing.md](./Drawing.md) |
| setShader / getShader | class Brush / class Pen | [Drawing.md](./Drawing.md) |
| moveTo / lineTo / quadTo / cubicTo | class Path | [Drawing.md](./Drawing.md) |
| addRect / addCircle / addOval / addArc | class Path | [Drawing.md](./Drawing.md) |
| drawPath / drawRect / drawCircle / drawText | class Canvas | [Drawing.md](./Drawing.md) |
| setScale / setRotate / setTranslate | class Matrix | [Drawing.md](./Drawing.md) |