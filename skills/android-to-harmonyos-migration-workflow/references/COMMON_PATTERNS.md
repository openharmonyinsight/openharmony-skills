# 常见代码模式转换

## 单例模式

### Android (Kotlin)
```kotlin
object DatabaseManager {
    private var instance: MyDatabase? = null

    fun getInstance(context: Context): MyDatabase {
        return instance ?: synchronized(this) {
            instance ?: buildDatabase(context).also { instance = it }
        }
    }
}
```

### HarmonyOS (ArkTS)
```typescript
export class DatabaseManager {
  private static instance: DatabaseManager | null = null
  private database: MyDatabase | null = null

  private constructor() {}

  static getInstance(): DatabaseManager {
    if (!DatabaseManager.instance) {
      DatabaseManager.instance = new DatabaseManager()
    }
    return DatabaseManager.instance
  }

  async init(context: common.UIAbilityContext): Promise<void> {
    if (!this.database) {
      this.database = await this.buildDatabase(context)
    }
  }
}
```

## 回调转 Promise

### Android 回调
```kotlin
interface Callback {
    fun onSuccess(result: String)
    fun onError(error: Exception)
}

fun fetchData(callback: Callback) {
    // ...
}
```

### HarmonyOS Promise
```typescript
async fetchData(): Promise<string> {
  return new Promise((resolve, reject) => {
    // ...
    if (success) {
      resolve(result)
    } else {
      reject(error)
    }
  })
}

// 使用
try {
  const result = await this.fetchData()
} catch (error) {
  console.error(error)
}
```

## 集合操作

### Android (Kotlin)
```kotlin
val list = listOf(1, 2, 3)
val filtered = list.filter { it > 1 }
val mapped = list.map { it * 2 }
val reduced = list.reduce { acc, num -> acc + num }
```

### HarmonyOS
```typescript
const list: number[] = [1, 2, 3]
const filtered = list.filter(item => item > 1)
const mapped = list.map(item => item * 2)
const reduced = list.reduce((acc, num) => acc + num, 0)
```

## 空安全处理

### Android (Kotlin)
```kotlin
val name: String? = null
val length = name?.length ?: 0

val result = data?.let {
    process(it)
} ?: defaultValue
```

### HarmonyOS
```typescript
let name: string | null = null
const length = name?.length ?? 0

const result = data ? process(data) : defaultValue
```

## 数据类

### Android (Kotlin)
```kotlin
data class User(
    val id: Int,
    val name: String,
    val email: String
)
```

### HarmonyOS
```typescript
export class User {
  id: number = 0
  name: string = ''
  email: string = ''

  constructor(data?: Partial<User>) {
    if (data) {
      this.id = data.id ?? 0
      this.name = data.name ?? ''
      this.email = data.email ?? ''
    }
  }

  static create(data: Partial<User>): User {
    return new User(data)
  }
}
```

## 枚举

### Android (Kotlin)
```kotlin
enum class Color {
    RED, GREEN, BLUE
}

val color = Color.RED
```

### HarmonyOS
```typescript
export enum Color {
  RED = 'red',
  GREEN = 'green',
  BLUE = 'blue'
}

const color = Color.RED
```

## 接口实现

### Android (Kotlin)
```kotlin
interface ClickListener {
    fun onClick(view: View)
}

class MyListener : ClickListener {
    override fun onClick(view: View) {
        // 处理点击
    }
}
```

### HarmonyOS
```typescript
interface ClickListener {
  onClick(view: ClickEvent): void
}

class MyListener implements ClickListener {
  onClick(view: ClickEvent): void {
    // 处理点击
  }
}

// 或使用箭头函数
const listener: ClickListener = {
  onClick: (view: ClickEvent) => {
    // 处理点击
  }
}
```

## 常量定义

### Android (Kotlin)
```kotlin
object Constants {
    const val MAX_COUNT = 100
    val API_URL = "https://api.example.com"
}
```

### HarmonyOS
```typescript
export class Constants {
  static readonly MAX_COUNT: number = 100
  static readonly API_URL: string = 'https://api.example.com'
}

// 或使用
export const MAX_COUNT = 100
export const API_URL = 'https://api.example.com'
```

## 日志记录

### Android (Kotlin)
```kotlin
Log.d("TAG", "Debug message")
Log.i("TAG", "Info message")
Log.e("TAG", "Error message", exception)
```

### HarmonyOS
```typescript
import { hilog } from '@kit.PerformanceAnalysisKit'

const DOMAIN = 0x0001

hilog.debug(DOMAIN, 'TAG', 'Debug message: %{public}s', 'arg')
hilog.info(DOMAIN, 'TAG', 'Info message')
hilog.error(DOMAIN, 'TAG', 'Error message: %{public}s', JSON.stringify(error))
```
