# Android 组件到 HarmonyOS 组件转换模式

## Activity 转换为 Page

### Android Activity
```kotlin
class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
    }
}
```

### HarmonyOS Page
```typescript
@Entry
@Component
struct MainPage {
  @State private message: string = 'Hello World'

  build() {
    Column() {
      Text(this.message)
    }
  }

  aboutToAppear() {
    // 相当于 onCreate
  }
}
```

## Fragment 转换为 Component

### Android Fragment
```kotlin
class MyFragment : Fragment() {
    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        return inflater.inflate(R.layout.fragment_my, container, false)
    }
}
```

### HarmonyOS Component
```typescript
@Component
export struct MyComponent {
  @Prop title: string = ''

  build() {
    Column() {
      Text(this.title)
    }
  }
}

// 使用方式
@Entry
@Component
struct ParentPage {
  build() {
    Column() {
      MyComponent({ title: 'Hello' })
    }
  }
}
```

## RecyclerView 转换

### Android RecyclerView
```kotlin
recyclerView.layoutManager = LinearLayoutManager(this)
recyclerView.adapter = MyAdapter(items)
```

### HarmonyOS List
```typescript
@Entry
@Component
struct ListPage {
  @State items: Item[] = []

  build() {
    List() {
      LazyForEach(new DataSource(this.items), (item: Item, index: number) => {
        ListItem() {
          Text(item.name)
        }
      })
    }
  }
}

class DataSource extends BasicDataSource {
  constructor(private items: Item[]) {
    super()
  }
}
```

## LiveData + ViewModel 转换

### Android MVVM
```kotlin
class MyViewModel : ViewModel() {
    private val _data = MutableLiveData<String>()
    val data: LiveData<String> = _data
}

// Activity 中
viewModel.data.observe(this) { value ->
    textView.text = value
}
```

### HarmonyOS 状态管理
```typescript
@Observed
class ViewModel {
  @Track data: string = ''

  setData(value: string) {
    this.data = value
  }
}

@Component
struct MyComponent {
  @ObjectLink viewModel: ViewModel

  build() {
    Text(this.viewModel.data)
  }
}
```

## AsyncTask 转换

### Android AsyncTask
```kotlin
class MyTask : AsyncTask<Void, Void, Result>() {
    override fun doInBackground(vararg params: Void): Result {
        // 后台任务
        return result
    }

    override fun onPostExecute(result: Result) {
        // 更新 UI
    }
}
```

### HarmonyOS async/await
```typescript
async doWork(): Promise<void> {
  try {
    const result = await this.backgroundTask()
    // 更新 UI
  } catch (error) {
    console.error(error)
  }
}

private async backgroundTask(): Promise<Result> {
  // 后台任务
  return result
}
```

## Dialog 转换

### Android Dialog
```kotlin
AlertDialog.Builder(this)
    .setTitle("Title")
    .setMessage("Message")
    .setPositiveButton("OK") { dialog, which -> }
    .show()
```

### HarmonyOS CustomDialog
```typescript
@CustomDialog
struct ConfirmDialog {
  controller: CustomDialogController
  title: string = ''
  message: string = ''

  build() {
    Column() {
      Text(this.title)
      Text(this.message)
      Button('OK')
        .onClick(() => {
          this.controller.close()
        })
    }
  }
}

// 使用
dialogController: CustomDialogController = new CustomDialogController({
  builder: ConfirmDialog({
    title: 'Title',
    message: 'Message'
  })
})
```

## 权限请求转换

### Android
```kotlin
ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA)
ActivityCompat.requestPermissions(this, arrayOf(Manifest.permission.CAMERA), 100)
```

### HarmonyOS
```typescript
import { abilityAccessCtrl, Permissions } from '@kit.AbilityKit'

async checkPermission(permission: Permissions): Promise<boolean> {
  const atManager = abilityAccessCtrl.createAtManager()
  const result = await atManager.checkAccessToken(this.context.applicationInfo.accessTokenId, permission)
  return result === abilityAccessCtrl.GrantStatus.PERMISSION_GRANTED
}

async requestPermissions(permissions: Permissions[]): Promise<void> {
  const atManager = abilityAccessCtrl.createAtManager()
  await atManager.requestPermissionsFromUser(this.context, permissions)
}
```
