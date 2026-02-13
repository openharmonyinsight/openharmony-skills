# 功能比对指南 (Feature Comparison Guide)

## 概述

功能比对者（Feature Comparator）负责对比 Android 源码与迁移后的 HarmonyOS 代码，找出遗漏的功能。

## 比对维度

### 1. 组件级别比对

| Android 组件 | HarmonyOS 对应 | 比对要点 |
|--------------|---------------|----------|
| Activity | @Entry Page | 检查页面数量、生命周期方法 |
| Fragment | @Component | 检查是否转为独立组件或内嵌 |
| Service | ServiceExtensionAbility | 检查后台服务迁移 |
| BroadcastReceiver | 事件订阅/发布 | 检查事件机制转换 |
| ViewModel | @Observed 类 | 检查状态管理迁移 |
| Repository | 数据层类 | 检查数据访问层 |

### 2. 功能点比对清单

#### 核心功能（CRITICAL）
- [ ] 用户登录/注册
- [ ] 数据同步
- [ ] 核心业务流程
- [ ] 支付/交易功能

#### 重要功能（HIGH）
- [ ] 消息推送
- [ ] 文件上传/下载
- [ ] 相机/拍照
- [ ] 位置服务

#### 一般功能（MEDIUM）
- [ ] 设置页面
- [ ] 分享功能
- [ ] 收藏/书签
- [ ] 搜索功能

### 3. API 调用覆盖比对

检查以下 Android API 是否在 HarmonyOS 中有对应实现：

| Android API | HarmonyOS 对应 | 状态 |
|-------------|---------------|------|
| SharedPreferences | preferences | |
| Room/SQLite | RelationalDB | |
| Retrofit/OkHttp | @ohos.net.http | |
| Glide/Coil | @ohos.multimedia.image | |
| CameraX | @ohos.multimedia.camera | |
| MediaStore | @ohos.file.photoAccessHelper | |
| LocationManager | @ohos.geoLocationManager | |
| NotificationManager | @ohos.notificationManager | |

## 使用方法

### 命令行执行

```bash
# 基本比对
python scripts/compare_features.py <android-source> <harmonyos-target>

# 输出到文件
python scripts/compare_features.py <android-source> <harmonyos-target> -o report.txt

# JSON 格式输出
python scripts/compare_features.py <android-source> <harmonyos-target> --json
```

### 报告解读

#### 功能覆盖率计算

```
覆盖率 = (完整迁移数 + 部分迁移数 × 0.5) / 总功能数 × 100%
```

| 覆盖率范围 | 评价 | 建议 |
|-----------|------|------|
| 90%+ | 优秀 | 可进行测试验证 |
| 70-90% | 良好 | 继续完善迁移 |
| 50-70% | 一般 | 加快迁移进度 |
| <50% | 较差 | 重新评估迁移策略 |

#### 优先级处理

1. **CRITICAL** 遗漏：立即处理，阻塞上线
2. **HIGH** 遗漏：本周内处理
3. **MEDIUM** 遗漏：两周内处理
4. **LOW** 遗漏：可选处理

## 常见遗漏场景

### 场景1：生命周期方法遗漏

Android Activity 有多个生命周期方法，迁移时可能遗漏：

```kotlin
// Android
class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) { }
    override fun onStart() { }
    override fun onResume() { }
    override fun onPause() { }
    override fun onStop() { }
    override fun onDestroy() { }
}
```

```typescript
// HarmonyOS 应对应
@Entry
@Component
struct MainPage {
  aboutToAppear() { }  // 对应 onCreate
  onAppear() { }       // 对应 onStart
  onPageShow() { }     // 对应 onResume
  onPageHide() { }     // 对应 onPause
  aboutToDisappear() { } // 对应 onStop
}
```

### 场景2：异步处理遗漏

Android 使用回调/协程，HarmonyOS 应使用 Promise/async-await：

```kotlin
// Android
viewModel.getData().observe(this) { data ->
    updateUI(data)
}
```

```typescript
// HarmonyOS
async aboutToAppear() {
    const data = await this.viewModel.getData();
    this.updateUI(data);
}
```

### 场景3：权限申请遗漏

Android 运行时权限需要在 HarmonyOS 中对应实现：

```kotlin
// Android
requestPermissions(arrayOf(Manifest.permission.CAMERA), 100)
```

```typescript
// HarmonyOS
import abilityAccessCtrl from '@ohos.abilityAccessCtrl';

async requestCameraPermission() {
    const atManager = abilityAccessCtrl.createAtManager();
    await atManager.requestPermissionsFromUser(context, ['ohos.permission.CAMERA']);
}
```

## 自动化检查脚本扩展

### 自定义组件识别

如需识别自定义组件模式，可编辑 `compare_features.py` 中的正则表达式：

```python
# 添加自定义模式
ANDROID_PATTERNS = {
    # ... 现有模式
    'CustomController': r'class\s+(\w+Controller)',
    'CustomManager': r'class\s+(\w+Manager)',
    'CustomHelper': r'class\s+(\w+Helper)',
}
```

### 自定义 API 识别

```python
# 添加需要检查的第三方库
ANDROID_API_PATTERNS = [
    # ... 现有模式
    r'Retrofit\.',
    r'OkHttp',
    r'Glide\.',
    r'Greenfoot\.',
]
```

## 与其他角色协作

| 角色 | 协作方式 |
|------|----------|
| Analyzer | 获取 Android 代码结构分析结果 |
| Translator | 提供遗漏功能的迁移实现 |
| Validator | 验证补充功能的代码质量 |
| Tester | 测试补充功能的正确性 |

## 输出模板

功能比对报告应包含以下部分：

```markdown
## 功能迁移比对报告

### 概览
- Android 功能总数: X
- 已完整迁移: Y
- 部分迁移: Z
- 未迁移: N
- 功能覆盖率: P%

### 遗漏功能清单 (按优先级)

#### CRITICAL
- [功能1] 描述...
  文件: xxx
  关键方法: xxx

#### HIGH
...

### 部分迁移功能
...

### 迁移建议
...
```
