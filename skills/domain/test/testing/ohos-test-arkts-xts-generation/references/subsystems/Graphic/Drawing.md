# Drawing 模块测试规则

> **模块信息**
> - 模块名: Drawing
> - .d.ts 声明: @ohos.graphics.drawing
> - API声明文件: @ohos.graphics.drawing.d.ts
> - API参考文档: arkts-apis-graphics-drawing.md 及各子模块文档
> - 依赖模块: 无

> **继承自父级**：语法规范、try-catch 结构、@tc 注释模板、权限约束等通用规则见 [Graphic/_common.md](./_common.md)，以下为 Drawing 模块特有约束。

## 一、API 测试规则

### 1.1 Brush 测试规则

**开发流程阶段**：阶段1（创建对象）、阶段2（设置属性）、阶段3（验证属性）

**测试场景**：
1. 正常场景：创建 Brush 对象，设置颜色、透明度、着色器等属性，使用对应 get 方法验证
2. 错误场景：传入 null、undefined 参数，验证错误码 401
3. 边界场景：颜色值边界（0, 255）、透明度边界（0, 255）

**预期错误码**：
- 401: 参数类型错误（null、undefined、参数缺失）

**前置条件要求**：
- 无需权限申请
- 必须先创建 Brush 对象

**核心 API**：
- constructor(): 创建画刷对象
- constructor(brush: Brush): 复制构造画刷对象
- setColor(color: common2D.Color): 设置颜色
- getColor(): 获取颜色
- setAlpha(alpha: number): 设置透明度
- getAlpha(): 获取透明度
- setShader(shader: ShaderEffect): 设置着色器
- getShader(): 获取着色器
- setColorFilter(colorFilter: ColorFilter): 设置颜色过滤器
- getColorFilter(): 获取颜色过滤器
- setMaskFilter(maskFilter: MaskFilter): 设置遮罩过滤器
- getMaskFilter(): 获取遮罩过滤器
- reset(): 重置画刷

**测试模板**：
```typescript
/**
 * @tc.number SUB_GRAPHIC_DRAWING_BRUSH_SETCOLOR_001
 * @tc.name testBrushSetColor001
 * @tc.desc Test setColor and getColor interfaces of Brush.
 * @tc.level 0
 */
it('testBrushSetColor001', Level.LEVEL0, async () => {
  const flag = 'testBrushSetColor001';
  try {
    console.info(`${flag} start`);
    const brush = new drawing.Brush();
    const color: common2D.Color = { alpha: 255, red: 100, green: 150, blue: 200 };
    brush.setColor(color);
    const colorGet = brush.getColor();
    console.info(`${flag} colorGet.alpha: ${colorGet.alpha}, colorGet.red: ${colorGet.red}, colorGet.green: ${colorGet.green}, colorGet.blue: ${colorGet.blue}`);
    expect(colorGet.alpha).assertEqual(255);
    expect(colorGet.red).assertEqual(100);
    expect(colorGet.green).assertEqual(150);
    expect(colorGet.blue).assertEqual(200);
    console.info(`${flag} success`);
  } catch (e) {
    console.info(`${flag} errorCode: ${e.code}, errorMessage: ${e.message}`);
    expect().assertFail();
  }
});
```

### 1.2 Pen 测试规则

**开发流程阶段**：阶段1（创建对象）、阶段2（设置属性）、阶段3（验证属性）

**测试场景**：
1. 正常场景：创建 Pen 对象，设置颜色、线宽、线帽、连接样式等属性
2. 错误场景：传入 null、undefined 参数，验证错误码 401
3. 边界场景：线宽边界值（0、负数）、斜接限制边界

**预期错误码**：
- 401: 参数类型错误

**核心 API**：
- constructor(): 创建画笔对象
- constructor(pen: Pen): 复制构造画笔对象
- setColor(color: common2D.Color): 设置颜色
- getColor(): 获取颜色
- setAlpha(alpha: number): 设置透明度
- getAlpha(): 获取透明度
- setStrokeWidth(width: number): 设置线宽
- getStrokeWidth(): 获取线宽
- setStrokeCap(cap: PenStrokeCap): 设置线帽样式
- getStrokeCap(): 获取线帽样式
- setStrokeJoin(join: PenStrokeJoin): 设置连接样式
- getStrokeJoin(): 获取连接样式
- setStrokeMiter(miter: number): 设置斜接限制
- getStrokeMiter(): 获取斜接限制
- setPathEffect(pathEffect: PathEffect): 设置路径效果
- getPathEffect(): 获取路径效果
- setShader(shader: ShaderEffect): 设置着色器
- getShader(): 获取着色器
- setColorFilter(colorFilter: ColorFilter): 设置颜色过滤器
- getColorFilter(): 获取颜色过滤器
- setMaskFilter(maskFilter: MaskFilter): 设置遮罩过滤器
- getMaskFilter(): 获取遮罩过滤器
- reset(): 重置画笔

**测试模板**：
```typescript
/**
 * @tc.number SUB_GRAPHIC_DRAWING_PEN_SETSTROKEWIDTH_001
 * @tc.name testPenSetStrokeWidth001
 * @tc.desc Test setStrokeWidth and getStrokeWidth interfaces of Pen.
 * @tc.level 0
 */
it('testPenSetStrokeWidth001', Level.LEVEL0, async () => {
  const flag = 'testPenSetStrokeWidth001';
  try {
    console.info(`${flag} start`);
    const pen = new drawing.Pen();
    pen.setStrokeWidth(10);
    const width = pen.getStrokeWidth();
    console.info(`${flag} width: ${width}`);
    expect(width).assertEqual(10);
    console.info(`${flag} success`);
  } catch (e) {
    console.info(`${flag} errorCode: ${e.code}, errorMessage: ${e.message}`);
    expect().assertFail();
  }
});
```

### 1.3 Path 测试规则

**开发流程阶段**：阶段1（创建对象）、阶段2（构建路径）、阶段4（执行操作）

**测试场景**：
1. 正常场景：创建路径，添加各种图形（矩形、圆形、椭圆、弧线等）
2. 错误场景：传入非法参数，验证错误码
3. 边界场景：超大坐标值、零长度路径

**预期错误码**：
- 401: 参数类型错误

**核心 API**：
- constructor(): 创建路径对象
- constructor(path: Path): 复制构造路径对象
- moveTo(x: number, y: number): 移动到指定点
- lineTo(x: number, y: number): 绘制直线到指定点
- quadTo(ctrlX: number, ctrlY: number, endX: number, endY: number): 绘制二阶贝塞尔曲线
- cubicTo(ctrlX1: number, ctrlY1: number, ctrlX2: number, ctrlY2: number, endX: number, endY: number): 绘制三阶贝塞尔曲线
- addRect(rect: common2D.Rect): 添加矩形
- addCircle(x: number, y: number, radius: number): 添加圆形
- addOval(rect: common2D.Rect): 添加椭圆
- addArc(rect: common2D.Rect, startAngle: number, sweepAngle: number): 添加弧线
- close(): 闭合路径
- reset(): 重置路径
- transform(matrix: Matrix): 路径变换
- op(path: Path, op: PathOp): 路径布尔操作

**测试模板**：
```typescript
/**
 * @tc.number SUB_GRAPHIC_DRAWING_PATH_MOVETO_001
 * @tc.name testPathMoveTo001
 * @tc.desc Test moveTo and lineTo interfaces of Path.
 * @tc.level 0
 */
it('testPathMoveTo001', Level.LEVEL0, async () => {
  const flag = 'testPathMoveTo001';
  try {
    console.info(`${flag} start`);
    const path = new drawing.Path();
    path.moveTo(10, 20);
    path.lineTo(100, 200);
    const pathLength = path.getLength(false);
    console.info(`${flag} pathLength: ${pathLength}`);
    expect(pathLength).assertEqual(190);
    console.info(`${flag} success`);
  } catch (e) {
    console.info(`${flag} errorCode: ${e.code}, errorMessage: ${e.message}`);
    expect().assertFail();
  }
});
```

### 1.4 Canvas 测试规则

**开发流程阶段**：阶段1（创建对象）、阶段4（执行操作）、阶段5（释放资源）

**测试场景**：
1. 正常场景：创建画布，执行绘图操作（绘制路径、矩形、圆形、文本等）
2. 错误场景：传入 null、undefined 参数，验证错误码 401
3. 状态场景：save/restore 状态保存恢复

**预期错误码**：
- 401: 参数类型错误

**前置条件要求**：
- 需要先创建 [PixelMap](arkts-apis-image-PixelMap.md) 对象作为画布的绘制目标
- 无需权限申请

**核心 API**：
- constructor(pixelmap: image.PixelMap): 创建画布对象
- drawPath(path: Path, pen?: Pen, brush?: Brush): 绘制路径
- drawRect(rect: common2D.Rect, pen?: Pen, brush?: Brush): 绘制矩形
- drawCircle(x: number, y: number, radius: number, pen?: Pen, brush?: Brush): 绘制圆形
- drawText(text: string, x: number, y: number, font: Font, pen?: Pen, brush?: Brush): 绘制文本
- clipPath(path: Path, op?: CanvasClipOp): 路径裁剪
- clipRect(rect: common2D.Rect, op?: CanvasClipOp): 矩形裁剪
- save(): 保存状态
- restore(): 恢复状态
- translate(dx: number, dy: number): 平移变换
- scale(sx: number, sy: number): 缩放变换
- rotate(degrees: number): 旋转变换
- skew(sx: number, sy: number): 倾斜变换
- concat(matrix: Matrix): 矩阵变换

**测试模板**：
```typescript
/**
 * @tc.number SUB_GRAPHIC_DRAWING_CANVAS_DRAWPATH_001
 * @tc.name testCanvasDrawPath001
 * @tc.desc Test drawPath interface of Canvas.
 * @tc.level 0
 */
it('testCanvasDrawPath001', Level.LEVEL0, async () => {
  const flag = 'testCanvasDrawPath001';
  try {
    console.info(`${flag} start`);
    const pixelMap = await image.createPixelMap(colorBuffer, opts);
    const canvas = new drawing.Canvas(pixelMap);
    expect(canvas !== null && canvas !== undefined).assertTrue();
    console.info(`${flag} canvas created`);
    const path = new drawing.Path();
    path.moveTo(10, 20);
    path.lineTo(100, 200);
    const pen = new drawing.Pen();
    pen.setColor({ alpha: 255, red: 255, green: 0, blue: 0 });
    canvas.attachPen(pen);
    canvas.drawPath(path);
    canvas.detachPen();
    console.info(`${flag} success`);
  } catch (e) {
    console.info(`${flag} errorCode: ${e.code}, errorMessage: ${e.message}`);
    expect().assertFail();
  }
});
```

### 1.5 Matrix 测试规则

**开发流程阶段**：阶段1（创建对象）、阶段2（设置变换）、阶段3（验证矩阵）

**测试场景**：
1. 正常场景：创建矩阵，设置各种变换（平移、缩放、旋转、倾斜）
2. 错误场景：传入非法参数
3. 边界场景：变换矩阵边界值

**预期错误码**：
- 401: 参数类型错误

**核心 API**：
- constructor(): 创建矩阵对象
- constructor(matrix: Matrix): 复制构造矩阵对象
- setScale(sx: number, sy: number, px: number, py: number): 设置缩放变换
- setRotate(degrees: number, px: number, py: number): 设置旋转变换
- setTranslate(dx: number, dy: number): 设置平移变换
- setSkew(sx: number, sy: number, px: number, py: number): 设置倾斜变换
- preScale(sx: number, sy: number, px: number, py: number): 前乘缩放变换
- preRotate(degrees: number, px: number, py: number): 前乘旋转变换
- preTranslate(dx: number, dy: number): 前乘平移变换
- preSkew(sx: number, sy: number, px: number, py: number): 前乘倾斜变换
- postScale(sx: number, sy: number, px: number, py: number): 后乘缩放变换
- postRotate(degrees: number, px: number, py: number): 后乘旋转变换
- postTranslate(dx: number, dy: number): 后乘平移变换
- postSkew(sx: number, sy: number, px: number, py: number): 后乘倾斜变换
- mapPoint(x: number, y: number): 映射点坐标
- mapRect(rect: common2D.Rect): 映射矩形
- reset(): 重置矩阵

**测试模板**：
```typescript
/**
 * @tc.number SUB_GRAPHIC_DRAWING_MATRIX_SETSCALE_001
 * @tc.name testMatrixSetScale001
 * @tc.desc Test setScale interface of Matrix.
 * @tc.level 0
 */
it('testMatrixSetScale001', Level.LEVEL0, async () => {
  const flag = 'testMatrixSetScale001';
  try {
    console.info(`${flag} start`);
    const matrix = new drawing.Matrix();
    matrix.setScale(2, 2, 0, 0);
    const point = matrix.mapPoint(10, 10);
    console.info(`${flag} point.x: ${point.x}, point.y: ${point.y}`);
    expect(point.x).assertEqual(20);
    expect(point.y).assertEqual(20);
    console.info(`${flag} success`);
  } catch (e) {
    console.info(`${flag} errorCode: ${e.code}, errorMessage: ${e.message}`);
    expect().assertFail();
  }
});
```

### 1.6 Font 测试规则

**开发流程阶段**：阶段1（创建对象）、阶段2（设置属性）、阶段3（验证属性）

**测试场景**：
1. 正常场景：创建字体对象，设置字体大小、类型等属性
2. 错误场景：传入非法参数，验证错误码
3. 边界场景：字体大小边界值

**预期错误码**：
- 401: 参数类型错误

**核心 API**：
- constructor(): 创建字体对象
- setSize(size: number): 设置字体大小
- getSize(): 获取字体大小
- setTypeface(typeface: Typeface): 设置字体
- getTypeface(): 获取字体
- setSkewX(skewX: number): 设置x轴倾斜度
- getSkewX(): 获取x轴倾斜度
- enableSubpixel(isSubpixel: boolean): 设置是否使用次像素渲染
- isSubpixel(): 获取是否使用次像素渲染
- enableLinearMetrics(isLinearMetrics: boolean): 设置是否可线性缩放
- isLinearMetrics(): 获取是否可线性缩放
- countText(text: string): 计算文本字形个数
- getTextPath(text: string, originX: number, originY: number): 获取文本路径

**测试模板**：
```typescript
/**
 * @tc.number SUB_GRAPHIC_DRAWING_FONT_SETSIZE_001
 * @tc.name testFontSetSize001
 * @tc.desc Test setSize and getSize interfaces of Font.
 * @tc.level 0
 */
it('testFontSetSize001', Level.LEVEL0, async () => {
  const flag = 'testFontSetSize001';
  try {
    console.info(`${flag} start`);
    const font = new drawing.Font();
    font.setSize(50);
    const size = font.getSize();
    console.info(`${flag} size: ${size}`);
    expect(size).assertEqual(50);
    console.info(`${flag} success`);
  } catch (e) {
    console.info(`${flag} errorCode: ${e.code}, errorMessage: ${e.message}`);
    expect().assertFail();
  }
});
```

### 1.7 Typeface 测试规则

**开发流程阶段**：阶段1（创建对象）

**测试场景**：
1. 正常场景：创建字体类型对象，从文件创建字体
2. 错误场景：传入非法参数、不存在的文件路径，验证错误码
3. 边界场景：文件路径长度边界

**预期错误码**：
- 401: 参数类型错误

**核心 API**：
- getFamilyName(): 获取字体族名
- makeFromFile(filePath: string): 从文件创建字体
- makeFromCurrent(typefaceArguments: TypefaceArguments): 基于当前字体结合字体属性构造新的字体对象

**测试模板**：
```typescript
/**
 * @tc.number SUB_GRAPHIC_DRAWING_TYPEFACE_MAKEFROMFILE_001
 * @tc.name testTypefaceMakeFromFile001
 * @tc.desc Test makeFromFile interface of Typeface.
 * @tc.level 0
 */
it('testTypefaceMakeFromFile001', Level.LEVEL0, async () => {
  const flag = 'testTypefaceMakeFromFile001';
  try {
    console.info(`${flag} start`);
    const typeface = drawing.Typeface.makeFromFile('/system/fonts/HarmonyOS_Sans_SC.ttf');
    expect(typeface !== null && typeface !== undefined).assertTrue();
    console.info(`${flag} typeface created`);
    const familyName = typeface.getFamilyName();
    console.info(`${flag} familyName: ${familyName}`);
    expect(familyName !== null && familyName !== undefined).assertTrue();
    expect(familyName.length > 0).assertTrue();
    console.info(`${flag} success`);
  } catch (e) {
    console.info(`${flag} errorCode: ${e.code}, errorMessage: ${e.message}`);
    expect().assertFail();
  }
});
```

### 1.8 Region 测试规则

**开发流程阶段**：阶段1（创建对象）、阶段2（设置区域）

**测试场景**：
1. 正常场景：创建区域对象，设置矩形区域、执行区域操作
2. 错误场景：传入非法参数，验证错误码
3. 边界场景：区域边界值、超大区域

**预期错误码**：
- 401: 参数类型错误

**核心 API**：
- constructor(): 创建区域对象
- constructor(region: Region): 复制构造区域对象
- setRect(left: number, top: number, right: number, bottom: number): 设置矩形区域
- setPath(path: Path, clip: Region): 设置路径区域
- op(region: Region, op: RegionOp): 区域布尔操作
- isEmpty(): 判断区域是否为空
- isRect(): 判断区域是否为矩形
- getBounds(): 获取区域边界

**测试模板**：
```typescript
/**
 * @tc.number SUB_GRAPHIC_DRAWING_REGION_SETRECT_001
 * @tc.name testRegionSetRect001
 * @tc.desc Test setRect interface of Region.
 * @tc.level 0
 */
it('testRegionSetRect001', Level.LEVEL0, async () => {
  const flag = 'testRegionSetRect001';
  try {
    console.info(`${flag} start`);
    const region = new drawing.Region();
    region.setRect(100, 100, 500, 500);
    const bounds = region.getBounds();
    console.info(`${flag} bounds.left: ${bounds.left}, bounds.top: ${bounds.top}, bounds.right: ${bounds.right}, bounds.bottom: ${bounds.bottom}`);
    expect(bounds.left).assertEqual(100);
    expect(bounds.top).assertEqual(100);
    expect(bounds.right).assertEqual(500);
    expect(bounds.bottom).assertEqual(500);
    console.info(`${flag} success`);
  } catch (e) {
    console.info(`${flag} errorCode: ${e.code}, errorMessage: ${e.message}`);
    expect().assertFail();
  }
});
```

### 1.9 ShaderEffect 测试规则

**开发流程阶段**：阶段1（创建对象）

**测试场景**：
1. 正常场景：创建各种着色器（颜色着色器、图片着色器、混合着色器）
2. 错误场景：传入非法参数，验证错误码 401 和 25900001
3. 边界场景：着色器参数边界值

**预期错误码**：
- 401: 参数类型错误
- 25900001: 参数范围错误

**核心 API**：
- createColorShader(color: number): 创建颜色着色器
- createImageShader(pixelmap: image.PixelMap, tileX: TileMode, tileY: TileMode, samplingOptions: SamplingOptions, matrix?: Matrix): 创建图片着色器
- createComposeShader(dstShaderEffect: ShaderEffect, srcShaderEffect: ShaderEffect, blendMode: BlendMode): 创建混合着色器
- createLinearGradient(startPoint: common2D.Point, endPoint: common2D.Point, colors: Array<number>, positions: Array<number>, tileMode: TileMode): 创建线性渐变着色器
- createRadialGradient(centerPoint: common2D.Point, radius: number, colors: Array<number>, positions: Array<number>, tileMode: TileMode): 创建径向渐变着色器

**测试模板**：
```typescript
/**
 * @tc.number SUB_GRAPHIC_DRAWING_SHADER_CREATECOLORSHADER_001
 * @tc.name testShaderCreateColorShader001
 * @tc.desc Test createColorShader interface of ShaderEffect.
 * @tc.level 0
 */
it('testShaderCreateColorShader001', Level.LEVEL0, async () => {
  const flag = 'testShaderCreateColorShader001';
  try {
    console.info(`${flag} start`);
    const shader = drawing.ShaderEffect.createColorShader(0xFFFF0000);
    const shader2 = drawing.ShaderEffect.createColorShader(0xFF0000FF);
    expect(shader !== null && shader !== undefined).assertTrue();
    expect(shader2 !== null && shader2 !== undefined).assertTrue();
    console.info(`${flag} shader and shader2 created`);
    let shaderMixture = drawing.ShaderEffect.createComposeShader(shader, shader2, drawing.BlendMode.SRC);
    expect(shaderMixture !== null && shaderMixture !== undefined).assertTrue();
    console.info(`${flag} shaderMixture created`);
    console.info(`${flag} success`);
  } catch (e) {
    console.info(`${flag} errorCode: ${e.code}, errorMessage: ${e.message}`);
    expect().assertFail();
  }
});
```

### 1.10 ColorFilter 测试规则

**开发流程阶段**：阶段1（创建对象）

**测试场景**：
1. 正常场景：创建颜色滤波器（混合模式滤波器、矩阵滤波器）
2. 错误场景：传入非法参数，验证错误码 401
3. 边界场景：颜色值边界、矩阵值边界

**预期错误码**：
- 401: 参数类型错误

**核心 API**：
- createBlendModeColorFilter(color: common2D.Color | number, mode: BlendMode): 创建混合模式颜色滤波器
- createMatrixColorFilter(matrix: Array<number>): 创建矩阵颜色滤波器
- createLumaColorFilter(): 创建亮度颜色滤波器
- createComposeColorFilter(outer: ColorFilter, inner: ColorFilter): 创建组合颜色滤波器

**测试模板**：
```typescript
/**
 * @tc.number SUB_GRAPHIC_DRAWING_COLORFILTER_CREATEBLENDMODE_001
 * @tc.name testColorFilterCreateBlendMode001
 * @tc.desc Test createBlendModeColorFilter interface of ColorFilter.
 * @tc.level 0
 */
it('testColorFilterCreateBlendMode001', Level.LEVEL0, async () => {
  const flag = 'testColorFilterCreateBlendMode001';
  try {
    console.info(`${flag} start`);
    const color : common2D.Color = { alpha: 255, red: 255, green: 0, blue: 0 };
    let colorFilter1 = drawing.ColorFilter.createBlendModeColorFilter(color, drawing.BlendMode.SRC);
    expect(colorFilter1 !== null && colorFilter1 !== undefined).assertTrue();
    console.info(`${flag} colorFilter1 created`);
    let colorFilter2 = drawing.ColorFilter.createBlendModeColorFilter(color, drawing.BlendMode.DST);
    expect(colorFilter2 !== null && colorFilter2 !== undefined).assertTrue();
    console.info(`${flag} colorFilter2 created`);
    let colorFilter = drawing.ColorFilter.createComposeColorFilter(colorFilter1, colorFilter2);
    expect(colorFilter !== null && colorFilter !== undefined).assertTrue();
    console.info(`${flag} colorFilter created`);
    console.info(`${flag} success`);
  } catch (e) {
    console.info(`${flag} errorCode: ${e.code}, errorMessage: ${e.message}`);
    expect().assertFail();
  }
});
```

### 1.11 MaskFilter 测试规则

**开发流程阶段**：阶段1（创建对象）

**测试场景**：
1. 正常场景：创建蒙版滤镜（模糊蒙版滤镜）
2. 错误场景：传入非法参数，验证错误码 401
3. 边界场景：模糊半径边界值

**预期错误码**：
- 401: 参数类型错误

**核心 API**：
- createBlurMaskFilter(blurType: BlurType, sigma: number): 创建模糊蒙版滤镜

**测试模板**：
```typescript
/**
 * @tc.number SUB_GRAPHIC_DRAWING_MASKFILTER_CREATEBLUR_001
 * @tc.name testMaskFilterCreateBlur001
 * @tc.desc Test createBlurMaskFilter interface of MaskFilter.
 * @tc.level 0
 */
it('testMaskFilterCreateBlur001', Level.LEVEL0, async () => {
  const flag = 'testMaskFilterCreateBlur001';
  console.info(`${flag} start`);
  const brush = new drawing.Brush();
  try {
    const maskFilter = drawing.MaskFilter.createBlurMaskFilter(drawing.BlurType.OUTER, 10);
    expect(maskFilter !== null && maskFilter !== undefined).assertTrue();
    console.info(`${flag} maskFilter created`);
    brush.setMaskFilter(maskFilter);
    console.info(`${flag} success`);
  } catch (e) {
    console.info(`${flag} errorCode: ${e.code}, errorMessage: ${e.message}`);
    expect().assertFail();
  }
});
```

### 1.12 PathEffect 测试规则

**开发流程阶段**：阶段1（创建对象）

**测试场景**：
1. 正常场景：创建路径效果（虚线效果、路径虚线效果）
2. 错误场景：传入非法参数，验证错误码 401
3. 边界场景：虚线参数边界值

**预期错误码**：
- 401: 参数类型错误

**核心 API**：
- createDashPathEffect(intervals: Array<number>, phase: number): 创建虚线效果
- createPathDashEffect(path: Path, advance: number, phase: number, style: PathDashStyle): 创建路径虚线效果
- createCornerPathEffect(radius: number): 创建圆角路径效果
- createComposePathEffect(outer: PathEffect, inner: PathEffect): 创建组合路径效果
- createSumPathEffect(first: PathEffect, second: PathEffect): 创建叠加路径效果

**测试模板**：
```typescript
/**
 * @tc.number SUB_GRAPHIC_DRAWING_PATHEFFECT_CREATEDASH_001
 * @tc.name testPathEffectCreateDash001
 * @tc.desc Test createDashPathEffect interface of PathEffect.
 * @tc.level 0
 */
it('testPathEffectCreateDash001', Level.LEVEL0, async () => {
  const flag = 'testPathEffectCreateDash001';
  console.info(`${flag} start`);
  const pen = new drawing.Pen();
  try {
    const intervals = [10, 5];
    const effect = drawing.PathEffect.createDashPathEffect(intervals, 5);
    expect(effect !== null && effect !== undefined).assertTrue();
    console.info(`${flag} effect created`);
    pen.setPathEffect(effect);
    console.info(`${flag} success`);
  } catch (e) {
    console.info(`${flag} errorCode: ${e.code}, errorMessage: ${e.message}`);
    expect().assertFail();
  }
});
```

### 1.13 ImageFilter 测试规则

**开发流程阶段**：阶段1（创建对象）

**测试场景**：
1. 正常场景：创建图像滤波器（模糊滤波器、图片滤波器）
2. 错误场景：传入非法参数，验证错误码 401
3. 边界场景：模糊参数边界值

**预期错误码**：
- 401: 参数类型错误

**核心 API**：
- createBlurImageFilter(sigmaX: number, sigmaY: number, tileMode: TileMode, imageFilter?: ImageFilter): 创建模糊图像滤波器
- createFromImage(pixelmap: image.PixelMap, srcRect?: common2D.Rect, dstRect?: common2D.Rect): 创建图片滤波器
- createColorFilterImageFilter(colorFilter: ColorFilter, imageFilter?: ImageFilter): 创建颜色滤波器图像滤波器
- createComposeImageFilter(outer: ImageFilter, inner: ImageFilter): 创建组合图像滤波器

**测试模板**：
```typescript
/**
 * @tc.number SUB_GRAPHIC_DRAWING_IMAGEFILTER_CREATEBLUR_001
 * @tc.name testImageFilterCreateBlur001
 * @tc.desc Test createBlurImageFilter interface of ImageFilter.
 * @tc.level 0
 */
it('testImageFilterCreateBlur001', Level.LEVEL0, async () => {
  const flag = 'testImageFilterCreateBlur001';
  console.info(`${flag} start`);
  let brush = new drawing.Brush();
  let pen = new drawing.Pen();
  try {
    const imgFilter = drawing.ImageFilter.createBlurImageFilter(5, 10, drawing.TileMode.CLAMP);
    expect(imgFilter !== null && imgFilter !== undefined).assertTrue();
    console.info(`${flag} imgFilter created`);
    pen.setImageFilter(imgFilter);
    console.info(`${flag} pen.setImageFilter success`);
    pen.setImageFilter(null);
    brush.setImageFilter(imgFilter);
    console.info(`${flag} brush.setImageFilter success`);
    brush.setImageFilter(null);
    console.info(`${flag} success`);
  } catch (e) {
    console.info(`${flag} errorCode: ${e.code}, errorMessage: ${e.message}`);
    expect().assertFail();
  }
});
```

### 1.14 TextBlob 测试规则

**开发流程阶段**：阶段1（创建对象）

**测试场景**：
1. 正常场景：创建文本块对象
2. 错误场景：传入非法参数，验证错误码 401
3. 边界场景：文本长度边界

**预期错误码**：
- 401: 参数类型错误

**核心 API**：
- makeFromString(text: string, font: Font, encoding: TextEncoding): 从字符串创建文本块
- makeFromPosText(text: string, len: number, points: common2D.Point[], font: Font): 从位置文本创建文本块
- uniqueID(): 获取唯一标识符

**测试模板**：
```typescript
/**
 * @tc.number SUB_GRAPHIC_DRAWING_TEXTBLOB_MAKEFROMSTRING_001
 * @tc.name testTextBlobMakeFromString001
 * @tc.desc Test makeFromString interface of TextBlob.
 * @tc.level 0
 */
it('testTextBlobMakeFromString001', Level.LEVEL0, async () => {
  const flag = 'testTextBlobMakeFromString001';
  try {
    console.info(`${flag} start`);
    const font = new drawing.Font();
    font.setSize(50);
    const textBlob = drawing.TextBlob.makeFromString('Hello', font, drawing.TextEncoding.TEXT_ENCODING_UTF8);
    expect(textBlob !== null && textBlob !== undefined).assertTrue();
    console.info(`${flag} textBlob created`);
    const id = textBlob.uniqueID();
    console.info(`${flag} uniqueID: ${id}`);
    expect(id).assertLarger(0);
    console.info(`${flag} success`);
  } catch (e) {
    console.info(`${flag} errorCode: ${e.code}, errorMessage: ${e.message}`);
    expect().assertFail();
  }
});
```

### 1.15 RoundRect 测试规则

**开发流程阶段**：阶段1（创建对象）、阶段2（设置属性）

**测试场景**：
1. 正常场景：创建圆角矩形对象，设置圆角属性
2. 错误场景：传入非法参数，验证错误码 401
3. 边界场景：圆角半径边界值

**预期错误码**：
- 401: 参数类型错误

**核心 API**：
- constructor(rect: common2D.Rect, xRadii: number, yRadii: number): 创建圆角矩形
- constructor(roundRect: RoundRect): 复制构造圆角矩形
- setCorner(pos: CornerPos, x: number, y: number): 设置指定位置的圆角
- getCornerRadii(pos: CornerPos): 获取指定位置的圆角半径
- setRect(rect: common2D.Rect): 设置矩形区域
- getRect(): 获取矩形区域
- getWidth(): 获取宽度
- getHeight(): 获取高度

**测试模板**：
```typescript
/**
 * @tc.number SUB_GRAPHIC_DRAWING_ROUNDRECT_SETCORNER_001
 * @tc.name testRoundRectSetCorner001
 * @tc.desc Test setCorner interface of RoundRect.
 * @tc.level 0
 */
it('testRoundRectSetCorner001', Level.LEVEL0, async () => {
  const flag = 'testRoundRectSetCorner001';
  try {
    console.info(`${flag} start`);
    const rect: common2D.Rect = { left: 100, top: 100, right: 500, bottom: 300 };
    const roundRect = new drawing.RoundRect(rect, 50, 50);
    roundRect.setCorner(drawing.CornerPos.TOP_LEFT_CORNER, 30, 30);
    const radii = roundRect.getCornerRadii(drawing.CornerPos.TOP_LEFT_CORNER);
    console.info(`${flag} radii.x: ${radii.x}, radii.y: ${radii.y}`);
    expect(radii.x).assertEqual(30);
    expect(radii.y).assertEqual(30);
    console.info(`${flag} success`);
  } catch (e) {
    console.info(`${flag} errorCode: ${e.code}, errorMessage: ${e.message}`);
    expect().assertFail();
  }
});
```

### 1.16 SamplingOptions 测试规则

**开发流程阶段**：阶段1（创建对象）

**测试场景**：
1. 正常场景：创建采样选项对象
2. 错误场景：传入非法参数，验证错误码 401
3. 边界场景：采样参数边界值

**预期错误码**：
- 401: 参数类型错误

**核心 API**：
- constructor(): 创建采样选项对象（默认过滤模式）
- constructor(filterMode: FilterMode): 创建指定过滤模式的采样选项对象
- constructor(filterMode: FilterMode, mipmapMode: MipmapMode): 创建指定过滤模式和.mipmap模式的采样选项对象

**测试模板**：
```typescript
/**
 * @tc.number SUB_GRAPHIC_DRAWING_SAMPLINGOPTIONS_CREATE_001
 * @tc.name testSamplingOptionsCreate001
 * @tc.desc Test constructor interface of SamplingOptions.
 * @tc.level 0
 */
it('testSamplingOptionsCreate001', Level.LEVEL0, async () => {
  const flag = 'testSamplingOptionsCreate001';
  console.info(`${flag} start`);
  let matrix = new drawing.Matrix();
  const pixelMap = await image.createPixelMap(colorBuffer, opts);
  try {
    const samplingOptions = new drawing.SamplingOptions(drawing.FilterMode.FILTER_MODE_NEAREST);
    expect(samplingOptions !== null && samplingOptions !== undefined).assertTrue();
    console.info(`${flag} samplingOptions created`);
    let imageShader = drawing.ShaderEffect.createImageShader(pixelMap, drawing.TileMode.CLAMP, drawing.TileMode.CLAMP, samplingOptions, matrix);
    console.info(`${flag} imageShader created`);
    console.info(`${flag} success`);
  } catch (e) {
    console.info(`${flag} errorCode: ${e.code}, errorMessage: ${e.message}`);
    expect().assertFail();
  }
});
```

### 1.17 ShadowLayer 测试规则

**开发流程阶段**：阶段1（创建对象）

**测试场景**：
1. 正常场景：创建阴影层对象
2. 错误场景：传入非法参数，验证错误码 401
3. 边界场景：阴影半径边界值

**预期错误码**：
- 401: 参数类型错误

**核心 API**：
- create(blurRadius: number, x: number, y: number, color: common2D.Color | number): 创建阴影层对象

**测试模板**：
```typescript
/**
 * @tc.number SUB_GRAPHIC_DRAWING_SHADOWLAYER_CREATE_001
 * @tc.name testShadowLayerCreate001
 * @tc.desc Test create interface of ShadowLayer.
 * @tc.level 0
 */
it('testShadowLayerCreate001', Level.LEVEL0, async () => {
  const flag = 'testShadowLayerCreate001';
  console.info(`${flag} start`);
  let font = new drawing.Font();
  font.setSize(60);
  let textBlob = drawing.TextBlob.makeFromString("hello", font, drawing.TextEncoding.TEXT_ENCODING_UTF8);
  let pen = new drawing.Pen();
  pen.setStrokeWidth(2.0);
  const pixelMap = await image.createPixelMap(colorBuffer, opts);
  const canvas = new drawing.Canvas(pixelMap);
  try {
    const color: common2D.Color = { alpha: 255, red: 0, green: 255, blue: 0 };
    const shadowLayer = drawing.ShadowLayer.create(3, -3, 3, color);
    expect(shadowLayer !== null && shadowLayer !== undefined).assertTrue();
    console.info(`${flag} shadowLayer created`);
    pen.setShadowLayer(shadowLayer);
    canvas.attachPen(pen);
    canvas.drawTextBlob(textBlob, 100, 200);
    canvas.detachPen();
    console.info(`${flag} success`);
  } catch (e) {
    console.info(`${flag} errorCode: ${e.code}, errorMessage: ${e.message}`);
    expect().assertFail();
  }
});
```

### 1.18 PathIterator 测试规则

**开发流程阶段**：阶段1（创建对象）、阶段2（遍历路径）

**测试场景**：
1. 正常场景：创建路径迭代器对象，遍历路径操作
2. 错误场景：传入非法参数，验证错误码 401
3. 边界场景：路径操作边界值

**预期错误码**：
- 401: 参数类型错误

**核心 API**：
- constructor(path: Path): 创建路径迭代器对象
- next(points: Array<common2D.Point>, offset?: number): 获取下一个路径操作

**测试模板**：
```typescript
/**
 * @tc.number SUB_GRAPHIC_DRAWING_PATHITERATOR_NEXT_001
 * @tc.name testPathIteratorNext001
 * @tc.desc Test next interface of PathIterator.
 * @tc.level 0
 */
it('testPathIteratorNext001', Level.LEVEL0, async () => {
  const flag = 'testPathIteratorNext001';
  try {
    console.info(`${flag} start`);
    const path = new drawing.Path();
    path.moveTo(10, 20);
    path.lineTo(100, 200);
    const iter = new drawing.PathIterator(path);
    const points: Array<common2D.Point> = [{ x: 0, y: 0 }, { x: 0, y: 0 }, { x: 0, y: 0 }, { x: 0, y: 0 }];
    const verb = iter.next(points, 0);
    console.info(`${flag} verb: ${verb}`);
    expect(verb).assertEqual(drawing.PathIteratorVerb.MOVE);
    console.info(`${flag} success`);
  } catch (e) {
    console.info(`${flag} errorCode: ${e.code}, errorMessage: ${e.message}`);
    expect().assertFail();
  }
});
```

### 1.19 TypefaceArguments 测试规则

**开发流程阶段**：阶段1（创建对象）、阶段2（设置属性）

**测试场景**：
1. 正常场景：创建字体属性对象，设置字体属性
2. 错误场景：传入非法参数，验证错误码 25900001
3. 边界场景：字体属性值边界

**预期错误码**：
- 25900001: 参数范围错误

**核心 API**：
- constructor(): 创建字体属性对象
- addVariation(axis: string, value: number): 设置字体属性

**测试模板**：
```typescript
/**
 * @tc.number SUB_GRAPHIC_DRAWING_TYPEFACEARGS_ADDVARIATION_001
 * @tc.name testTypefaceArgsAddVariation001
 * @tc.desc Test addVariation interface of TypefaceArguments.
 * @tc.level 0
 */
it('testTypefaceArgsAddVariation001', Level.LEVEL0, async () => {
  const flag = 'testTypefaceArgsAddVariation001';
  try {
    console.info(`${flag} start`);
    const typeFaceArgument = new drawing.TypefaceArguments();
    typeFaceArgument.addVariation('wght', 100);
    expect(typeFaceArgument !== null && typeFaceArgument !== undefined).assertTrue();
    console.info(`${flag} typeFaceArgument created and addVariation success`);
    console.info(`${flag} success`);
  } catch (e) {
    console.info(`${flag} errorCode: ${e.code}, errorMessage: ${e.message}`);
    expect().assertFail();
  }
});
```

### 1.20 Lattice 测试规则

**开发流程阶段**：阶段1（创建对象）

**测试场景**：
1. 正常场景：创建矩形网格对象
2. 错误场景：传入非法参数，验证错误码 401
3. 边界场景：网格参数边界值

**预期错误码**：
- 401: 参数类型错误

**核心 API**：
- createImageLattice(xDivs: Array<number>, yDivs: Array<number>, fXCount: number, fYCount: number, fBounds?: common2D.Rect, fRectTypes?: Array<RectType>, fColors?: Array<common2D.Color> | Array<number>): 创建矩形网格对象

**测试模板**：
```typescript
/**
 * @tc.number SUB_GRAPHIC_DRAWING_LATTICE_CREATE_001
 * @tc.name testLatticeCreate001
 * @tc.desc Test createImageLattice interface of Lattice.
 * @tc.level 0
 */
it('testLatticeCreate001', Level.LEVEL0, async () => {
  const flag = 'testLatticeCreate001';
  try {
    console.info(`${flag} start`);
    const pixelMap = await image.createPixelMap(colorBuffer, opts);
    const canvas = new drawing.Canvas(pixelMap);
    console.info(`${flag} canvas created`);
    const xDivs: Array<number> = [1, 2, 4];
    const yDivs: Array<number> = [1, 2, 4];
    const lattice = drawing.Lattice.createImageLattice(xDivs, yDivs, 3, 3);
    expect(lattice !== null && lattice !== undefined).assertTrue();
    console.info(`${flag} lattice created`);
    let dst: common2D.Rect = { left: 0, top: 0, right: 200, bottom: 200 };
    try {
      canvas.drawImageLattice(pixel, lattice, dst, drawing.FilterMode.FILTER_MODE_NEAREST);
      console.info(`${flag} drawImageLattice success`);
    } catch (e) {
      console.info(`${flag} drawImageLattice errorCode: ${e.code}, errorMessage: ${e.message}`);
      expect().assertFail();
    }
    console.info(`${flag} success`);
  } catch (e) {
    console.info(`${flag} errorCode: ${e.code}, errorMessage: ${e.message}`);
    expect().assertFail();
  }
});
```

### 1.21 Tool 测试规则

**开发流程阶段**：阶段1（调用工具方法）

**测试场景**：
1. 正常场景：调用工具方法转换颜色
2. 错误场景：传入非法参数，验证错误码 401
3. 边界场景：颜色值边界

**预期错误码**：
- 401: 参数类型错误

**核心 API**：
- makeColorFromResourceColor(resourceColor: ResourceColor): 将ResourceColor转换为common2D.Color

**测试模板**：
```typescript
/**
 * @tc.number SUB_GRAPHIC_DRAWING_TOOL_MAKECOLOR_001
 * @tc.name testToolMakeColor001
 * @tc.desc Test makeColorFromResourceColor interface of Tool.
 * @tc.level 0
 */
it('testToolMakeColor001', Level.LEVEL0, async () => {
  const flag = 'testToolMakeColor001';
  try {
    console.info(`${flag} start`);
    const color = drawing.Tool.makeColorFromResourceColor(0xffc0cb);
    expect(color !== null && color !== undefined).assertTrue();
    console.info(`${flag} color.alpha: ${color.alpha}`);
    expect(color.alpha).assertEqual(255);
    console.info(`${flag} success`);
  } catch (e) {
    console.info(`${flag} errorCode: ${e.code}, errorMessage: ${e.message}`);
    expect().assertFail();
  }
});
```

### 1.22 PointUtils 测试规则

**开发流程阶段**：阶段1（调用工具方法）

**测试场景**：
1. 正常场景：调用点工具方法进行点的操作
2. 错误场景：传入非法参数，验证错误码 401
3. 边界场景：点坐标边界值

**预期错误码**：
- 401: 参数类型错误

**核心 API**：
- negate(point: common2D.Point): 对点的坐标取反
- offset(point: common2D.Point, dx: number, dy: number): 将指定坐标点偏移

**测试模板**：
```typescript
/**
 * @tc.number SUB_GRAPHIC_DRAWING_POINTUTILS_OFFSET_001
 * @tc.name testPointUtilsOffset001
 * @tc.desc Test offset interface of PointUtils.
 * @tc.level 0
 */
it('testPointUtilsOffset001', Level.LEVEL0, async () => {
  const flag = 'testPointUtilsOffset001';
  try {
    console.info(`${flag} start`);
    const point: common2D.Point = { x: 10, y: 20 };
    drawing.PointUtils.offset(point, 5, 10);
    console.info(`${flag} point.x: ${point.x}, point.y: ${point.y}`);
    expect(point.x).assertEqual(15);
    expect(point.y).assertEqual(30);
    console.info(`${flag} success`);
  } catch (e) {
    console.info(`${flag} errorCode: ${e.code}, errorMessage: ${e.message}`);
    expect().assertFail();
  }
});
```

### 1.23 RectUtils 测试规则

**开发流程阶段**：阶段1（调用工具方法）

**测试场景**：
1. 正常场景：调用矩形工具方法进行矩形的操作
2. 错误场景：传入非法参数，验证错误码 401
3. 边界场景：矩形参数边界值

**预期错误码**：
- 401: 参数类型错误

**核心 API**：
- makeEmpty(): 创建空矩形
- makeLtrb(left: number, top: number, right: number, bottom: number): 创建指定边界的矩形
- makeCopy(src: common2D.Rect): 拷贝矩形
- getWidth(rect: common2D.Rect): 获取矩形宽度
- getHeight(rect: common2D.Rect): 获取矩形高度
- getCenterX(rect: common2D.Rect): 获取矩形中心点x坐标
- getCenterY(rect: common2D.Rect): 获取矩形中心点y坐标
- intersects(rect1: common2D.Rect, rect2: common2D.Rect): 判断两个矩形是否相交
- intersect(rect1: common2D.Rect, rect2: common2D.Rect): 计算两个矩形的交集

**测试模板**：
```typescript
/**
 * @tc.number SUB_GRAPHIC_DRAWING_RECTUTILS_MAKELTRB_001
 * @tc.name testRectUtilsMakeLtrb001
 * @tc.desc Test makeLtrb interface of RectUtils.
 * @tc.level 0
 */
it('testRectUtilsMakeLtrb001', Level.LEVEL0, async () => {
  const flag = 'testRectUtilsMakeLtrb001';
  try {
    console.info(`${flag} start`);
    const rect = drawing.RectUtils.makeLtrb(10, 10, 20, 20);
    console.info(`${flag} rect.left: ${rect.left}, rect.top: ${rect.top}, rect.right: ${rect.right}, rect.bottom: ${rect.bottom}`);
    expect(rect.left).assertEqual(10);
    expect(rect.top).assertEqual(10);
    expect(rect.right).assertEqual(20);
    expect(rect.bottom).assertEqual(20);
    console.info(`${flag} success`);
  } catch (e) {
    console.info(`${flag} errorCode: ${e.code}, errorMessage: ${e.message}`);
    expect().assertFail();
  }
});
```

## 二、模块特有约束

### 2.1 颜色值验证规则

所有颜色设置接口（setColor 等）必须使用对应的获取接口（getColor）验证：

- 整数颜色值：直接使用 `assertEqual` 验证
- 颜色对象：分别验证 alpha、red、green、blue 四个分量

```typescript
const color: common2D.Color = {
  alpha: 255,
  red: 100,
  green: 150,
  blue: 200
};
brush.setColor(color);
const colorGet = brush.getColor();
expect(colorGet.alpha).assertEqual(255);
expect(colorGet.red).assertEqual(100);
expect(colorGet.green).assertEqual(150);
expect(colorGet.blue).assertEqual(200);
```

### 2.2 属性设置验证规则

每个 set 方法必须有对应的 get 方法验证：

```typescript
pen.setStrokeWidth(10);
const width = pen.getStrokeWidth();
expect(width).assertEqual(10);
```

### 2.3 浮点数精度验证规则

浮点数参数验证需根据期望值格式选择验证方式:

**验证规则**：
- 当浮点数有小数点，并且小数点后大于等于5位数时，使用误差范围校验：`Math.abs(actual - expected).assertLess(0.01)`
- 其他情况（无小数点或小数点后少于5位数），直接使用 `assertEqual` 校验

**示例代码**：

```typescript
// 小数点后大于等于5位，使用精度校验
const flag = 'getLength_test';
let pathLength = path.getLength(false);
console.info(`${flag} success, pathLength: ${pathLength}`);
expect(Math.abs(pathLength - 195.50589723)).assertLess(0.01);

// 小数点后少于5位或无小数点，直接比较
pen.setStrokeWidth(10.5);
const width = pen.getStrokeWidth();
expect(width).assertEqual(10.5);

// 无小数点，直接比较
pen.setStrokeWidth(10);
const width = pen.getStrokeWidth();
expect(width).assertEqual(10);
```

### 2.4 错误码验证规则

参数错误统一验证错误码 401：

```typescript
const flag = 'setColor_error_test';
try {
  brush.setColor(null);
  console.info(`${flag} success`);
  expect().assertFail();
} catch (e) {
  console.info(`${flag} errorCode: ${e.code}, errorMessage: ${e.message}`);
  expect(e.code).assertEqual(401);
}
```

接口有其他非401错误码的，需要验证 例如：25900001：

```typescript
const flag = 'addVariation_error_test';
try {
  typeFaceArgument.addVariation('wghta', 100);
  console.info(`${flag} success`);
  expect().assertFail();
} catch (e) {
  console.info(`${flag} errorCode: ${e.code}, errorMessage: ${e.message}`);
  expect(e.code).assertEqual(25900001);
}
```

### 2.5 测试用例命名规范

文件命名：`Drawing[API].test.ets`

- 示例：DrawingBrushSetColor.test.ets、DrawingPenSetStrokeWidth.test.ets

用例编号：`SUB_GRAPHIC_DRAWING_[API]_[TYPE]_[序号]`

- TYPE 类型：CREATE（创建）、OPERATION（操作）、ATTRIBUTE（属性）、ERROR（错误码）、BOUNDARY（边界值）
- 示例：SUB_GRAPHIC_DRAWING_BRUSH_SETCOLOR_001

### 2.6 测试级别要求

每个 API 至少需要：

- LEVEL0: 基本功能测试（至少 1 个）
- LEVEL1: 常用场景测试（至少 1 个）
- LEVEL2 或更高: 异常或边界测试（至少 1 个）

### 2.7 线程安全约束

Drawing 模块为单线程模型策略，测试时需注意：

- 避免多线程并发调用 Drawing API
- 需要调用方自行管理线程安全和上下文状态的切换

### 2.8 单位约束

Drawing 模块使用屏幕物理像素单位 px，测试时需注意：

- 所有坐标、长度参数单位均为 px
- 不需要进行单位转换

## 三、模块特殊注意事项

### 3.1 验证返回值有效性

**强制要求**:
返回值是drawing特有的类时，需对该类对象做非空以外的有效性校验，有以下四种方式可以验证：

#### 方式一：调用对象自身的接口验证（优先使用）

**适用场景**：该对象有可以调用的接口（如get方法），可以直接使用该对象调用相关接口，验证其有效性。

**示例1：getTextPathWithFallback 返回 Path 对象**
API接口定义：`getTextPathWithFallback(text: string, byteLength: number, x: number, y: number): Path`

返回值是Path对象，直接调用Path对象的接口getLength()和接口getLastPoint()，对返回值做具体值断言校验。
```typescript
const flag = 'getTextPathWithFallback_test';
try {
  let path = font.getTextPathWithFallback(myString, length, 0, 100);
  if (path == undefined) {
    console.info(`${flag} path is undefined`);
    expect().assertFail();
  } else {
    expect(path !== null && path !== undefined).assertTrue();
    let pathLength = path.getLength(false);
    console.info(`${flag} getLength success, pathLength: ${pathLength}`);
    expect(Math.abs(pathLength - 195.50) < 0.01).assertTrue();
    let lastPoint = path.getLastPoint();
    expect(lastPoint !== null && lastPoint !== undefined).assertTrue();
    if (lastPoint) {
      console.info(`${flag} getLastPoint success, lastPoint.x: ${lastPoint.x}, lastPoint.y: ${lastPoint.y}`);
      expect(Math.abs(lastPoint.x - 94.84) < 0.01).assertTrue();
      expect(Math.abs(lastPoint.y - 86.99) < 0.01).assertTrue();
    }
  }
} catch (e) {
  console.info(`${flag} errorCode: ${e.code}, errorMessage: ${e.message}`);
  expect().assertFail();
}
```

**示例2：Brush 对象验证**
```typescript
const flag = 'Brush_test';
try {
  const brush = new drawing.Brush();
  const color: common2D.Color = { alpha: 255, red: 100, green: 150, blue: 200 };
  brush.setColor(color);
  const colorGet = brush.getColor();
  console.info(`${flag} colorGet.alpha: ${colorGet.alpha}, colorGet.red: ${colorGet.red}, colorGet.green: ${colorGet.green}, colorGet.blue: ${colorGet.blue}`);
  expect(colorGet.alpha).assertEqual(255);
  expect(colorGet.red).assertEqual(100);
  expect(colorGet.green).assertEqual(150);
  expect(colorGet.blue).assertEqual(200);
  console.info(`${flag} success`);
} catch (e) {
  console.info(`${flag} errorCode: ${e.code}, errorMessage: ${e.message}`);
  expect().assertFail();
}
```

#### 方式二：作为其他接口的入参验证（常用）

**适用场景**：该对象是其他类对象接口的入参，可以调用相关接口，把该对象作为入参，验证有效性。

**示例1：createBlurMaskFilter 返回 MaskFilter 对象**
API接口定义：`static createBlurMaskFilter(blurType: BlurType, sigma: number): MaskFilter`

返回值是MaskFilter对象，调用brush.setMaskFilter()接口，MaskFilter对象作为入参验证有效性。
```typescript
const flag = 'createBlurMaskFilter_test';
const brush = new drawing.Brush();
try {
  const maskFilter = drawing.MaskFilter.createBlurMaskFilter(drawing.BlurType.OUTER, 10);
  expect(maskFilter !== null && maskFilter !== undefined).assertTrue();
  console.info(`${flag} maskFilter created`);
  brush.setMaskFilter(maskFilter);
  console.info(`${flag} brush.setMaskFilter success`);
  console.info(`${flag} success`);
} catch (e) {
  console.info(`${flag} errorCode: ${e.code}, errorMessage: ${e.message}`);
  expect().assertFail();
}
```

**示例2：ShadowLayer.create 返回 ShadowLayer 对象**
```typescript
const flag = 'ShadowLayer_test';
let font = new drawing.Font();
font.setSize(60);
let textBlob = drawing.TextBlob.makeFromString("hello", font, drawing.TextEncoding.TEXT_ENCODING_UTF8);
let pen = new drawing.Pen();
pen.setStrokeWidth(2.0);
const pixelMap = await image.createPixelMap(colorBuffer, opts);
const canvas = new drawing.Canvas(pixelMap);
try {
  const color: common2D.Color = { alpha: 255, red: 0, green: 255, blue: 0 };
  const shadowLayer = drawing.ShadowLayer.create(3, -3, 3, color);
  expect(shadowLayer !== null && shadowLayer !== undefined).assertTrue();
  console.info(`${flag} shadowLayer created`);
  pen.setShadowLayer(shadowLayer);
  console.info(`${flag} pen.setShadowLayer success`);
  canvas.attachPen(pen);
  canvas.drawTextBlob(textBlob, 100, 200);
  canvas.detachPen();
  console.info(`${flag} success`);
} catch (e) {
  console.info(`${flag} errorCode: ${e.code}, errorMessage: ${e.message}`);
  expect().assertFail();
}
```

**示例3：ShaderEffect.createColorShader 返回 ShaderEffect 对象**
```typescript
const flag = 'createComposeShader_test';
try {
  const shader = drawing.ShaderEffect.createColorShader(0xFFFF0000);
  const shader2 = drawing.ShaderEffect.createColorShader(0xFF0000FF);
  expect(shader !== null && shader !== undefined).assertTrue();
  expect(shader2 !== null && shader2 !== undefined).assertTrue();
  console.info(`${flag} shader and shader2 created`);
  let shaderMixture = drawing.ShaderEffect.createComposeShader(shader, shader2, drawing.BlendMode.SRC);
  expect(shaderMixture !== null && shaderMixture !== undefined).assertTrue();
  console.info(`${flag} shaderMixture created as composeShader input`);
  console.info(`${flag} success`);
} catch (e) {
  console.info(`${flag} errorCode: ${e.code}, errorMessage: ${e.message}`);
  expect().assertFail();
}
```

#### 方式三：唯一标识符验证（补充验证）

**适用场景**：对象有uniqueID等标识属性，可以通过验证标识符的有效性来间接确认对象有效性。

**示例：TextBlob.uniqueID()**
```typescript
const flag = 'TextBlob_uniqueID_test';
try {
  const font = new drawing.Font();
  font.setSize(50);
  const textBlob = drawing.TextBlob.makeFromString('Hello', font, drawing.TextEncoding.TEXT_ENCODING_UTF8);
  expect(textBlob !== null && textBlob !== undefined).assertTrue();
  console.info(`${flag} textBlob created`);
  const id = textBlob.uniqueID();
  console.info(`${flag} uniqueID: ${id}`);
  expect(id).assertLarger(0);
  console.info(`${flag} success`);
} catch (e) {
  console.info(`${flag} errorCode: ${e.code}, errorMessage: ${e.message}`);
  expect().assertFail();
}
```

#### 方式四：日志记录值验证（补充验证）

**适用场景**：对接口返回的有效值，如果没有get接口获取，需要添加日志记录接口返回的值，然后添加断言校验。

**示例：Path.getLength() 返回路径长度**
```typescript
const flag = 'getLength_test';
try {
  let pathLength = path.getLength(false);
  console.info(`${flag} success, pathLength: ${pathLength}`);
  expect(Math.abs(pathLength - 195.50) < 0.01).assertTrue();
} catch (e) {
  console.info(`${flag} errorCode: ${e.code}, errorMessage: ${e.message}`);
  expect().assertFail();
}
```

#### 验证方式选择原则

| 验证方式 | 适用场景 | 是否强制要求 | 优先级 |
|---------|---------|------------|-------|
| 方式一：调用自身接口 | 对象有可调用接口（如get方法） | ✅ 强制要求（首选） | 高 |
| 方式二：作为入参验证 | 对象无直接验证接口，但可作为其他接口入参 | ✅ 强制要求 | 高 |
| 方式三：唯一标识符验证 | 对象有uniqueID等标识属性 | ⚪ 补充验证 | 中 |
| 方式四：日志记录验证 | 无get接口但有返回值需验证 | ⚪ 补充验证 | 中 |

**建议验证顺序**：
1. 优先使用方式一，直接调用对象自身的接口进行验证
2. 若对象无可直接调用的验证接口，使用方式二，作为其他接口入参验证
3. 可结合方式三或方式四进行补充验证

### 3.2 对用例的代码逻辑的每个分支都添加有效断言

1、代码逻辑走到不应该到的分支使用expect().assertFail()做断言终结
```typescript
const flag = 'drawVertices_test';
try {
  canvas.drawVertices(drawing.VertexMode.TRIANGLESSTRIP_VERTEXMODE, null, pointsArray, texsArray, colors, 3, indices,drawing.BlendMode.SRC);
  console.info(`${flag} success`);
  expect().assertFail();
} catch (e) {
  console.info(`${flag} errorCode: ${e.code}, errorMessage: ${e.message}`);
  expect(e.code).assertEqual(25900001);
}
```

2、用例中不能出现恒真断言expect(true).assertTrue()