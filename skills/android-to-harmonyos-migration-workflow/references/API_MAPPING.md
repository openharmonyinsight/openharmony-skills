# Android 到 HarmonyOS API 映射表

## 核心框架映射

| Android API | HarmonyOS API | 备注 |
|------------|---------------|------|
| `android.app.Activity` | `@Entry @Component` | Activity 转换为 Page 组件 |
| `android.app.Fragment` | `@Component` | Fragment 转换为普通组件 |
| `android.content.Context` | `common.UIAbilityContext` | 上下文获取方式不同 |
| `android.os.Bundle` | 路由参数对象 | 通过 router传递参数 |
| `android.intent` | `@kit.AbilityKit` Want | Intent/Intent 映射 |

## UI 组件映射

| Android | HarmonyOS | 说明 |
|---------|-----------|------|
| `RecyclerView` | `List` + `LazyForEach` | 列表组件 |
| `GridView` | `Grid` + `LazyForEach` | 网格组件 |
| `ViewPager` | `Swiper` | 滑动容器 |
| `LinearLayout` | `Column`/`Row` | 线性布局 |
| `RelativeLayout` | `RelativeContainer` | 相对布局 |
| `ConstraintLayout` | 详见映射 | 需要特殊处理 |
| `CardView` | `卡片样式` | 通过装饰器实现 |

## 数据存储映射

| Android | HarmonyOS | 备注 |
|---------|-----------|------|
| `Room Database` | `RelationalStore` | 关系型数据库 |
| `SharedPreferences` | `Preferences` | 轻量级存储 |
| `SQLiteOpenHelper` | `RdbStore` | 数据库帮助类 |
| `ContentProvider` | `DataShare` | 数据共享 |

## 媒体 API 映射

| Android | HarmonyOS | API 限制 |
|---------|-----------|----------|
| `MediaStore` | `photoAccessHelper` | API 22+ |
| `BitmapFactory` | `image.createImageSource` | - |
| `ExifInterface` | `image.ImagePacker` | - |
| `CursorLoader` | `FetchResult` | - |

## 网络映射

| Android | HarmonyOS |
|---------|-----------|
| `OkHttp` | `@kit.NetworkKit` http |
| `Retrofit` | 需自行封装 |
| `WebView` | `Web` 组件 |

## 权限映射

| Android | HarmonyOS |
|---------|-----------|
| `READ_EXTERNAL_STORAGE` | `ohos.permission.READ_IMAGEVIDEO` |
| `WRITE_EXTERNAL_STORAGE` | `ohos.permission.WRITE_IMAGEVIDEO` |
| `CAMERA` | `ohos.permission.CAMERA` |
| `INTERNET` | `ohos.permission.INTERNET` |
| `ACCESS_FINE_LOCATION` | `ohos.permission.APPROXIMATELY_LOCATION` |

## 异步处理映射

| Android | HarmonyOS |
|---------|-----------|
| `Thread` | `@kit.TaskPoolKit` taskpool |
| `ExecutorService` | taskpool |
| `Coroutine` | async/await |
| `LiveData` | `@Observed` + `@ObjectLink` |
| `Flow` | 自定义实现 |
| `Handler` | 不推荐使用 |

## 常用工具类映射

| Android | HarmonyOS |
|---------|-----------|
| `Log`/`Logger` | `hilog` |
| `Toast` | `promptAction` |
| `Snackbar` | 自定义组件 |
| `Dialog` | `CustomDialog` |
| `Gson` | `JSON.parse`/`JSON.stringify` |
| `SimpleDateFormat` | `@kit.I18nKit` |
| `Locale` | `I18n` |
