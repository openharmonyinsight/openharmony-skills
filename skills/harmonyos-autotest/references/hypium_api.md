**配套Hypium版本: 6.0.7.210**

# hypium.action.app.launcher

**类型**: `module`

## Launcher

**类型**: `class`

**描述**

桌面相关操作，包括滑动找到app并打开，返回桌面首页等, 仅支持手机

**导入方式**

```python
from hypium.action.app.launcher import Launcher
```

### find_component

```python
def find_component(driver: UiDriver, selector: By, max_swipe_times: int = 8) -> UiComponent
```

**归属模块**: `hypium.action.app.launcher`

**归属类**: `Launcher`

**类型**: 函数

**描述**

在桌面上滑动查找指定控件

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| selector | By对象指定的控件查找条件 |
| max_swipe_times | 查找app时，最大滑动桌面屏幕的次数 |

**返回值**

无返回值描述

**示例**

```python
# 在桌面滑动查找key为card的控件
component = Launcher.find_component(driver, BY.key("card"))
```

### start_app

```python
def start_app(driver: UiDriver, app_name: str, match_pattern: MatchPattern = MatchPattern.EQUALS, max_swipe_times: int = 8)
```

**归属模块**: `hypium.action.app.launcher`

**归属类**: `Launcher`

**类型**: 函数

**描述**

滑动桌面找到名为 app_name 的应用并点击打开

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| app_name | 需要查找的app名称(用户看到的app名称，不是包名，用UiView工具看到的text或者description) |
| max_swipe_times | 查找app时，最大滑动桌面屏幕的次数 |

**返回值**

无返回值描述

**示例**

```python
# 桌面点击启动抖音
Launcher.start_app(driver, "抖音")
```

### go_home

```python
def go_home(driver: UiDriver)
```

**归属模块**: `hypium.action.app.launcher`

**归属类**: `Launcher`

**类型**: 函数

**描述**

通过按home键回到桌面主页, 如果在其他页面，一般需要连续按2次主页键才能保证回到桌面主页

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

无返回值描述

**示例**

```python
# 回到桌面首页
Launcher.go_home(driver)
```

### clear_recent_task

```python
def clear_recent_task(driver: UiDriver, clear_button_id: str = None)
```

**归属模块**: `hypium.action.app.launcher`

**归属类**: `Launcher`

**类型**: 函数

**描述**

进入多任务界面并清理后台应用

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| clear_button_id | 可选, 多任务界面清理按钮的id, 不设置则使用默认的id |

**返回值**

无返回值描述

**示例**

```python
# 进入多任务界面清理后台
Launcher.clear_recent_task(driver)
```

# hypium.action.device.uidriver

**类型**: `module`

## UiDriver

**类型**: `class`

**描述**

设备Ui测试核心功能类, 提供控件查找/设备点击/滑动操作, app启动停止等常用功能

**导入方式**

```python
from hypium.action.device.uidriver import UiDriver
```

### close_display

```python
def close_display()
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

关闭屏幕, 如果屏幕已经关闭则无动作

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

无返回值描述

**示例**

```python
# 关闭屏幕
driver.close_display()
```

### unlock

```python
def unlock()
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

唤醒并解锁屏幕

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

无返回值描述

**示例**

```python
# 唤醒并解锁屏幕
driver.unlock()
```

### set_sleep_time

```python
def set_sleep_time(sleep_time: float)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

设置熄屏时间, 注意该接口设置的熄屏时间仅临时生效, 不会修改系统设置中设置的熄屏时间,
在屏幕熄屏一次后将恢复设置应用中的熄屏时间

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| sleep_time | 熄屏时间, 单位秒 |

**返回值**

无返回值描述

**示例**

```python
# 设置熄屏时间为600秒
driver.set_sleep_time(600)
```

### restore_sleep_time

```python
def restore_sleep_time()
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

恢复设置应用中设置的熄屏时间。注意需要先调用driver.set_sleep_time后该接口才能正常调用，否则
会执行失败。

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

无返回值描述

**示例**

```python
# 设置熄屏时间为600秒
driver.set_sleep_time(600)
# 恢复设置应用中设置的熄屏时间
driver.restore_sleep_time()
```

### add_hook

```python
def add_hook(hook_type, hook_id, callback)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

添加操作事件钩子

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| hook_type | 钩子函数触发的事件类型, 当前仅支持EventManager.EVENT_UI_ACTION_START, 该钩子函数会在框架进行设备操作前触发 |
| hook_id | 钩子函数自定义id, 每个id对应一个钩子函数, 相同的id会覆盖已有的钩子函数, 不同的id可以设置多个钩子函数 |
| callback | 钩子函数, 函数签名为callback(event_type: str, param: dict) |

**返回值**

无返回值描述

**示例**

```python
from hypium.utils.event_manager import EventManager
# 为EventManager.EVENT_UI_ACTION_START事件添加一个钩子函数print_test, 钩子函数id为id为perf_hook
driver.add_hook(EventManager.EVENT_UI_ACTION_START, "perf_hook", print_test)
```

### remove_hook

```python
def remove_hook(hook_type, hook_id)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

移除操作事件钩子

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| hook_type | 钩子函数触发的事件类型, 当前仅支持EventManager.EVENT_UI_ACTION_START, 该钩子函数会在框架进行设备操作前触发 |
| hook_id | 钩子函数自定义id, 每个id对应一个钩子函数 |

**返回值**

无返回值描述

**示例**

```python
from hypium.utils.event_manager import EventManager
# 移除EventManager.EVENT_UI_ACTION_START事件中id为perf_hook的钩子
driver.remove_hook(EventManager.EVENT_UI_ACTION_START, "perf_hook")
```

### remove_all_hooks

```python
def remove_all_hooks(hook_type)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

移除指定事件的所有钩子

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| hook_type | 钩子函数触发的事件类型 |

**返回值**

无返回值描述

**示例**

```python
from hypium.utils.event_manager import EventManager
# 移除EventManager.EVENT_UI_ACTION_START事件的所有钩子
driver.remove_all_hooks(EventManager.EVENT_UI_ACTION_START)
```

### connect

```python
def connect(connector="hdc", **kwargs) -> 'UiDriver'
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

在非hypium用例类中快速创建driver, hypium用例类中请使用UiDriver(self.device1)创建UiDriver
默认连接第一可用的设备

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| connector | 设备连接模式, 当前仅支持hdc |
| kwargs | 其他配置参数, 当前支持<br>device_sn: 指定连接的设备sn号, 不指定则使用hdc读取的第一个设备<br>report_path: 指定driver落盘日志保存目录, 默认为工作目录reports下当前时间命名的目录, 不存在会自动创建<br>如果指定目录，则日志保存到指定目录中，指定目录必须存在<br>log_level: 指定打印日志级别, 默认info -- 当前支持info/debug<br>connector_server: 远程设备服务器地址, 格式为(ip, port), 在连接远程hdc server时使用。 |

**返回值**

无返回值描述

**示例**

```python
# 连接默认设备
driver = UiDriver.connect()
# 连接指定设备
driver = UiDriver.connect(device_sn="xxxxxx")
# 自定义落盘日志目录
driver = UiDriver.connect(report_path="tmp")
# 开启debug日志
driver = UiDriver.connect(log_level="debug")
# 连接远程设备
driver = UiDriver.connect(connector_server=("10.176.11.11", 8710))
# 注意结束driver使用后需要调用driver.close清理端口, 释放资源
driver.close()
```

### close

```python
def close()
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

关闭驱动, 断开与设备的连接并清理连接资源。
仅当使用UiDriver.connect方式创建设备驱动，并且驱动对象不再使用时调用。
如果在Hypium框架用例工程中创建驱动则无需主动调用，任务直接结束会自动完成释放。

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

无返回值描述

**示例**

```python

# 通过UiDriver.connect方式连接
driver = UiDriver.connect()
# 调用driver执行操作
driver.go_home()
# 不再使用driver时关闭
driver.close()
```

### device_sn

```python
def device_sn()
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 属性

**描述**

读取设备的sn号

### log

```python
def log() -> ILog
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 属性

**描述**

日志模块, 支持打印记录到用例报告中的日志

### get_device_type

```python
def get_device_type() -> str
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

读取设备类型

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### set_implicit_wait_time

```python
def set_implicit_wait_time(wait_time: float)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

设置操作控件类的接口在控件未出现时等待的超时时间

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| wait_time | 操作控件类的接口在控件未出现时等待的时间 |

**返回值**

无返回值描述

**示例**

```python
driver.set_implicit_wait_time(10)
```

### hdc

```python
def hdc(cmd, timeout: float = 60) -> str
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

执行hdc命令

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| cmd | 执行的hdc命令 |
| timeout | 超时时间, 单位秒 |

**返回值**

命令执行后的回显内容

**示例**

```python
# 执行hdc命令list targets
echo = driver.hdc("list targets")
# 执行hdc命令hilog, 设置30秒超时
echo = driver.hdc("hilog", timeout = 30)
```

### shell

```python
def shell(cmd: str, timeout: float = 60) -> str
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

在设备端shell中执行命令

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| cmd | 执行的shell命令 |
| timeout | 超时时间, 单位秒 |

**返回值**

命令执行后的回显内容

**示例**

```python
# 在设备shell中执行命令ls -l
echo = driver.shell("ls -l")
# 在设备shell中执行命令top, 设置10秒超时时间
echo = driver.shell("top", timeout=10)
```

### pull_file

```python
def pull_file(device_path: str, local_path: str = None, timeout: int = 60)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

从设备端的传输文件到pc端

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| device_path | 设备侧保存文件的路径 |
| local_path | PC侧保存文件的路 |
| timeout | 拉取文件超时时间, 默认60秒 |

**返回值**

无返回值描述

**示例**

```python
# 从设备中拉取文件"/data/local/tmp/test.log"保存到pc端的test.log
driver.pull_file("/data/local/tmp/test.log", "test.log")
```

### push_file

```python
def push_file(local_path: str, device_path: str, timeout: int = 60)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

从pc端传输文件到设备端

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| local_path | PC侧文件的路径 |
| device_path | 设备侧文件的路径 |
| timeout | 推送文件超时时间 |

**返回值**

无返回值描述

**示例**

```python
# 从设备中推送文件test.hap保存到设备端的"/data/local/tmp/test.hap"
driver.push_file("test.hap", "/data/local/tmp/test.hap")
```

### has_file

```python
def has_file(file_path: str) -> bool
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

查询设备中是否有存在路径为file_path的文件

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| file_path | 需要检查的设备端文件路径 |

**返回值**

无返回值描述

**示例**

```python
# 查询设备端是否存在文件/data/local/tmp/test_file.txt
driver.has_file("/data/local/tmp/test_file.txt")
```

### wait

```python
def wait(wait_time: float)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

等待wait_time秒

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| wait_time | 等待秒数 |

**返回值**

无返回值描述

**示例**

```python
# 等待5秒钟
driver.wait(5)
```

### start_app

```python
def start_app(package_name: str, page_name: str = None, params: str = "", wait_time: float = 1)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

根据包名启动指定的app

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| package_name | 应用程序包名(bundle_name) |
| page_name | 应用内页面名称(ability_name) |
| params | 其他传递给aa命令行参数 |
| wait_time | 发送启动指令后，等待app启动的时间 |

**返回值**

无返回值描述

**示例**

```python
# 启动包名为com.huawei.hmos.browser应用的MainAbility
driver.start_app("com.huawei.hmos.browser", "MainAbility")
```

### stop_app

```python
def stop_app(package_name: str, wait_time: float = 0.5)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

停止指定的应用

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| package_name | 应用程序包名 |
| wait_time | 停止app后延时等待的时间, 单位为秒 |

**返回值**

无返回值描述

**示例**

```python
# 停止包名为com.huawei.hmos.browser的应用
driver.stop_app("com.huawei.hmos.browser")
```

### has_app

```python
def has_app(package_name: str) -> bool
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

查询是否安装指定包名的app

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| package_name | 需要检查的应用程序包名 |

**返回值**

无返回值描述

**示例**

```python
has_app = driver.has_app("com.huawei.hmos.settings")
```

### current_app

```python
def current_app() -> (str, str)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

获取当前前台运行的app信息

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

app包名和页面名称, 例如('com.huawei.hmos.settings', 'com.huawei.hmos.settings.MainAbility'),
如果读取失败则返回(None, None)

**示例**

```python
package_name, page_name = driver.current_app()
```

### install_app

```python
def install_app(package_path: str, options: str = "", **kwargs)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

安装app

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| package_path | PC端保存的安装包路径 |
| options | 传递给install命令的额外参数 |

**返回值**

无返回值描述

**示例**

```python
# 安装路径为test.hap的安装包到手机
driver.install_app(r"test.hap")
# 替换安装路径为test.hap的安装包到手机(增加-r参数指定替换安装)
driver.install_app(r"test.hap", "-r")
```

### uninstall_app

```python
def uninstall_app(package_name: str, **kwargs)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

卸载App

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| package_name | 需要卸载的app包名 |

**返回值**

无返回值描述

**示例**

```python
driver.uninstall_app("com.ohos.devicetest")
```

### clear_app_data

```python
def clear_app_data(package_name: str)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

清除app的数据

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| package_name | app包名，对应Openharmony中的bundle name |

**返回值**

无返回值描述

**示例**

```python
# 清除包名为com.tencent.mm的应用的所有数据
driver.clear_app_data("com.tencent.mm")
```

### wake_up_display

```python
def wake_up_display()
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

唤醒屏幕

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

无返回值描述

**示例**

```python
# 唤醒屏幕
driver.wake_up_display()
```

### get_display_rotation

```python
def get_display_rotation() -> DisplayRotation
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

获取当前设备的屏幕显示方向

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

无返回值描述

**示例**

```python
# 获取当前设备的屏幕显示方向
display_rotation = driver.get_display_rotation()
```

### set_display_rotation

```python
def set_display_rotation(rotation: DisplayRotation)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

将设备的屏幕显示方向设置为指定的显示方向。注意部分应用不支持旋转，该接口设置的旋转方向在
此类应用上不会生效

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| rotation | 屏幕旋转方向, 取值范围为DisplayRotation枚举值。 |

**返回值**

无返回值描述

**示例**

```python
# 顺时针选择90度
driver.set_display_rotation(DisplayRotation.ROTATION_90)
# 顺时针选择180度
driver.set_display_rotation(DisplayRotation.ROTATION_180)
```

### set_display_rotation_enabled

```python
def set_display_rotation_enabled(enabled: bool)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

启用/禁用设备旋转屏幕的功能

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| enabled | 能否旋转屏幕的标识 |

**返回值**

无返回值描述

**示例**

```python
# 设置开启/关闭设备自动旋转。
driver.set_display_rotation_enabled(True)
driver.set_display_rotation_enabled(False)
```

### drag

```python
def drag(start: Union[ISelector, tuple, IUiComponent], end: Union[ISelector, tuple, IUiComponent], area: Union[ISelector, IUiComponent] = None, press_time: float = 1.5, drag_time: float = 1, speed: int = None)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

根据指定的起始和结束位置执行拖拽操作，起始和结束的位置可以为控件或者屏幕坐标

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| start | 拖拽起始位置，支持三种类型：<br>1. BY控件选择器<br>2. 控件对象<br>3. 屏幕坐标（通过tuple类型指定，例如(100, 200)， 其中100为x轴坐标，200为y轴坐标，<br>或相对于区域长度和宽度的比例坐标，例如(0.1, 0.2)。) |
| end | 拖拽结束位置<br>1. BY控件选择器<br>2. 控件对象<br>3. 屏幕坐标（通过tuple类型指定，例如(100, 200)， 其中100为x轴坐标，200为y轴坐标，<br>或者相对于区域长度和宽度的比例坐标，例如(0.1, 0.2)。) |
| area | 拖拽操作区域，可以为控件BY.text("画布"), 或者使用find_component找到的控件对象。<br>目前仅在start或者end为坐标时生效，指定区域后，当start和end为坐标时，其坐标将被视为相对于指定的区域<br>的相对位置坐标。 |
| press_time | 拖拽操作开始时，长按的时间, 默认为1.5s。 该参数仅设备API level >= 20时支持设置。 |
| drag_time | 拖动的时间， 默认为1s(整个拖拽操作总时间 = press_time + drag_time) |
| speed | 拖拽速度, 指定速度时, drag_time不生效 |

**返回值**

无返回值描述

**示例**

```python
# 拖拽文本为"文件.txt"的控件到文本为"上传文件"的控件
driver.drag(BY.text("文件.txt"), BY.text("上传文件"))
# 拖拽id为"start_bar"的控件到坐标(100, 200)的位置, 拖拽时间为2秒
driver.drag(BY.key("start_bar"), (100, 200), drag_time=2)

# 在id为"Canvas"的控件上执行拖拽操作，从"Canvas"控件中(0.1， 0.5)的位置拖拽到(0.9, 0.5)位置。
# 假如"Canvas"控件左上角坐标(100, 100), 宽度为200，高度为50，此操作等价于
# driver.drag((100 + 0.1 * 200, 100 + 0.5 * 50), (100 + 0.9 * 200, 100 + 0.5 * 50))
driver.drag((0.1, 0.5), (0.9, 0.5), area=BY.id("Canvas"))

# 在滑动条上执行拖拽操作, 以滑动条组件左上角为原点, 从滑动条区域中的(10, 10)拖拽到(10, 200)。
# 假设滑动条左上角坐标为(500, 500), 此操作等价于driver.drag((500 + 10, 500 + 10), (500 + 10, 500 + 200))
driver.drag((10, 10), (10, 200), area=BY.type("Slider"))
```

### touch

```python
def touch(target: Union[ISelector, IUiComponent, tuple], mode: str = "normal", scroll_target: Union[ISelector, IUiComponent] = None, wait_time: float = 0.1, offset: tuple = None)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

根据选定的控件或者坐标位置执行点击操作

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| target | 需要点击的目标，可以为控件(通过By类指定)或者屏幕坐标(通过tuple类型指定，<br>例如(100, 200)， 其中100为x轴坐标，200为y轴坐标), 或者使用find_component找到的控件对象 |
| mode | 点击模式，目前支持:<br>"normal" 点击<br>"long" 长按（长按后放开）<br>"double" 双击 |
| scroll_target | 指定可滚动的控件，在该控件中滚动搜索指定的目标控件target。仅在<br>target为`By`对象时有效 |
| wait_time | 点击后等待响应的时间，默认0.1s |
| offset | 点击坐标相对目标控件的偏移, 例如(0.5, 0.5)表示点击目标中心, (0, 0)表示左上角, (1, 1)表示右下角<br>支持负数, 每个方向的偏移值取值范围为[-1, 1] |

**返回值**

无返回值描述

**示例**

```python
# 点击文本为"hello"的控件
driver.touch(BY.text("hello"))
# 点击(100, 200)的位置
driver.touch((100, 200))
# 点击比例坐标为(0.8, 0.9)的位置
driver.touch((0.8, 0.9))
# 双击确认按钮(控件文本为"确认", 类型为"Button")
driver.touch(BY.text("确认").type("Button"), mode=UiParam.DOUBLE)
# 在类型为Scroll的控件上滑动查找文本为"退出"的控件并点击
driver.touch(BY.text("退出"), scroll_target=BY.type("Scroll"))
# 长按比例坐标为(0.8, 0.9)的位置
driver.touch((0.8, 0.9), mode="long")
```

### find_image

```python
def find_image(image_path_pc: str, mode="sift", **kwargs) -> Rect
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

在屏幕上查找指定图片的位置

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| image_path_pc | 模板图片的路径 |
| mode | 图片匹配模式, 支持template和sift, 图片分辨率/旋转变化对sift模式影响相对较小，但sift模式难以处理缺少较复杂图案<br>的纯色，无线条图片 |
| kwargs | 其他配置参数<br>min_match_point: sift模式支持, 最少匹配特征点数, 值越大匹配越严格, 默认为16<br>similarity: template模式支持，图片最小相似度 |

**返回值**

图片在屏幕上的矩形区域位置, 如果没有找到则返回None

**示例**

```python
# 在屏幕上查找icon.png的位置
bounds = driver.find_image("icon.png")
# 点击图片中心坐标
driver.touch(bounds.get_center())
```

### touch_image

```python
def touch_image(image_path_pc: str, mode: str = "normal", similarity: float = 0.95, wait_time: int = 0.1, **kwargs)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

在屏幕上显示内容同图片image_path_pc内容相同的位置执行点击操作， 注意模板图片分辨率需与屏幕目标区域一致，
如果图片被缩放或旋转将无法正常匹配到正确的位置。

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| image_path_pc | 需要点击的图像的存储路径(图片存储在PC端) |
| mode | 点击模式，目前支持:<br>"normal" 点击<br>"long" 长按（长按后放开）<br>"double" 双击 |
| wait_time | 点击后等待响应的时间，默认0.1s |
| kwargs | 其他配置参数<br>min_match_point: 最少匹配特征点数, 值越大匹配越严格, 默认为16个(同similarity参数独立，用于控制另外一种算法匹配图片) |

**返回值**

无返回值描述

**示例**

```python
# 使用图片的方式点击屏幕上显示内容为button.jpeg的位置
driver.touch_image("button.jpeg")
# 双击图片button.jpeg的位置
driver.touch_image("button.jpeg", mode=UiParam.DOUBLE)
# 长按图片button.jpeg的位置
driver.touch_image("button.jpeg", mode=UiParam.LONG)
# 点击图片button.jpeg的位置, 相似度设置为0.8
driver.touch_image("button.jpeg", similarity=0.8)
# 点击图片button.jpeg的位置, 特征点最少匹配16个
driver.touch_image("button.jpeg", min_match_point=16)
```

### switch_component_status

```python
def switch_component_status(component: Union[ISelector, IUiComponent], checked: bool)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

切换带有状态的控件的状态，例如单选框选中与取消选中

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| component | 操作的目标控件 |
| checked | 设置控件的check状态 |

**返回值**

无返回值描述

**示例**

```python
# 切换id为"confirm_checkbox"的控件为选中状态
driver.switch_component_status(BY.key("confirm_checkbox"), checked=True)
# 切换id为"confirm_checkbox"的控件为未选中状态
driver.switch_component_status(BY.key("confirm_checkbox"), checked=False)
```

### press_combination_key

```python
def press_combination_key(key1: Union[KeyCode, int], key2: Union[KeyCode, int], key3: Union[KeyCode, int] = None)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

按下组合键, 支持2键或者3键组合

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| key1 | 组合键第一个按键 |
| key2 | 组合键第二个按键 |
| key3 | 组合键第三个按键(HMOS不支持三键组合, 第三个按键不会生效) |

**返回值**

无返回值描述

**示例**

```python
# 按下音量下键和电源键的组合键
driver.press_combination_key(KeyCode.VOLUME_DOWN, KeyCode.POWER)
# 同时按下ctrl, shift和F键
driver.press_combination_key(KeyCode.CTRL_LEFT, KeyCode.SHIFT_LEFT, KeyCode.F)
```

### press_key

```python
def press_key(key_code: Union[KeyCode, int], key_code2: Union[KeyCode, int] = None, mode="normal")
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

按下指定按键(按组合键请使用press_combination_key)

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| key_code | 需要按下的按键编码 |
| key_code2 | 需要按下的按键编码 |
| mode | 按键模式, 仅在进行单个按键时支持，支持:<br>UiParam.NORMAL 默认, 按一次<br>UiParam.LONG 长按<br>UiParam.DOUBLE 双击 |

**返回值**

无返回值描述

**示例**

```python
# 按下电源键
driver.press_key(KeyCode.POWER)
# 长按电源键
driver.press_key(KeyCode.POWER, mode=UiParam.LONG)
# 按下音量下键
driver.press_key(KeyCode.VOLUME_DOWN)
```

### press_home

```python
def press_home()
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

按下HOME键

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

无返回值描述

**示例**

```python
# 按下home键
driver.press_home()
```

### go_home

```python
def go_home()
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

返回桌面(不关心返回桌面的方式，自动决定最稳定的返回桌面方式)

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

无返回值描述

**示例**

```python
# 返回桌面
driver.go_home()
```

### go_back

```python
def go_back()
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

返回上一级(不关心返回桌面的方式，自动决定最稳定的返回方式)

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

无返回值描述

**示例**

```python
# 返回桌面
driver.go_back()
```

### press_power

```python
def press_power()
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

按下电源键

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

无返回值描述

**示例**

```python
# 按下电源键
driver.press_power()
```

### get_component_bound

```python
def get_component_bound(component: Union[ISelector, IUiComponent]) -> Rect
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

获取指定的控件的边界矩形区域

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| component | 需要获取边框位置的控件选择器或者控件对象 |

**返回值**

返回控件边界坐标的Rect对象，如果没找到控件则返回None

**示例**

```python
# 获取text为按钮的控件的边框位置
bounds = driver.get_component_bound(BY.text("按钮"))
# 获取控件对象的边框位置
component = driver.find_component(BY.text("按钮"))
bounds = driver.get_component_bound(component)
```

### press_back

```python
def press_back()
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

按下返回键

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

无返回值描述

**示例**

```python
# 按下返回键
driver.press_back()
```

### slide

```python
def slide(start: Union[ISelector, tuple], end: Union[ISelector, tuple], area: Union[ISelector, IUiComponent] = None, slide_time: float = DEFAULT_SLIDE_TIME)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

根据指定的起始和结束位置执行滑动操作，起始和结束的位置可以为控件或者屏幕坐标。该接口用于执行较为精准的滑动操作。

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| start | 滑动起始位置，可以为控件BY.text("滑块")或者坐标(100, 200), 或者使用find_component找到的控件对象 |
| end | 滑动结束位置，可以为控件BY.text("最大值")或者坐标(100, 200), 或者使用find_component找到的控件对象 |
| area | 滑动操作区域，可以为控件BY.text("画布")。目前仅在start或者end为坐标<br>时生效，指定区域后，当start和end为坐标时，其坐标将被视为相对于指定的区域<br>的相对位置坐标。 |
| slide_time | 滑动操作总时间，单位秒 |

**返回值**

无返回值描述

**示例**

```python
# 从类型为Slider的控件滑动到文本为最大的控件
driver.slide(BY.type("Slider"), BY.text("最大"))
# 从坐标100, 200滑动到300，400
driver.slide((100, 200), (300, 400))
# 从坐标100, 200滑动到300，400, 滑动时间为3秒
driver.slide((100, 200), (300, 400), slide_time=3)
# 在类型为Slider的控件上从(0, 0)滑动到(100, 0)
driver.slide((0, 0), (100, 0), area = BY.type("Slider"))
```

### swipe

```python
def swipe(direction: str, distance: int = 60, area: Union[ISelector, IUiComponent] = None, side: str = None, start_point: tuple = None, swipe_time: float = 0.3, speed: int = None)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

在屏幕上或者指定区域area中执行朝向指定方向direction的滑动操作。该接口用于执行不太精准的滑动操作。

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| direction | 滑动方向，目前支持:<br>"LEFT" 左滑<br>"RIGHT" 右滑<br>"UP" 上滑<br>"DOWN" 下滑 |
| distance | 相对滑动区域总长度的滑动距离，范围为1-100, 表示滑动长度为滑动区域总长度的1%到100%， 默认为60 |
| area | 通过控件指定的滑动区域 |
| side | 滑动位置， 指定滑动区域内部(屏幕内部)执行操作的大概位置，支持:<br>UiParam.LEFT 靠左区域<br>UiParam.RIGHT 靠右区域<br>UiParam.TOP 靠上区域<br>UiParam.BOTTOM 靠下区域 |
| start_point | 滑动起始点, 默认为None, 表示在区域中间位置执行滑动操作, 可以传入滑动起始点坐标，支持使用(0.5, 0.5)<br>这样的比例坐标。当同时传入side和start_point的时候, |
| swipe_time | 滑动时间（s)， 默认0.3s |
| speed | 滑动速度, 单位像素/秒, 指定速度时, swipe_time不生效 |

**返回值**

无返回值描述

**示例**

```python
# 在屏幕上向上滑动, 距离40
driver.swipe(UiParam.UP, distance=40)
# 在屏幕上向右滑动, 滑动时间为0.1秒
driver.swipe(UiParam.RIGHT, swipe_time=0.1)
# 在屏幕起始点为比例坐标为(0.8, 0.8)的位置向上滑动，距离30
driver.swipe(UiParam.UP, 30, start_point=(0.8, 0.8))
# 在屏幕左边区域向下滑动， 距离30
driver.swipe(UiParam.DOWN, 30, side=UiParam.LEFT)
# 在屏幕右侧区域向上滑动，距离30
driver.swipe(UiParam.UP, side=UiParam.RIGHT)
# 在类型为Scroll的控件中向上滑动
driver.swipe(UiParam.UP, area=BY.type("Scroll"))
```

### find_component

```python
def find_component(target: ISelector, scroll_target: ISelector = None) -> IUiComponent
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

根据BY指定的条件查找控件, 返回满足条件的第一个控件对象

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| target | 使用By对象描述的查找条件 |
| scroll_target | 滑动scroll_target控件, 搜索target |

**返回值**

返回控件对象IUiComponent, 如果没有找到满足条件的控件，则返回None

**示例**

```python
# 查找类型为button的第一个控件对象
component = driver.find_component(BY.type("button"))
# 获取控件对象的文本
text = component.getText()
# 在类型为Scroll的控件上滚动查找文本为"拒绝"的控件
component = driver.find_component(BY.text("拒绝"), scroll_target=BY.type("Scroll"))
```

### find_all_components

```python
def find_all_components(target: ISelector, index: int = None) -> Union[IUiComponent, List[IUiComponent]]
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

根据BY指定的条件查找控件, 返回满足条件的所有控件对象列表, 或者列表中第index个控件对象

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| target | 使用By对象描述的查找条件 |
| index | 默认为None, 表示返回所有控件列表，当传入整数时, 返回列表中第index个对象 |

**返回值**

返回控件对象IUiComponent或者控件对象列表, 例如[component1, component2], 每个
如果没有找到满足条件的控件，则返回None

**示例**

```python
# 查找所有类型为"button"的控件
components = driver.find_all_components(BY.type("Button"))
# 查找满足条件的第3个控件(index从0开始)
component = driver.find_all_components(BY.type("Button"), 2)
# 点击控件
driver.touch(component)
```

### find_window

```python
def find_window(filter: WindowFilter) -> UiWindow
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

根据指定条件查找窗口, 返回窗口对象

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| filter | 使用WindowFilter对象指定查找条件 |

**返回值**

如果找到window则返回UiWindow对象, 否则返回None

**示例**

```python
# 查找标题为日历的窗口
window = driver.find_window(WindowFilter().title("日历"))
# 查找包名为com.huawei.hmos.settings，并且处于活动状态的窗口
window = driver.find_window(WindowFilter().bundle_name("com.huawei.hmos.settings").actived(True))
# 查找处于活动状态的窗口
window = driver.find_window(WindowFilter().actived(True))
# 查找聚焦状态的窗口
window = driver.find_window(WindowFilter().focused(True))
```

### get_display_size

```python
def get_display_size() -> (int, int)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

返回屏幕分辨率

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

(宽度, 高度)

**示例**

```python
# 获取屏幕分辨率
width, height = driver.get_display_size()
```

### get_window_size

```python
def get_window_size() -> (int, int)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

获取当前处于活动状态的窗口大小

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

(宽度, 高度), 如果不存在活动/获焦的窗口则返回None

**示例**

```python
# 获取当前活动状态的窗口大小
width, height = driver.get_window_size()
```

### get_current_window

```python
def get_current_window() -> UiWindow
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

返回当前用户正在操作的窗口(处于活动或者获焦状态的窗口对)

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

窗口对象，如果不存在活动或者获焦的窗口，则返回None

**示例**

```python
# 获取当前活动的窗口对象
window = driver.get_current_window()
# 读取窗口所属的应用包名
bundle_name = window.getBundleName()
# 读取窗口边框
bounds = window.getBounds()
```

### get_component_property

```python
def get_component_property(component: Union[ISelector, IUiComponent], property_name: str) -> Any
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

获取指定控件属性

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| component | By对象指定的控件或者IUiComponent控件对象 |
| property_name | 属性名称, 目前支持:<br>"id", "text", "key", "type", "enabled", "focused", "clickable", "scrollable"<br>"checked", "checkable" |

**返回值**

指定控件的指定属性值

**示例**

```python
# 获取类型为"checkbox"的控件的checked状态
checked = driver.get_component_property(BY.type("Toggle"), "checked")
# 获取id为"text_container"的控件的文本属性
text = driver.get_component_property(BY.key("text_container"), "text")
```

### capture_screen

```python
def capture_screen(save_path: str, in_pc: bool = True, area: Union[Rect, ISelector, IUiComponent] = None) -> str
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

通过系统命令获取屏幕截图的图片, 并保存到设备或者PC上指定位置

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| save_path | 截图保存路径(目录 + 文件名) |
| in_pc | 保存路径是否为PC端路径, True表示为PC端路径, False表示设备端路径 |
| area | 指定区域截图, 可以通过控件或者Rect对象指定截图区域 |

**返回值**

截图文件保存的路径

**示例**

```python
# 截屏保存到test.jpeg
driver.capture_screen("test.jpeg")
# 截取id为icon的控件区域的图片, 保存到area.jpeg
driver.capture_screen("area.jpeg", area=BY.key("icon"))
# 截取屏幕中区域(left, right, top, bottom)的图片, 保存到area2.jpeg
driver.capture_screen("area2.jpeg", area=Rect(left, right, top, bottom))
```

### take_screenshot

```python
def take_screenshot(mode: str = "key")
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

模拟用户触发系统截屏的操作, 例如通过按音量下键+电源键

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| mode | 进行系统截屏的方式，当前支持<br>"key" 例如通过按音量下键+电源键<br>默认通过按音量下键+电源键实现 |

**返回值**

无返回值描述

**示例**

```python
# 模拟用户执行截屏操作
driver.take_screenshot()
```

### input_text

```python
def input_text(component: Union[ISelector, IUiComponent, tuple], text: str, mode: InputTextMode = None)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

向指定控件中输入文本内容

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| component | 需要输入文本的控件，可以使用ISelector对象，<br>或者使用find_component找到的控件对象,<br>以及坐标点(x, y) |
| text | 需要输入的文本 |
| mode | 输入模式配置(该参数需要设备API level >= 20支持), 默认模式如下:<br>1. 默认清空指定的控件中的文本后再执行输入<br>2. 英文字符长度<200时, 逐个输入, 超过200时, 通过剪切板粘贴一次输入<br>3. 中文文本通过剪切板粘贴一次输入<br>通过该参数可以配置<br>1. 追加输入. InputTextMode().addition(True)<br>2. 是否不考虑文本长度直接使用剪切板或者逐个文字输入 InputTextMode().paste(True) |

**返回值**

无返回值描述

**示例**

```python
# 在类型为"TextInput"的控件中输入文本"hello world"
driver.input_text(BY.type("TextInput"), "hello world")
# 在类型为"TextInput"的控件中使用剪切板一次性输入文本"hello world"
driver.input_text(BY.type("TextInput"), "hello world", mode=InputTextMode().paste(True))
# 在类型为"TextInput"的控件中使用剪切板一次性并追加输入文本"hello world"
driver.input_text(BY.type("TextInput"), "hello world", mode=InputTextMode().paste(True).addition(True))
```

### clear_text

```python
def clear_text(component: Union[ISelector, IUiComponent])
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

清空指定控件中的文本内容

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| component | 需要清除文本的控件 |

**返回值**

无返回值描述

**示例**

```python
# 清除类型为"InputText"的控件中的内容
driver.clear_text(BY.type("InputText"))
```

### move_cursor

```python
def move_cursor(direction: str, times: int = 1)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

移动输入框中的光标位置

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| direction | 光标移动的方向, 支持:<br>UiParam.LEFT 向左移动<br>UiParam.RIGHT 向右移动<br>UiParam.UP 向上移动<br>UiParam.DOWN 向下移动<br>UiParam.END 移动到文本尾部<br>UiParam.BEGIN 移动到文本头部 |
| times | 光标移动次数 |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### wait_for_idle

```python
def wait_for_idle(idle_time: float = DEFAULT_IDLE_TIME, timeout: float = DEFAULT_TIMEOUT)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

等待控件进入空闲状态

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| idle_time | UI界面处于空闲状态的持续时间，当UI空闲时间>=idle_time时，该函数返回 |
| timeout | 等待超时时间，如果经过timeout秒后UI空闲时间仍然不满足，则返回 |

**返回值**

无返回值描述

**示例**

```python
# 等待UI界面进入空闲(稳定)状态
driver.wait_for_idle()
# 等待UI界面进入空闲(稳定)状态，空闲时间为0.1秒，最长等待时间(超时时间)为10秒
driver.wait_for_idle(idle_time=0.1, timeout=10)
```

### wait_for_component

```python
def wait_for_component(by: ISelector, timeout: float = DEFAULT_TIMEOUT) -> IUiComponent
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

等待目标控件出现, 如果出现则返回控件对象

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| by | 等待出现的控件, 通过By类指定 |
| timeout | 等待超时时间, 单位秒 |

**返回值**

控件在超时前出现则返回IUiComponent控件对象，否则返回None

**示例**

```python
# 等待id为"confirm_button"的控件出现，超时时间为10秒
driver.wait_for_component(BY.key("confirm_button"), timeout=10)
# 等待id为"confirm_button"的控件出现
driver.wait_for_component(BY.key("confirm_button"))
```

### wait_for_component_disappear

```python
def wait_for_component_disappear(by: ISelector, timeout: float = DEFAULT_TIMEOUT)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

等待控件消失

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| by | 等待消失的控件, 通过By类指定 |
| timeout | 等待超时时间, 单位秒 |

**返回值**

None表示控件消失, 否则返回控件对象IUiComponent表示等待超时控件仍未消失

**示例**

```python
# 等待id为"confirm_button"的控件消失，超时时间为10秒
driver.wait_for_component_disappear(BY.key("confirm_button"), timeout=10)
```

### to_abs_pos

```python
def to_abs_pos(x: float, y: float) -> (int, int)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

根据屏幕分辨率将比例坐标转换为绝对坐标

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| x | 相对x坐标，范围0~1 |
| y | 相对y坐标，范围0~1 |

**返回值**

比例坐标对应的绝对坐标

**示例**

```python
# 将比例坐标(0.1, 0.8)转为屏幕上的绝对坐标
abs_pos = driver.to_abs_pos(0.1, 0.8)
```

### pinch_in

```python
def pinch_in(area: Union[ISelector, IUiComponent, Rect], scale: float = 0.4, direction: str = "diagonal", **kwargs)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

在控件上捏合缩小

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| area | 手势执行的区域 |
| scale | 缩放的比例, [0, 1], 值越小表示缩放操作距离越长, 缩小的越多 |
| direction | 双指缩放时缩放操作方向, 支持<br>"diagonal" 对角线滑动<br>"horizontal" 水平滑动 |
| kwargs | 其他可选滑动配置参数<br>dead_zone_ratio 缩放操作时控件靠近边界不可操作的区域占控件长度/宽度的比例, 默认为0.2, 调节范围为(0, 0.5) |

**返回值**

无返回值描述

**示例**

```python
# 在类型为Image的控件上进行双指捏合缩小操作
driver.pinch_in(BY.type("Image"))
# 在类型为Image的控件上进行双指捏合缩小操作, 设置水平方向捏合
driver.pinch_in(BY.type("Image"), direction="horizontal")
```

### pinch_out

```python
def pinch_out(area: Union[ISelector, IUiComponent, Rect], scale: float = 1.6, direction: str = "diagonal", **kwargs)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

在控件上双指放大

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| area | 手势执行的区域 |
| scale | 缩放的比例, 范围1~2, 值越大表示缩放操作滑动的距离越长, 放大的越多 |
| direction | 双指缩放时缩放操作方向, 支持<br>"diagonal" 对角线滑动<br>"horizontal" 水平滑动 |
| kwargs | 其他可选滑动配置参数<br>dead_zone_ratio 缩放操作时控件靠近边界不可操作的区域占控件长度/宽度的比例, 默认为0.2, 调节范围为(0, 0.5) |

**返回值**

无返回值描述

**示例**

```python
# 在类型为Image的控件上进行双指放大操作
driver.pinch_out(BY.type("Image"))
# 在类型为Image的控件上进行双指捏合缩小操作, 设置水平方向捏合
driver.pinch_out(BY.type("Image"), direction="horizontal")
```

### fling

```python
def fling(direction: str, distance: int = 50, area: Union[ISelector, IUiComponent] = None, speed: str = "fast")
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

执行抛滑操作

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| direction | 滑动方向，目前支持:<br>"LEFT" 左滑<br>"RIGHT" 右滑<br>"UP" 上滑<br>"DOWN" 下滑 |
| distance | 相对滑动区域总长度的滑动距离，范围为1-100, 表示滑动长度为滑动区域总长度的1%到100%， 默认为60 |
| area | 通过控件指定的滑动区域 |
| speed | 滑动速度, 目前支持三档:<br>UiParam.FAST 快速<br>UiParam.NORMAL 正常速度<br>UiParam.SLOW 慢速 |

**返回值**

无返回值描述

**示例**

```python
# 向上抛滑
driver.fling(UiParam.UP)
# 向下慢速抛滑
driver.fling(UiParam.DOWN, speed=UiParam.SLOW)
```

### inject_gesture

```python
def inject_gesture(gesture: Gesture, speed: int = 2000)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

执行自定义滑动手势操作

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| gesture | 描述手势操作的Gesture对象 |
| speed | 默认操作速度, 当生成Gesture对象的某个步骤中没有传入操作时间的默认使用该速度进行操作 |

**返回值**

无返回值描述

**示例**

```python
from hypium import Gesture
# 创建一个gesture对象
gesture = Gesture()
# 获取控件计算器的位置
pos = driver.findComponent(BY.text("计算器")).getBoundsCenter()
# 获取屏幕尺寸
size = driver.getDisplaySize()
# 起始位置, 长按2秒
gesture.start(pos.to_tuple(), 2)
# 移动到屏幕边缘
gesture.move_to(Point(size.X - 20, int(size.Y / 2)).to_tuple())
# 停留2秒
gesture.pause(2)
# 移动到(360, 500)的位置
gesture.move_to(Point(360, 500).to_tuple())
# 停留2秒结束
gesture.pause(2)
# 执行gesture对象描述的操作
driver.inject_gesture(gesture)
```

### mouse_double_click

```python
def mouse_double_click(pos: Union[tuple, IUiComponent, ISelector], button_id: MouseButton = MouseButton.MOUSE_BUTTON_LEFT)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

鼠标双击

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| pos | 点击的位置, 例如(100, 200) |
| button_id | 需要点击的鼠标按键 |

**返回值**

无返回值描述

**示例**

```python
# 使用鼠标左键双击(100, 200)的位置
driver.mouse_double_click((100, 200), MouseButton.MOUSE_BUTTON_LEFT)
# 使用鼠标右键双击文本为"确认"
driver.mouse_double_click(BY.text("确认"), MouseButton.MOUSE_BUTTON_RIGHT)
```

### mouse_long_click

```python
def mouse_long_click(pos: Union[tuple, IUiComponent, ISelector], button_id: MouseButton = MouseButton.MOUSE_BUTTON_LEFT, press_time: float = 1.5)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

鼠标长按(rk板测试未生效)

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| pos | 长按的位置, 例如(100, 200) |
| button_id | 需要点击的鼠标按键 |
| press_time | 长按的时间 |

**返回值**

无返回值描述

**示例**

```python
# 使用鼠标左键长按(100, 200)的位置
driver.mouse_long_click((100, 200), MouseButton.MOUSE_BUTTON_LEFT)
# 使用鼠标右键长按文本为"确认"的控件
driver.mouse_long_click(BY.text("确认"), MouseButton.MOUSE_BUTTON_RIGHT)
# 使用鼠标右键长按比例坐标(0.8, 0.5)的位置
driver.mouse_long_click((0.8, 0.5), MouseButton.MOUSE_BUTTON_RIGHT)
```

### mouse_click

```python
def mouse_click(pos: Union[tuple, IUiComponent, ISelector], button_id: MouseButton = MouseButton.MOUSE_BUTTON_LEFT, key1: Union[KeyCode, int] = None, key2: Union[KeyCode, int] = None)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

鼠标点击, 支持键鼠组合操作

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| pos | 点击的位置, 支持位置, IUiComponent对象以及By, 例如(100, 200), BY.text("确认") |
| button_id | 需要点击的鼠标按键 |
| key1 | 需要组合按下的第一个键盘按键 |
| key2 | 需要组合按下的第二个键盘按键 |

**返回值**

无返回值描述

**示例**

```python
# 使用鼠标左键点击(100, 200)的位置
driver.mouse_long_click((100, 200), MouseButton.MOUSE_BUTTON_LEFT)
# 使用鼠标右键点击文本为"确认"的控件
driver.mouse_long_click(BY.text("确认"), MouseButton.MOUSE_BUTTON_RIGHT)
# 使用鼠标右键点击比例坐标(0.8, 0.5)的位置
driver.mouse_long_click((0.8, 0.5), MouseButton.MOUSE_BUTTON_RIGHT)
```

### mouse_scroll

```python
def mouse_scroll(pos: Union[tuple, IUiComponent, ISelector], scroll_direction: str, scroll_steps: int, key1: int = None, key2: int = None, **kwargs)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

鼠标滚动, 支持键鼠组合操作

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| pos | 滚动的位置, 例如(100, 200) |
| scroll_direction | 滚动方向<br>"up" 向上滚动<br>"down" 向下滚动 |
| scroll_steps | 滚动的鼠标格数 |
| key1 | 需要组合按下的第一个键盘按键 |
| key2 | 需要组合按下的第二个键盘按键 |

**返回值**

无返回值描述

**示例**

```python
# 鼠标滚轮在(100, 200)的位置向下滚动10格
driver.mouse_scroll((100, 200), UiParam.DOWN, scroll_steps=10)
# 鼠标滚轮在类型为Scroll的控件上向上滚动10格
driver.mouse_scroll(BY.type("Scroll"), UiParam.UP, scroll_steps=10)
# 按住ctrl键, 鼠标滚轮在类型为Scroll的控件上向上滚动10格
driver.mouse_scroll(BY.type("Scroll"), UiParam.UP, scroll_steps=10, key1=KeyCode.CTRL_LEFT)
# 按住ctrl和shift键, 鼠标滚轮在类型为Scroll的控件上向上滚动10格
driver.mouse_scroll(BY.type("Scroll"), UiParam.UP, scroll_steps=10, key1=KeyCode.CTRL_LEFT,
key2=KeyCode.SHIFT_LEFT)
```

### mouse_move_to

```python
def mouse_move_to(pos: Union[tuple, IUiComponent, ISelector])
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

鼠标指针移动到指定位置

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| pos | 鼠标指针的位置, 例如(100, 200) |

**返回值**

无返回值描述

**示例**

```python
# 鼠标移动到(100, 200)的位置
driver.mouse_move_to((100, 200))
# 鼠标移动到文本为"查看"的控件
driver.mouse_move_to(BY.text("查看"))
# 鼠标移动到比例坐标(0.8, 0.5)的位置
driver.mouse_long_click((0.8, 0.5))
```

### mouse_move

```python
def mouse_move(start: Union[tuple, IUiComponent, ISelector], end: Union[tuple, IUiComponent, ISelector], speed: int = 3000)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

鼠标指针从之前起始位置移动到结束位置，模拟移动轨迹和速度

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| start | 起始位置, 支持坐标和控件 |
| end | 结束位置, 支持坐标和控件 |
| speed | 鼠标移动速度，像素/秒 |

**返回值**

无返回值描述

**示例**

```python
# 鼠标从控件1移动到控件2
driver.mouse_move(BY.text("控件1"), BY.text("控件2"))
```

### mouse_drag

```python
def mouse_drag(start: Union[tuple, IUiComponent, ISelector], end: Union[tuple, IUiComponent, ISelector], speed: int = 3000)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

使用鼠标进行拖拽操作(按住鼠标左键移动鼠标)

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| start | 起始位置, 支持坐标和控件 |
| end | 结束位置, 支持坐标和控件 |
| speed | 鼠标移动速度，像素/秒 |

**返回值**

无返回值描述

**示例**

```python
# 鼠标从控件1拖拽到控件2
driver.mouse_drag(BY.text("控件1"), BY.text("控件2"))
```

### swipe_to_home

```python
def swipe_to_home(times: int = 1)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

屏幕低端上滑回到桌面

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| times | 上滑次数, 默认1次, 某些场景可能需要两次上滑才能返回桌面 |

**返回值**

无返回值描述

**示例**

```python
# 上滑返回桌面
driver.swipe_to_home()
# 连续上滑2次返回桌面
driver.swipe_to_home(times=2)
```

### swipe_to_back

```python
def swipe_to_back(side=UiParam.RIGHT, times: int = 1, height: float = 0.5)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

滑动屏幕右侧返回

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| side | 滑动的位置, "RIGHT"表示在右边滑动返回，"LEFT"表示在左边滑动返回 |
| times | 上滑次数, 默认1次, 某些场景可能需要两次上滑才能返回桌面 |
| height | 滑动位置在屏幕中Y轴的比例高度(从屏幕顶部开始计算) |

**返回值**

无返回值描述

**示例**

```python
# 侧滑返回
driver.swipe_to_back()
# 侧滑2次返回
driver.swipe_to_back(times=2)
# 设置侧滑位置的高度比例为屏幕高度的80%，即在屏幕靠下的位置侧滑返回
driver.swipe_to_back(height=0.8)
```

### swipe_to_recent_task

```python
def swipe_to_recent_task()
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

屏幕底端上滑停顿, 打开多任务界面

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

无返回值描述

**示例**

```python
# 上滑停顿进度多任务界面
driver.swipe_to_recent_task()
```

### check_current_window

```python
def check_current_window(title: str = None, bundle_name: str = None)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

检查当前活动的窗口的属性是否符合预期

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| title | 预期的窗口标题, None表示不检查 |
| bundle_name | 预期窗口所属的app包名, None表示不检查 |

**返回值**

无返回值描述

**示例**

```python
# 检查当前活动窗口的标题为"畅连"
driver.check_current_window(title="畅连")
# 检查当前活动窗口对应的应用包名为"com.huawei.hmos.settings"
driver.check_current_window(bundle_name="com.huawei.hmos.settings")
```

### check_window

```python
def check_window(window: WindowFilter, title: str = None, bundle_name: str = None)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

检查指定的window的属性是否符合预期

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| title | 预期的窗口标题, None表示不检查 |
| bundle_name | 预期窗口所属的app包名, None表示不检查 |

**返回值**

无返回值描述

**示例**

```python
# 检查当前焦点窗口的包名为com.huawei.hmos.settings
driver.check_window(WindowFilter().focused(True), bundle_name="com.huawei.hmos.settings")
```

### check_component_exist

```python
def check_component_exist(component: ISelector, expect_exist: bool = True, wait_time: int = 0, scroll_target: Union[ISelector, IUiComponent] = None)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

检查指定UI控件是否存在

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| component | 待检查的UI控件, 使用By对象指定 |
| expect_exist | 是否期望控件存在, True表示期望控件存在，False表示期望控件不存在 |
| wait_time | 检查过程中等待控件出现的时间 |
| scroll_target | 上下滑动检查目标控件时滑动的控件, 默认为None表示不进行滑动查找 |

**返回值**

无返回值描述

**示例**

```python
# 检查类型为Button的控件存在
driver.check_component_exist(BY.type("Button"))
# 检查类型为Button的控件存在，如果不存在等待最多5秒
driver.check_component_exist(BY.type("Button"), wait_time=5)
# 在类型为Scroll的控件上滚动检查文本为"hello"的控件存在
driver.check_component_exist(BY.text("hello"), scroll_target=BY.type("Scroll"))
# 检查文本为确认的控件不存在
driver.check_component_exist(BY.text("确认"), expect_exist=False)
```

### check_component

```python
def check_component(component: Union[ISelector, IUiComponent], expected_equal: bool = True, **kwargs)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

检查控件属性是否符合预期

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| component | 需要检查的控件, 支持By或者IUiComponent对象 |
| expected_equal | 预期值和实际值是否相等，True表示预期相等，False表示预期不相等 |
| kwargs | 指定预期的控件属性值, 目前支持:<br>"id", "text", "key", "type", "enabled", "focused", "clickable", "scrollable"<br>"checked", "checkable" |

**返回值**

无返回值描述

**示例**

```python
# 检查id为xxx的控件的checked属性为True
driver.check_component(BY.key("xxx"), checked=True)
# 检查id为check_button的按钮enabled属性为True
driver.check_component(BY.key("checked_button"), enabled=True)
# 检查id为container的控件文本内容为正在检查
driver.check_component(BY.key("container"), text="正在检查")
# 检查id为container的控件文本内容不为空
driver.check_component(BY.key("container"), text="", expect_equal=False)
```

### check_window_exist

```python
def check_window_exist(window: WindowFilter, expect_exist: bool = True)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

检查指定的window是否存在

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| window | 待检查的窗口选择器 |
| expect_exist | 是否期望窗口存在, True表示期望窗口存在，False表示期望窗口不存在 |

**返回值**

无返回值描述

**示例**

```python
# 检查包名为com.huawei.hmos.settings的窗口存在
driver.check_window_exist(WindowFilter().bundle_name("com.huawei.hmos.settings"))
# 检查标题为畅连的窗口不存在
driver.check_window_exist(WindowFilter().title("畅联"), expect_exist=False)
# 检查包名为com.huawei.hmos.settings, 标题为设置的窗口存在
driver.check_window_exist(WindowFilter().title("设置").bundle_name("com.huawei.hmos.settings"))
```

### check_image_exist

```python
def check_image_exist(image_path_pc: str, expect_exist: bool = True, similarity: float = 0.95, timeout: int = 3, mode="template", **kwargs)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

使用图片模板匹配算法检测当前屏幕截图中是否有指定图片，需要保证模板图片的分辨率和屏幕截图中目标图像的
分辨率一致，否则会无法成功检测到目标图片

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| image_path_pc | 待检查的图片路径（图片保存在PC端） |
| expect_exist | 是否期望图片在设备屏幕上存在, True表示期望控件存在，False表示期望控件不存在 |
| similarity | 图像匹配算法比较图片时使用的相似度, 范围0~1, |
| timeout | 检查的总时间，每秒会进行获取一次屏幕截图检查指定图片是否存在，通过timeout可指定检查的次数 |
| mode | 图片匹配模式, 支持template和sift, 图片分辨率/旋转变化对sift模式影响相对较小，但sift模式难以处理缺少较复杂图案<br>的纯色，无线条图片 |
| kwargs | 其他配置参数<br>min_match_point: 最少匹配特征点数, 值越大匹配越严格, 默认为16, 仅sift模式有效 |

**返回值**

无返回值描述

**示例**

```python
# 检查图片存在
driver.check_image_exist("test.jpeg")
# 检查图片不存在
driver.check_image_exist("test.jpeg", expect_exist=False)
# 检查图片存在, 图片相似度要求95%, 重复检查时间5秒
driver.check_image_exist("test.jpeg", timeout=5, similarity=0.95)
# 检查图片不存在, 重复检查时间5秒
driver.check_image_exist("test.jpeg", timeout=5, expect_exist=False)
# 使用sift算法检查图片存在, 设置最少匹配特征点数量为16
driver.check_image_exist("test.jpeg", mode="sift", min_match_point=16)
```

### start_listen_toast

```python
def start_listen_toast()
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

开启新的toast监听, 需要配合get_latest_toast使用
(该操作会清理上次记录的toast消息, 保证get_latest_toast获取本次listen_toast之后产生的toast消息)

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

无返回值描述

**示例**

```python
# 开启Toast监听
driver.start_listen_toast()
# 执行操作
driver.touch(BY.text("发送"))
# 返回上次开启监听后最新的一条toast消息，如果没有消息则等待最多5秒直到新toast出现, 返回该toast的文本
text_in_toast = driver.get_latest_toast(time_out=5)
# 断言text_in_toast等于"发送成功"
host.check_equal(text_in_toast, "发送成功")
```

### get_latest_toast

```python
def get_latest_toast(timeout: float = 3) -> str
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

读取最近一段时间内最新的一条toast消息内容

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| timeout | 没有满足的toast出现时，等待toast出现的最长时间，单位为秒 |

**返回值**

toast消息的文本内容, 如果没有满足的toast消息则返回空字符串""

**示例**

```python

# 开启Toast监听
driver.start_listen_toast()
# 执行操作
driver.touch(BY.text("发送"))
# 返回上次开启监听后最新的一条toast消息，如果没有消息则等待最多5秒直到新toast出现, 返回该toast的文本
text_in_toast = driver.get_latest_toast(timeout=5)
# 检查text_in_toast等于发送成功
host.check_equal(text_in_toast, "发送成功")
```

### check_toast

```python
def check_toast(expect_text: str, fuzzy: str = 'equal', timeout: int = 3)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

检查最新的一条toast消息内容

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| expect_text | 期望的toas文本内容 |
| fuzzy | 模糊匹配方式<br>"equal: 全等匹配<br>"starts_with" 匹配开头<br>"ends_with" 匹配结尾<br>"contains" 匹配包含(实际toast消息包含期望文本) |
| timeout | 没有满足的toast出现时，等待toast出现的最长时间，单位为秒 |

**返回值**

无返回值描述

**示例**

```python

# 开启Toast监听
driver.start_listen_toast()
# 执行操作
driver.touch(BY.text("发送"))
# 检查toast
driver.check_toast("发送成功")
```

### start_listen_ui_event

```python
def start_listen_ui_event(event_type: str)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

开始ui事件监听
(该操作会清理上次记录的toast消息, 保证get_latest_ui_event获取开始监听后产生的最新ui事件)

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| event_type | ui事件类型, 目前支持<br>toastShow toast消息出现<br>dialogShow 对话框出现 |

**返回值**

无返回值描述

**示例**

```python
# 开启toast消息事件监听
driver.start_listen_ui_event("toastShow")
# 开启对话框出现事件监听
driver.start_listen_ui_event("dialogShow")
```

### get_latest_ui_event

```python
def get_latest_ui_event(timeout: float = 3) -> dict
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

读取开始监听ui事件后最新出现的UI事件

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

ui事件信息, 例如:
dialogShow 事件 {"bundleName":"com.uitestScene.acts","text":"dialogShow","type":"AlertDialog"}
toastShow 事件 {"bundleName":"com.uitestScene.acts","text":"toastShow","type":"Toast"}
没有事件返回None

**示例**

```python
# 开启对话框出现(dialogShow)事件监听
driver.start_listen_ui_event("dialogShow")
# 点击发送
driver.touch(BY.text("发送"))
# 读取ui事件，如果没有ui事件则等待最多5秒直到有ui事件出现, 返回ui事件信息
ui_event = driver.get_latest_ui_event(timeout=5)
```

### inject_multi_finger_gesture

```python
def inject_multi_finger_gesture(gestures: List[Gesture], speed: int = 2000)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

注入多指手势操作

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| gestures | 表示单指手势操作的Gesture对象列表，每个Gesture对象描述一个手指的操作轨迹。<br>注意如果各个手势持续时间不同，时间短的手势操作会保持在结束位置，等待所有手势完成后抬起对应手指。 |
| speed | Gesture对象的步骤没有设置执行时间时, 使用该速度计算时间, 单位像素/秒 |

**返回值**

无返回值描述

**示例**

```python
# 导入Gesture对象
from hypium import Gesture
# 创建手指1的手势, 从(0.4, 0.4)的位置移动到(0.2, 0.2)的位置
gesture1 = Gesture().start((0.4, 0.4)).move_to((0.2, 0.2), interval=1)
# 创建手指2的手势, 从(0.6, 0.6)的位置移动到(0.8, 0.8)的位置
gesture2 = Gesture().start((0.6, 0.6)).move_to((0.8, 0.8), interval=1)
# 注入多指操作
driver.inject_multi_finger_gesture((gesture1, gesture2))
```

### two_finger_swipe

```python
def two_finger_swipe(start1: tuple, end1: tuple, start2: tuple, end2: tuple, duration: float = 0.5, area: Rect = None)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

执行双指滑动操作

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| start1 | 手指1起始坐标 |
| end1 | 手指1起始坐标 |
| start2 | 手指2起始坐标 |
| end2 | 手指2结束坐标 |
| duration | 滑动操作持续时间 |
| area | 滑动操作的区域, 当起始结束坐标为(0.1, 0.2)等相对比例坐标时生效，默认为操作区域为全屏 |

**返回值**

无返回值描述

**示例**

```python
# 执行双指滑动操作, 手指1从(0.4, 0.4)滑动到(0.2, 0.2), 手指2从(0.6, 0.6)滑动到(0.8, 0.8)
driver.two_finger_swipe((0.4, 0.4), (0.2, 0.2), (0.6, 0.6), (0.8, 0.8))
# 执行双指滑动操作, 手指1从(0.4, 0.4)滑动到(0.2, 0.2), 手指2从(0.6, 0.6)滑动到(0.8, 0.8), 持续时间3秒
driver.two_finger_swipe((0.4, 0.4), (0.2, 0.2), (0.6, 0.6), (0.8, 0.8), duration=3)
# 查找Image类型控件
comp = driver.find_component(BY.type("Image"))
# 在指定的控件区域内执行双指滑动(滑动起始/停止坐标为控件区域内的比例坐标)
driver.two_finger_swipe((0.4, 0.4), (0.1, 0.1), (0.6, 0.6), (0.9, 0.9), area=comp.getBounds())
```

### multi_finger_touch

```python
def multi_finger_touch(points: List[tuple], duration: float = 0.1, area: Rect = None)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

执行多指点击操作

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| points | 需要点击的坐标位置列表，每个坐标对应一个手指, 例如[(0.1, 0.2), (0.3, 0.4)], 最多支持4指点击 |
| duration | 按下/抬起的时间，可实现多指长按操作, 单位秒 |
| area | 点击操作的区域, 当起始结束坐标为(0.1, 0.2)等相对比例坐标时生效，默认为操作区域为全屏 |

**返回值**

无返回值描述

**示例**

```python
# 执行多指点击操作, 同时点击屏幕(0.1， 0.2), (0.3, 0.4)的位置
driver.multi_finger_touch([(0.1， 0.2), (0.3, 0.4)])
# 执行多指点击操作, 设置点击按下时间为1秒
driver.multi_finger_touch([(0.1， 0.2), (0.3, 0.4)], duration=2)
# 查找Image类型控件
comp = driver.find_component(BY.type("Image"))
# 在指定的控件区域内执行多指点击(点击坐标为控件区域内的比例坐标)
driver.multi_finger_touch([(0.5, 0.5), (0.6, 0.6)], area=comp.getBounds())
```

### pen_click

```python
def pen_click(target: Union[ISelector, IUiComponent, tuple], offset: tuple = None)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

模拟触控笔点击

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| target | 点击操作目标 |
| offset | 点击坐标在操作目标中的偏移坐标 |

**返回值**

无返回值描述

**示例**

```python
# 触控笔点击蓝牙控件
driver.pen_click(BY.text("蓝牙"))
# 触控笔点击蓝牙控件左上角(偏移0, 0)
driver.pen_click(BY.text("蓝牙"), offset=(0, 0))
# 触控笔点击蓝牙控件中偏移为0.8, 0.8的位置
driver.pen_click(BY.text("蓝牙"), offset=(0.8, 0.8))
# 触控笔点击蓝牙控件正上方, 同蓝牙控件距离为蓝牙控件高度的80%的位置(0.5, -0.8)
driver.pen_click(BY.text("蓝牙"), offset=(0.5, -0.8))
```

### pen_double_click

```python
def pen_double_click(target: Union[ISelector, IUiComponent, tuple], offset: tuple = None)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

模拟触控笔双击

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| target | 点击操作目标 |
| offset | 点击坐标在操作目标中的偏移坐标 |

**返回值**

无返回值描述

**示例**

```python
# 触控笔双击蓝牙控件
driver.pen_double_click(BY.text("蓝牙"))
# 触控笔双击蓝牙控件左上角(偏移0, 0)
driver.pen_double_click(BY.text("蓝牙"), offset=(0, 0))
# 触控笔双击蓝牙控件中偏移为0.8, 0.8的位置
driver.pen_double_click(BY.text("蓝牙"), offset=(0.8, 0.8))
```

### pen_long_click

```python
def pen_long_click(target: Union[ISelector, IUiComponent, tuple], offset: tuple = None, pressure: float = None)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

模拟触控笔长按

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| target | 点击操作目标 |
| offset | 点击坐标在操作目标中的偏移坐标 |
| pressure | 触控笔压力值, 范围[0, 1] |

**返回值**

无返回值描述

**示例**

```python
# 触控笔长按蓝牙控件
driver.pen_long_click(BY.text("蓝牙"))
# 触控笔长按蓝牙控件左上角(偏移0, 0)
driver.pen_long_click(BY.text("蓝牙"), offset=(0, 0))
# 触控笔长按蓝牙控件中偏移为0.8, 0.8的位置
driver.pen_long_click(BY.text("蓝牙"), offset=(0.8, 0.8))
```

### pen_swipe

```python
def pen_swipe(direction: str, distance: int = 60, start_point: tuple = None, area: Union[ISelector, IUiComponent, Rect] = None, pressure: float = None, duration: float = DEFAULT_SLIDE_TIME, speed: int = None)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

在屏幕上或者指定区域area中执行朝向指定方向direction的触控笔滑动操作。该接口用于执行不太精准的滑动操作。

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| direction | 滑动方向，目前支持:<br>"LEFT" 左滑<br>"RIGHT" 右滑<br>"UP" 上滑<br>"DOWN" 下滑 |
| distance | 相对滑动区域总长度的滑动距离，范围为1-100, 表示滑动长度为滑动区域总长度的1%到100%， 默认为60 |
| area | 通过控件指定的滑动区域 |
| start_point | 滑动起始点, 默认为None, 表示在区域中间位置执行滑动操作, 可以传入滑动起始点坐标，支持使用(0.5, 0.5)<br>这样的比例坐标。 |
| pressure | 触控笔压力值, 范围[0, 1] |
| duration | 滑动时长, 单位秒, 默认0.3秒, 同时指定滑动时长和速度时, 仅速度生效 |
| speed | 滑动速度, 单位px/s, 同时指定滑动时长和速度时, 仅速度生效 |

**返回值**

无返回值描述

**示例**

```python
# 在屏幕上向上滑动, 距离40
driver.pen_swipe(UiParam.UP, distance=40)
# 在屏幕上向右滑动, 滑动时间为0.1秒
driver.pen_swipe(UiParam.RIGHT, duration=0.1)
# 在屏幕起始点为比例坐标为(0.8, 0.8)的位置向上滑动，距离30
driver.pen_swipe(UiParam.UP, 30, start_point=(0.8, 0.8))
# 在类型为Scroll的控件中向向滑动
driver.pen_swipe(UiParam.UP, area=BY.type("Scroll"))
# 在指定区域上滑, 指定速度为3000px/s
driver.pen_swipe(UiParam.UP, area=BY.type("Scroll"), speed=3000)
```

### pen_slide

```python
def pen_slide(start: Union[ISelector, IUiComponent, tuple], end: Union[ISelector, IUiComponent, tuple], area: Union[ISelector, IUiComponent, Rect] = None, pressure: float = None, duration: float = DEFAULT_SLIDE_TIME, speed: int = None)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

根据指定的起始和结束位置执行触控笔滑动操作，起始和结束的位置可以为控件或者屏幕坐标。该接口用于执行较为精准的滑动操作。

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| start | 滑动起始位置，可以为控件BY.text("滑块")或者坐标(100, 200), 或者使用find_component找到的控件对象 |
| end | 滑动结束位置，可以为控件BY.text("最大值")或者坐标(100, 200), 或者使用find_component找到的控件对象 |
| area | 滑动操作区域，可以为控件BY.text("画布")。目前仅在start或者end为坐标<br>时生效，指定区域后，当start和end为坐标时，其坐标将被视为相对于指定的区域<br>的相对位置坐标。 |
| pressure | 触控笔压力值, 范围[0, 1] |
| duration | 滑动时长, 单位秒, 默认0.3秒, 同时指定滑动时长和速度时, 仅速度生效 |
| speed | 滑动速度, 同时指定滑动时长和速度时, 仅速度生效 |

**返回值**

无返回值描述

**示例**

```python
# 从类型为Slider的控件滑动到文本为最大的控件
driver.pen_slide(BY.type("Slider"), BY.text("最大"))
# 从坐标100, 200滑动到300，400
driver.pen_slide((100, 200), (300, 400))
# 从坐标100, 200滑动到300，400, 滑动时间为1秒
driver.pen_slide((100, 200), (300, 400), duration=1)
# 在类型为Slider的控件上从(0, 0)滑动到(100, 0)
driver.pen_slide((0, 0), (100, 0), area = BY.type("Slider))
```

### pen_drag

```python
def pen_drag(start: Union[ISelector, IUiComponent, tuple], end: Union[ISelector, IUiComponent, tuple], area: Union[ISelector, IUiComponent, Rect] = None, pressure: float = None, press_time: float = 1.5, duration: float = 1, speed: int = None)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

根据指定的起始和结束位置执行触控笔拖拽操作，起始和结束的位置可以为控件或者屏幕坐标

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| start | 拖拽起始位置，可以为控件BY.text("滑块")或者坐标(100, 200), 或者使用find_component找到的控件对象 |
| end | 拖拽结束位置，可以为控件BY.text("最大值")或者坐标(100, 200), 或者使用find_component找到的控件对象 |
| area | 拖拽操作区域，可以为控件BY.text("画布"), 或者使用find_component找到的控件对象。<br>目前仅在start或者end为坐标时生效，指定区域后，当start和end为坐标时，其坐标将被视为相对于指定的区域<br>的相对位置坐标。 |
| pressure | 触控笔压力值, 范围[0, 1] |
| press_time | 拖拽操作开始时，长按的时间, 默认为1.5秒 |
| duration | 拖拽操作中滑动时长, 单位秒, 默认1秒, 同时指定滑动时长和速度时, 仅速度生效 |
| speed | 拖拽过程中滑动速度, 同时指定滑动时长和速度时, 仅速度生效 |

**返回值**

无返回值描述

**示例**

```python
# 拖拽文本为"文件.txt"的控件到文本为"上传文件"的控件
driver.pen_drag(BY.text("文件.txt"), BY.text("上传文件"))
# 拖拽id为"start_bar"的控件到坐标(100, 200)的位置, 拖拽时间为2秒
driver.pen_drag(BY.key("start_bar"), (100, 200), duration=2)
# 在id为"Canvas"的控件上从相对位置(10, 20)拖拽到(100, 200)
driver.pen_drag((10, 20), (100, 200), area=BY.id("Canvas"))
# 在滑动条上从相对位置(10, 10)拖拽到(10, 200)
driver.pen_drag((10, 10), (10, 200), area=BY.type("Slider"))
```

### pen_inject_gesture

```python
def pen_inject_gesture(gesture: Gesture, pressure: float = None, speed: int = None)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

模拟触控笔自定义手势

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| gesture | 触控笔自定义手势 |
| pressure | 触控笔压力值, 范围[0, 1] |
| speed | 移动速度, 单位px/s, 当gesture中未指定操作时长是生效, 默认600px/s |

**返回值**

无返回值描述

**示例**

```python
# 模拟注入触控笔滑动操作
gesture = Gesture()
# 在(0.5, 0.5)位置按下
gesture.start((0.5, 0.5))
# 移动到(0.8, 0.8)的位置
gesture.move_to((0.8, 0.8))
# 停顿1秒
gesture.pause()
# 注入操作
driver.pen_inject_gesture(gesture)
```

### touchpad_swipe

```python
def touchpad_swipe(direction: str, fingers=3, speed=None)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

模拟PC触控板滑动后手势

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| direction | 滑动方向, 支持<br>UiParam.LEFT<br>UiParam.RIGHT<br>UiParam.UP<br>UiParam.DOWN |
| fingers | 滑动手指数量, 仅支持3指和4指 |
| speed | 滑动速度 |

**返回值**

无返回值描述

**示例**

```python
# 触控板三指上滑后停顿
driver.touchpad_swipe_and_hold(UiParam.UP, fingers=3)
```

### touchpad_swipe_and_hold

```python
def touchpad_swipe_and_hold(direction: str, fingers=3, speed=None)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

模拟PC触控板滑动后停顿手势

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| direction | 滑动方向, 支持<br>UiParam.LEFT<br>UiParam.RIGHT<br>UiParam.UP<br>UiParam.DOWN |
| fingers | 滑动手指数量, 仅支持3指和4指 |
| speed | 滑动速度 |

**返回值**

无返回值描述

**示例**

```python
# 触控板三指上滑后停顿
driver.touchpad_swipe_and_hold(UiParam.UP, fingers=3)
```

### click

```python
def click(target: Union[ISelector, IUiComponent, tuple], offset=None)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

模拟点击操作

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| target | 点击操作目标 |
| offset | 点击坐标在目标控件区域的偏移值, 不设置时默认为(0.5, 0.5), 表示控件中心。支持设置范围是0到1<br>如(0.1, 0.1)表示点击目标左上角为坐标原点x方向10%, y方向10%的位置 |

**返回值**

无返回值描述

**示例**

```python
# 点击蓝牙控件
driver.click(BY.text("蓝牙"))
# 点击蓝牙控件左上角(偏移0, 0)
driver.click(BY.text("蓝牙"), offset=(0, 0))
# 点击蓝牙控件中偏移为0.8, 0.8的位置
driver.click(BY.text("蓝牙"), offset=(0.8, 0.8))
# 点击蓝牙控件正上方, 同蓝牙控件距离为蓝牙控件高度的80%的位置(0.5, -0.8)
driver.click(BY.text("蓝牙"), offset=(0.5, -0.8))
```

### double_click

```python
def double_click(target: Union[ISelector, IUiComponent, tuple], offset=None)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

模拟点击操作

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| target | 点击操作目标 |
| offset | 点击坐标在目标控件区域的偏移值, 不设置时默认为(0.5, 0.5), 表示控件中心。支持设置范围是0到1<br>如(0.1, 0.1)表示点击目标左上角为坐标原点x方向10%, y方向10%的位置 |

**返回值**

无返回值描述

**示例**

```python
# 点击蓝牙控件
driver.double_click(BY.text("测试按钮"))
# 点击蓝牙控件左上角(偏移0, 0)
driver.double_click(BY.text("测试按钮"), offset=(0, 0))
```

### long_click

```python
def long_click(target: Union[ISelector, IUiComponent, tuple], press_time: float = 2, offset=None)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

执行长按操作, 可以指定长按时间

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| target | 需要点击的目标，可以为控件查找条件, 控件对象或者屏幕坐标(通过tuple类型指定，<br>例如(100, 200)， 其中100为x轴坐标，200为y轴坐标), 或者使用find_component找到的控件对象 |
| press_time | 长按持续时间 |
| offset | 点击坐标在目标控件区域的偏移值, 不设置时默认为(0.5, 0.5), 表示控件中心。支持设置范围是0到1<br>如(0.1, 0.1)表示点击目标左上角为坐标原点x方向10%, y方向10%的位置 |

**返回值**

无返回值描述

**示例**

```python
# 长按文本为"按钮"的控件5秒
driver.long_click(BY.text("按钮"), press_time=5)
# 长按(100, 200)的位置5秒
driver.long_click((100, 200), press_time=5)
# 长按文本为"设置"的控件左上角(偏移0, 0)
driver.long_click(BY.text("设置"), offset=(0, 0))
```

### input_text_on_current_cursor

```python
def input_text_on_current_cursor(text: str)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

在光标处输入文本, 该参数需要设备API level >= 20支持

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| text | 输入的文本 |

**返回值**

无返回值描述

**示例**

```python
# 在光标位置输入你好
driver.input_text_on_current_cursor("你好")
```

### rotate_crown

```python
def rotate_crown(steps: int, speed: int = None)
```

**归属模块**: `hypium.action.device.uidriver`

**归属类**: `UiDriver`

**类型**: 函数

**描述**

模拟表冠旋转

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| steps | 旋转的步数, 正数表示顺时针旋转, 负数表示逆时针旋转 |
| speed | 旋转速度, 范围[1, 500], 默认为20<br>driver.rotate_crown(50)<br>表冠顺时针旋转50步<br>driver.rotate_crown(-50)<br>表冠顺时针旋转50步, 速度设置为60<br>driver.rotate_crown(50, speed=60) |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

# hypium.action.host.cv

**类型**: `module`

## CV

**类型**: `class`

**描述**

图像处理相关操作, 例如图片查找,裁剪,压缩,相似度对比, 清晰度计算等

**导入方式**

```python
from hypium.action.host.cv import CV
```

### imread

```python
def imread(file_path: str)
```

**归属模块**: `hypium.action.host.cv`

**归属类**: `CV`

**类型**: 函数

**描述**

读取一个图片, 返回OpenCV格式的图片对象, 支持中文路径

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

图片对象(numpy数组)

**示例**

```python
img = CV.imread("/path/to/image.jpeg")
```

### imwrite

```python
def imwrite(img, filepath: str, quality: int = 80)
```

**归属模块**: `hypium.action.host.cv`

**归属类**: `CV`

**类型**: 函数

**描述**

以jpeg格式保存一张图片, 支持中文路径

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| img | 图片对象(numpy数组) |
| filepath | 保存图片的路径 |
| quality | jpeg图像质量, 范围0~100, 数值越小图像质量越低，图片占用空间越小 |

**返回值**

无返回值描述

**示例**

```python
img = CV.imwrite("/path/to/image.jpeg")
```

### compress_image

```python
def compress_image(img_path: str, ratio: float = 0.5, quality=80, out_img_path: str = None)
```

**归属模块**: `hypium.action.host.cv`

**归属类**: `CV`

**类型**: 函数

**描述**

压缩图像, 保存为jpeg格式

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| img_path | 需要压缩的图片地址 |
| ratio | 分辨率压缩比例范围0~1, 数值越小输出分辨率越低, 图片占用空间越小 |
| quality | jpeg图像质量, 范围0~100, 数值越小图像质量越低，图片占用空间越小 |
| out_img_path | 输出图片路径, 当设置为None时使用img_path作为输出图片路径，即在原图片上修改 |

**返回值**

无返回值描述

**示例**

```python
# 压缩图片, 修改原图片
CV.compress_image("/path/to/image.jpeg")
# 压缩图片, 修改原图片
CV.compress_image("/path/to/image.jpeg", out_img_path="/path/to/save_image.jpeg")
```

### crop_image

```python
def crop_image(img_path: str, area: Rect, out_img_path: str = None)
```

**归属模块**: `hypium.action.host.cv`

**归属类**: `CV`

**类型**: 函数

**描述**

裁剪图片

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| img_path | 需要裁剪的图片路径 |
| area | 裁剪后保留的区域, 使用Rect类型指定 |
| out_img_path | 输出图片路径, 如果为None表示在原图上修改 |

**返回值**

无返回值描述

**示例**

```python
# 裁剪图片，保留指定区域，原图修改
CV.crop_image("/path/to/image.jpeg", Rect(left=10, right=100, top=10, bottom=100))
# 裁剪图片，保留指定区域，保存到新图片
CV.crop_image("/path/to/image.jpeg", Rect(left=10, right=100, top=10, bottom=100),
out_img_path=/path/to/new.jpeg")
```

### find_image

```python
def find_image(target_image_path: str, background_image_path: str, mode: str = "sift", **kwargs) -> Rect
```

**归属模块**: `hypium.action.host.cv`

**归属类**: `CV`

**类型**: 函数

**描述**

在backgound_image_path对应的图片中查找target_image_path对应的图片位置

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| target_image_path | 需要查找图片路径(查找的目标) |
| background_image_path | 背景图片路径(查找的范围) |
| mode | 图片匹配模式, 支持template和sift, 图片分辨率/旋转变化对sift模式影响相对较小，但sift模式难以处理缺少较复杂图案<br>的纯色，无线条图片 |
| kwargs | 其他配置参数<br>min_match_point: sift模式支持, 最少匹配特征点数, 值越大匹配越严格, 默认为16<br>similarity: template模式支持，图片最小相似度 |

**返回值**

无返回值描述

**示例**

```python
# 在"background.jpeg"中查找"target.jpeg"
image_bounds = CV.find_image("target.jpeg", "background.jpeg")
```

### compare_image

```python
def compare_image(image_path_a: str, image_path_b: str, mode: str = "template", with_color: bool = False) -> float
```

**归属模块**: `hypium.action.host.cv`

**归属类**: `CV`

**类型**: 函数

**描述**

比较两张图片的相似度

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| image_path_a | 第一张图片 |
| image_path_b | 第二张图片 |
| mode | 比较算法, "template" 表示相关系数算法比较, "sift"表示特征点算法比较 |

**返回值**

图片相似度0~1,, 数字越大相似度越高

**示例**

```python
# 比较image1.jpeg和image2.jpeg的相似度
similarity = CV.compare_image("/path/to/image1.jpeg", "/path/to/image2.jpeg")
```

### calculate_clarity

```python
def calculate_clarity(image_path: str) -> float
```

**归属模块**: `hypium.action.host.cv`

**归属类**: `CV`

**类型**: 函数

**描述**

计算图像的清晰度(通过检测图像中物体轮廓清晰度实现, 无法用于纯色的图片)

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| image_path | 需处理的图片路径 |

**返回值**

代表图像清晰度的数值, 值越大表示图像越清晰, 内容不同的图片使用该方法计算出的清晰度
不具备绝对的可比性, 内容相同的图片计算出的清晰度具有可比性。

**示例**

```python
# 计算图片清晰度
clarity = CV.calculate_clarity("/path/to/image.jpeg")
```

### calculate_brightness

```python
def calculate_brightness(image_path: str)
```

**归属模块**: `hypium.action.host.cv`

**归属类**: `CV`

**类型**: 函数

**描述**

计算图像的平均亮度

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| image_path | 需处理的图片路径 |

**返回值**

无返回值描述

**示例**

```python
# 计算图片亮度
brightness = CV.calculate_brightness("/path/to/image.jpeg")
```

### encode_qr_code

```python
def encode_qr_code(content: str, save_path: str)
```

**归属模块**: `hypium.action.host.cv`

**归属类**: `CV`

**类型**: 函数

**描述**

生成二维码

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| content | 需要保存的二维码中的字符串 |
| save_path | 生成的二维码图片保存路径 |

**返回值**

无返回值描述

**示例**

```python
# 生成二维码
CV.encode_qr_code("test_msg", "/path/to/save_qr_image.jpeg")
```

### decode_qr_code

```python
def decode_qr_code(image_path: str) -> str
```

**归属模块**: `hypium.action.host.cv`

**归属类**: `CV`

**类型**: 函数

**描述**

解析二维码

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| image_path | 二维码图片路径 |

**返回值**

二维码图片中的文本信息, 如果解析二维码失败则返回空字符串

**示例**

```python
# 解析二维码
msg = CV.decode_qr_code("/path/to/qr_image.jpeg")
```

### get_video_resolution

```python
def get_video_resolution(file_path: str) -> (int, int)
```

**归属模块**: `hypium.action.host.cv`

**归属类**: `CV`

**类型**: 函数

**描述**

读取视频分辨率

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

视频分辨率, (宽度, 高度)

**示例**

```python
# 获取视频分辨率
resolution = CV.get_video_resolution("test.mp4")
```

# hypium.checker.assertion

**类型**: `module`

## Assert

**类型**: `class`

**描述**

基础断言操作, 支持断言失败后自动截屏
from hypium.checker import Assert

```python
# UiDriver对象内置模块, 通过driver调用
driver.Assert
```

### is_true

```python
def is_true(actual: bool, fail_msg: str = None)
```

**归属模块**: `hypium.checker.assertion`

**归属类**: `Assert`

**类型**: 函数

**描述**

检查实际值和期望值相等

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| actual | 实际值 |
| expect | 期望值 |
| fail_msg | 检查失败时打印的内容 |

**返回值**

无返回值描述

**示例**

```python
# 检查实际值和期望值相等
driver.Assert.is_true(actual, True)
```

### equal

```python
def equal(actual: Any, expect: Any = True, fail_msg: str = None)
```

**归属模块**: `hypium.checker.assertion`

**归属类**: `Assert`

**类型**: 函数

**描述**

检查实际值和期望值相等

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| actual | 实际值 |
| expect | 期望值 |
| fail_msg | 检查失败时打印的内容 |

**返回值**

无返回值描述

**示例**

```python
# 检查实际值和期望值相等
driver.Assert.equal(actual, "a")
```

### not_equal

```python
def not_equal(actual: Any, expect: Any = True, fail_msg: str = None)
```

**归属模块**: `hypium.checker.assertion`

**归属类**: `Assert`

**类型**: 函数

**描述**

检查实际值于预期值不等

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| actual | 实际值 |
| expect | 期望值 |
| fail_msg | 检查失败时打印的内容 |

**返回值**

无返回值描述

**示例**

```python
# 检查实际值和期望值不相等
driver.Assert.not_equal(actual, "a")
```

### starts_with

```python
def starts_with(actual: str, expect: str, fail_msg: str = None)
```

**归属模块**: `hypium.checker.assertion`

**归属类**: `Assert`

**类型**: 函数

**描述**

检查实际值以期望值开头

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| actual | 实际值 |
| expect | 期望值 |
| fail_msg | 检查失败时打印的内容 |

**返回值**

无返回值描述

**示例**

```python
# 检查实际值以期望值开头
driver.Assert.starts_with(actual, "发送到")
```

### ends_with

```python
def ends_with(actual: str, expect: str, fail_msg: str = None)
```

**归属模块**: `hypium.checker.assertion`

**归属类**: `Assert`

**类型**: 函数

**描述**

检查实际值以期望值结尾

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| actual | 实际值 |
| expect | 期望值 |
| fail_msg | 检查失败时打印的内容 |

**返回值**

无返回值描述

**示例**

```python
# 检查实际值以期望值结尾
driver.Assert.ends_with(actual, "广告")
```

### contains

```python
def contains(actual: str, expect: str, fail_msg: str = None)
```

**归属模块**: `hypium.checker.assertion`

**归属类**: `Assert`

**类型**: 函数

**描述**

检查实际值包含期望值

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| actual | 实际值 |
| expect | 期望值 |
| fail_msg | 检查失败时打印的内容 |

**返回值**

无返回值描述

**示例**

```python
# 检查实际值包含期望值
driver.Assert.contains(actual, "发送")
```

### greater

```python
def greater(actual: Any, expect: Any, fail_msg: str = None)
```

**归属模块**: `hypium.checker.assertion`

**归属类**: `Assert`

**类型**: 函数

**描述**

检查actual是否大于expect, 不满足时抛出TestAssertionError异常

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| actual | 实际值 |
| expect | 期望值 |
| fail_msg | 检查失败时打印的内容 |

**返回值**

无返回值描述

**示例**

```python
# 检查实际值大于期望值
driver.Assert.greater(actual, 100)
```

### greater_equal

```python
def greater_equal(actual: Any, expect: Any, fail_msg: str = None)
```

**归属模块**: `hypium.checker.assertion`

**归属类**: `Assert`

**类型**: 函数

**描述**

检查actual是否大于等于expect, 不满足时抛出TestAssertionError异常

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| actual | 实际值 |
| expect | 期望值 |
| fail_msg | 检查失败时打印的内容 |

**返回值**

无返回值描述

**示例**

```python
# 检查实际值大于期望值
driver.Assert.greater_equal(actual, 100)
```

### match_regexp

```python
def match_regexp(actual: Any, expect: Any, fail_msg: str = None)
```

**归属模块**: `hypium.checker.assertion`

**归属类**: `Assert`

**类型**: 函数

**描述**

检查actual是否匹配正则表达式expect, 不满足时抛出TestAssertionError异常

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| actual | 实际值 |
| expect | 期望值 |
| fail_msg | 检查失败时打印的内容 |

**返回值**

无返回值描述

**示例**

```python
# 检查实际值匹配期望的正则表达式
driver.Assert.match_regexp(actual, r"星期.+")
```

### less

```python
def less(actual: Any, expect: Any, fail_msg: str = None)
```

**归属模块**: `hypium.checker.assertion`

**归属类**: `Assert`

**类型**: 函数

**描述**

检查actual是否小于expect, 不满足时抛出TestAssertionError异常

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| actual | 实际值 |
| expect | 期望值 |
| fail_msg | 检查失败时打印的内容 |

**返回值**

无返回值描述

**示例**

```python
# 检查实际值小于期望值
driver.Assert.less(actual, 100)
```

### less_equal

```python
def less_equal(actual: Any, expect: Any, fail_msg: str = None)
```

**归属模块**: `hypium.checker.assertion`

**归属类**: `Assert`

**类型**: 函数

**描述**

检查actual是否小于等于expect, 不满足时抛出TestAssertionError异常

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| actual | 实际值 |
| expect | 期望值 |
| fail_msg | 检查失败时打印的内容 |

**返回值**

无返回值描述

**示例**

```python
# 检查实际值小于等于期望值
driver.Assert.less_equal(actual, 100)
```

# hypium.dfx.tracker

**类型**: `module`

## UpLoadTimeManager

**类型**: `class`

**描述**

SDK打点上报管理

**导入方式**

```python
from hypium.dfx.tracker import UpLoadTimeManager
```

# hypium.exception

**类型**: `module`

## HypiumNotSupportError

**类型**: `class`

**描述**

操作在当前系统版本/设置上不支持时抛出该异常

**导入方式**

```python
from hypium.exception import HypiumNotSupportError
```

## HypiumNotImplementError

**类型**: `class`

**描述**

已经规划实现，当前代码还未完成时抛出该异常

**导入方式**

```python
from hypium.exception import HypiumNotImplementError
```

## HypiumOperationFailError

**类型**: `class`

**描述**

接口操作失败时抛出该异常

**导入方式**

```python
from hypium.exception import HypiumOperationFailError
```

## HypiumParamError

**类型**: `class`

**描述**

传入参数错误时抛出该异常

**导入方式**

```python
from hypium.exception import HypiumParamError
```

## HypiumBackendObjectDropped

**类型**: `class`

**描述**

意外情况导致后端对象被销毁时抛出该异常

**导入方式**

```python
from hypium.exception import HypiumBackendObjectDropped
```

## HypiumParamDirectionError

**类型**: `class`

**描述**

操作方向参数异常

**导入方式**

```python
from hypium.exception import HypiumParamDirectionError
```

## HypiumParamSideError

**类型**: `class`

**描述**

位置参数异常

**导入方式**

```python
from hypium.exception import HypiumParamSideError
```

## HypiumParamUiTargetError

**类型**: `class`

**描述**

Ui操作目标参数异常

**导入方式**

```python
from hypium.exception import HypiumParamUiTargetError
```

## HypiumParamAreaError

**类型**: `class`

**描述**

屏幕区域类型参数异常

**导入方式**

```python
from hypium.exception import HypiumParamAreaError
```

## HypiumParamTouchModeError

**类型**: `class`

**描述**

触摸操作方式参数异常

**导入方式**

```python
from hypium.exception import HypiumParamTouchModeError
```

## HypiumComponentNotFoundError

**类型**: `class`

**描述**

控件查找失败异常

**导入方式**

```python
from hypium.exception import HypiumComponentNotFoundError
```

# hypium.model.basic_data_type

**类型**: `module`

## Rect

**类型**: `class`

**描述**

表示矩形的区域的位置

**导入方式**

```python
from hypium.model.basic_data_type import Rect
```

### get_size

```python
def get_size() -> (int, int)
```

**归属模块**: `hypium.model.basic_data_type`

**归属类**: `Rect`

**类型**: 函数

**描述**

获取矩形区域的宽度和长度

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

tuple类型,  (width, height)

**示例**

```python
# 无示例
```

### get_center

```python
def get_center() -> (int, int)
```

**归属模块**: `hypium.model.basic_data_type`

**归属类**: `Rect`

**类型**: 函数

**描述**

获取矩形区域的中心点坐标

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

(center_x, center_y)

**示例**

```python
# 无示例
```

### get_pos

```python
def get_pos(x_offset: float, y_offset: float) -> (int, int)
```

**归属模块**: `hypium.model.basic_data_type`

**归属类**: `Rect`

**类型**: 函数

**描述**

获取矩形区域内部指定位置的绝对坐标

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| x_offset | 矩形区域内部x方向偏移, 支持相对距离[0, 1], 大于1表示绝对长度 |
| y_offset | 矩形区域内部y方向偏移, 支持相对距离[0, 1], 大于1表示绝对长度 |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

## Point

**类型**: `class`

**描述**

表示一个坐标点

**导入方式**

```python
from hypium.model.basic_data_type import Point
```

### to_tuple

```python
def to_tuple()
```

**归属模块**: `hypium.model.basic_data_type`

**归属类**: `Point`

**类型**: 函数

**描述**

将Point对象转换为tuple类型, (x, y)

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

## MatchPattern

**类型**: `class`

**描述**

指定BY选择器的匹配模式, 例如BY.text("app_", MatchPattern.STARTS_WITH)
```
from hypium.model import MatchPattern
```

**导入方式**

```python
from hypium.model.basic_data_type import MatchPattern
```

## WindowMode

**类型**: `class`

**描述**

表示窗口状态, UiWindow.getWindowMode返回值类型
```
from hypium.model import WindowMode
```

**导入方式**

```python
from hypium.model.basic_data_type import WindowMode
```

## ResizeDirection

**类型**: `class`

**描述**

窗口大小调整方向, 调用UiWindow.resize时使用
```
from hypium.model import ResizeDirection
```

**导入方式**

```python
from hypium.model.basic_data_type import ResizeDirection
```

## WindowFilter

**类型**: `class`

**描述**

根据指定条件获取匹配的window
```
from hypium.model import WindowFilter
```

**导入方式**

```python
from hypium.model.basic_data_type import WindowFilter
```

### title

```python
def title(title: str)
```

**归属模块**: `hypium.model.basic_data_type`

**归属类**: `WindowFilter`

**类型**: 函数

**描述**

指定窗口标题

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

无返回值描述

**示例**

```python
filter = WindowFilter().title("音乐")
```

### bundle_name

```python
def bundle_name(bundle_name: str)
```

**归属模块**: `hypium.model.basic_data_type`

**归属类**: `WindowFilter`

**类型**: 函数

**描述**

指定窗口所属的应用包名

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

无返回值描述

**示例**

```python
filter = WindowFilter().bundle_name("com.example.hap")
```

### focused

```python
def focused(focused: bool = True)
```

**归属模块**: `hypium.model.basic_data_type`

**归属类**: `WindowFilter`

**类型**: 函数

**描述**

指定窗口是否获得焦点

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

无返回值描述

**示例**

```python
filter = WindowFilter().focused(True)
```

### actived

```python
def actived(actived: bool = True)
```

**归属模块**: `hypium.model.basic_data_type`

**归属类**: `WindowFilter`

**类型**: 函数

**描述**

指定窗口是否活动

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

无返回值描述

**示例**

```python
filter = WindowFilter().actived(True)
```

## DisplayRotation

**类型**: `class`

**描述**

屏幕旋转角度，在UiDriver.setDisplayRotation中使用
```
from hypium.model import DisplayRotation
```

**导入方式**

```python
from hypium.model.basic_data_type import DisplayRotation
```

## MouseButton

**类型**: `class`

**描述**

鼠标按键
```
from hypium.model import MouseButton
```

**导入方式**

```python
from hypium.model.basic_data_type import MouseButton
```

## KeyCode

**类型**: `class`

**描述**

Openharmony键盘码
```
from hypium.model import KeyCode
```

**导入方式**

```python
from hypium.model.basic_data_type import KeyCode
```

## UiParam

**类型**: `class`

**描述**

Ui操作控制相关的常量
```
from hypium.model import UiParam
```

**导入方式**

```python
from hypium.model.basic_data_type import UiParam
```

## DeviceType

**类型**: `class`

**描述**

设备类型
```
from hypium.model import DeviceType
```

**导入方式**

```python
from hypium.model.basic_data_type import DeviceType
```

## AppState

**类型**: `class`

**描述**

应用程序状态常量

**导入方式**

```python
from hypium.model.basic_data_type import AppState
```

## TouchPadSwipeOptions

**类型**: `class`

**描述**

触摸板滑动选择器

**导入方式**

```python
from hypium.model.basic_data_type import TouchPadSwipeOptions
```

### stay

```python
def stay(stay: bool = True)
```

**归属模块**: `hypium.model.basic_data_type`

**归属类**: `TouchPadSwipeOptions`

**类型**: 函数

**描述**

指定在操作结束位置是否停留

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| stay | 滑动结束以后是否停留一秒，默认值为FALSE |

**返回值**

无返回值描述

**示例**

```python
option = TouchPadSwipeOptions().stay(True)
```

### speed

```python
def speed(speed: int)
```

**归属模块**: `hypium.model.basic_data_type`

**归属类**: `TouchPadSwipeOptions`

**类型**: 函数

**描述**

指定速度

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| speed | 触摸板多指滑动速度，默认值2000 速度范围200 - 40000，超过范围则取值为默认值（2000） |

**返回值**

无返回值描述

**示例**

```python
option = TouchPadSwipeOptions().speed(2000)
```

## InputTextMode

**类型**: `class`

**描述**

输入模式选择器

**导入方式**

```python
from hypium.model.basic_data_type import InputTextMode
```

### paste

```python
def paste(paste: bool = False)
```

**归属模块**: `hypium.model.basic_data_type`

**归属类**: `InputTextMode`

**类型**: 函数

**描述**

输入文本时是否指定以复制粘贴方式输入。
1.当输入文本中包含中文、特殊字符或文本长度超过200字符时，无论该参数取值为何，均以复制粘贴方式输入。
2.在智能穿戴设备中，该接口不支持以复制粘贴方式输入。

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

无返回值描述

**示例**

```python
# 通过剪切板粘贴的方式输入文本
driver.input_text(BY.type("TextInput"), "123456789", mode=InputTextMode().paste(True))
```

### addition

```python
def addition(addition: bool = False)
```

**归属模块**: `hypium.model.basic_data_type`

**归属类**: `InputTextMode`

**类型**: 函数

**描述**

输入文本时是否以追加的方式进行输入

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

无返回值描述

**示例**

```python
# 追加输入文本
driver.input_text(BY.type("TextInput"), "测试", mode=InputTextMode().addition(True))
```

# hypium.model.driver_config

**类型**: `module`

## DriverConfig

**类型**: `class`

**描述**

配置driver执行参数, 暂未配置项

**导入方式**

```python
from hypium.model.driver_config import DriverConfig
```

# hypium.uidriver.by

**类型**: `module`

## By

**类型**: `class`

**描述**

控件选择器, 在点击/查找控件接口中指定控件, 例如BY.text("中文").key("xxxx")
注意该类的方法只能顺序传参, 不支持通过key=value的方式指定参数

**导入方式**

```python
from hypium.uidriver.by import By
```

### set_config

```python
def set_config(config_name, config_value)
```

**归属模块**: `hypium.uidriver.by`

**归属类**: `By`

**类型**: 函数

**描述**

设置控件查找相关策略配置

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| config_name | 配置项名称 |
| config_value | 配置项值 |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### text

```python
def text(txt: str, mp: MatchPattern = MatchPattern.EQUALS) -> 'By'
```

**归属模块**: `hypium.uidriver.by`

**归属类**: `By`

**类型**: 函数

**描述**

通过文本选择控件

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| txt | 控件的text属性值 |
| mp | 匹配模式, MatchPattern枚举变量 |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### key

```python
def key(key: str, mp: MatchPattern = None) -> 'By'
```

**归属模块**: `hypium.uidriver.by`

**归属类**: `By`

**类型**: 函数

**描述**

通过key选择控件

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| key | 控件的key属性值 |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### id

```python
def id(compId: str, mp: MatchPattern = None) -> 'By'
```

**归属模块**: `hypium.uidriver.by`

**归属类**: `By`

**类型**: 函数

**描述**

通过id选择控件

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### type

```python
def type(tp: str, mp: MatchPattern = None) -> 'By'
```

**归属模块**: `hypium.uidriver.by`

**归属类**: `By`

**类型**: 函数

**描述**

通过控件类型选择控件

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| tp | 控件的类型属性值 |
| mp | 匹配模式, 默认全等匹配, 支持MatchPattern枚举中的类型 |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### hint

```python
def hint(hint: str, mp: MatchPattern = None)
```

**归属模块**: `hypium.uidriver.by`

**归属类**: `By`

**类型**: 函数

**描述**

通过hint属性选择控件

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| hint | 控件的类型属性值 |
| mp | 匹配模式, 默认全等匹配, 支持MatchPattern枚举中的类型 |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### checkable

```python
def checkable(b: bool = True) -> 'By'
```

**归属模块**: `hypium.uidriver.by`

**归属类**: `By`

**类型**: 函数

**描述**

通过checkable属性选择控件

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| b | 目标控件的checkable属性值 |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### longClickable

```python
def longClickable(b: bool = True) -> 'By'
```

**归属模块**: `hypium.uidriver.by`

**归属类**: `By`

**类型**: 函数

**描述**

通过longClickable属性选择控件

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| b | 目标控件的longClickable属性值 |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### clickable

```python
def clickable(b: bool = True) -> 'By'
```

**归属模块**: `hypium.uidriver.by`

**归属类**: `By`

**类型**: 函数

**描述**

指定clickable属性选择控件

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| b | 目标控件的clickable属性值 |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### scrollable

```python
def scrollable(b: bool = True) -> 'By'
```

**归属模块**: `hypium.uidriver.by`

**归属类**: `By`

**类型**: 函数

**描述**

指定scrollable属性选择控件

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| b | 目标控件的scrollable属性值 |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### enabled

```python
def enabled(b: bool = True) -> 'By'
```

**归属模块**: `hypium.uidriver.by`

**归属类**: `By`

**类型**: 函数

**描述**

指定enabled属性选择控件

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| b | 目标控件的enabled属性值 |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### focused

```python
def focused(b: bool = True) -> 'By'
```

**归属模块**: `hypium.uidriver.by`

**归属类**: `By`

**类型**: 函数

**描述**

指定focused属性选择控件

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| b | 目标控件的focused属性值 |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### selected

```python
def selected(b: bool = True) -> 'By'
```

**归属模块**: `hypium.uidriver.by`

**归属类**: `By`

**类型**: 函数

**描述**

指定selected属性选择控件

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| b | 目标控件的selected属性值 |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### checked

```python
def checked(b: bool = True) -> 'By'
```

**归属模块**: `hypium.uidriver.by`

**归属类**: `By`

**类型**: 函数

**描述**

指定checked属性选择控件

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| b | 目标控件的checked属性值 |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### isBefore

```python
def isBefore(by: 'By') -> 'By'
```

**归属模块**: `hypium.uidriver.by`

**归属类**: `By`

**类型**: 函数

**描述**

指定控件位于另一个控件之前

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| by | 通过By指定的另外一个控件 |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### isAfter

```python
def isAfter(by: 'By') -> 'By'
```

**归属模块**: `hypium.uidriver.by`

**归属类**: `By`

**类型**: 函数

**描述**

指定控件位于另一个控件之后

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| by | 通过By指定的另外一个控件 |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### description

```python
def description(description: str, mp: MatchPattern = MatchPattern.EQUALS) -> 'By'
```

**归属模块**: `hypium.uidriver.by`

**归属类**: `By`

**类型**: 函数

**描述**

指定description属性选择控件

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| description | 描述内容 |
| mp | 匹配模式, MatchPattern枚举变量 |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### inWindow

```python
def inWindow(package_name: str) -> 'By'
```

**归属模块**: `hypium.uidriver.by`

**归属类**: `By`

**类型**: 函数

**描述**

指定控件位于指定应用的窗口

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| package_name | 应用包名 |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### within

```python
def within(by: 'By')
```

**归属模块**: `hypium.uidriver.by`

**归属类**: `By`

**类型**: 函数

**描述**

指定目前控件位于另外一个控件中

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| by | 通过By指定的另外一个控件 |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### xpath

```python
def xpath(xpath: str)
```

**归属模块**: `hypium.uidriver.by`

**归属类**: `By`

**类型**: 函数

**描述**

通过xpath查找控件, (注意xpath不能和其他查找方式同时使用, 通过xpath查找的控件对象
只支持读取控件属性以及click/longClick/doubleClick/inputText/clearText操作)

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| xpath | 控件的xpath路径 |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### abspath

```python
def abspath(abspath: str)
```

**归属模块**: `hypium.uidriver.by`

**归属类**: `By`

**类型**: 函数

**描述**

通过uiviewer插件中生成的非标准绝对路径(控件index从0开始)查找控件(注意abspath不能和其他查找方式同时使用,
通过xpath查找的控件对象只支持读取控件属性以及click/longClick/doubleClick/inputText/clearText操作)

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| abspath | uiviewer插件中生成的非标准绝对路径 |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

# hypium.uidriver.uicomponent

**类型**: `module`

## UiComponent

**类型**: `class`

**描述**

Ui控件对象, 提供操作控件和获取控件属性接口。
注意该类的方法只能顺序传参, 不支持通过key=value的方式指定参数
```
from hypium.uidriver.uicomponent import UiComponent
```

**导入方式**

```python
from hypium.uidriver.uicomponent import UiComponent
```

### click

```python
def click() -> None
```

**归属模块**: `hypium.uidriver.uicomponent`

**归属类**: `UiComponent`

**类型**: 函数

**描述**

点击控件

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### doubleClick

```python
def doubleClick() -> None
```

**归属模块**: `hypium.uidriver.uicomponent`

**归属类**: `UiComponent`

**类型**: 函数

**描述**

双击控件

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### longClick

```python
def longClick() -> None
```

**归属模块**: `hypium.uidriver.uicomponent`

**归属类**: `UiComponent`

**类型**: 函数

**描述**

长按控件

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### getId

```python
def getId() -> int
```

**归属模块**: `hypium.uidriver.uicomponent`

**归属类**: `UiComponent`

**类型**: 函数

**描述**

获取控件id

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

在api8之前返回系统为控件分配的数字id，在api9以及之后返回用户为控件设置的id

**示例**

```python
# 无示例
```

### getKey

```python
def getKey() -> str
```

**归属模块**: `hypium.uidriver.uicomponent`

**归属类**: `UiComponent`

**类型**: 函数

**描述**

获取用户设置的控件id值，该接口在api9之上被删除，使用getId()替换

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

用户设置的控件id值

**示例**

```python
# 无示例
```

### getText

```python
def getText() -> str
```

**归属模块**: `hypium.uidriver.uicomponent`

**归属类**: `UiComponent`

**类型**: 函数

**描述**

获取控件text属性内容

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### getType

```python
def getType() -> str
```

**归属模块**: `hypium.uidriver.uicomponent`

**归属类**: `UiComponent`

**类型**: 函数

**描述**

获取控件type属性内容

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### isClickable

```python
def isClickable() -> bool
```

**归属模块**: `hypium.uidriver.uicomponent`

**归属类**: `UiComponent`

**类型**: 函数

**描述**

获取控件clickable属性内容

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### isScrollable

```python
def isScrollable() -> bool
```

**归属模块**: `hypium.uidriver.uicomponent`

**归属类**: `UiComponent`

**类型**: 函数

**描述**

获取控件scrollable属性内容

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### isEnabled

```python
def isEnabled() -> bool
```

**归属模块**: `hypium.uidriver.uicomponent`

**归属类**: `UiComponent`

**类型**: 函数

**描述**

获取控件enabled属性内容

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### isFocused

```python
def isFocused() -> bool
```

**归属模块**: `hypium.uidriver.uicomponent`

**归属类**: `UiComponent`

**类型**: 函数

**描述**

获取控件focused属性内容

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### isLongClickable

```python
def isLongClickable()
```

**归属模块**: `hypium.uidriver.uicomponent`

**归属类**: `UiComponent`

**类型**: 函数

**描述**

获取控件longClickable属性内容

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### isChecked

```python
def isChecked()
```

**归属模块**: `hypium.uidriver.uicomponent`

**归属类**: `UiComponent`

**类型**: 函数

**描述**

获取控件checked属性内容

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### isCheckable

```python
def isCheckable()
```

**归属模块**: `hypium.uidriver.uicomponent`

**归属类**: `UiComponent`

**类型**: 函数

**描述**

获取控件checkable属性内容

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### isSelected

```python
def isSelected()
```

**归属模块**: `hypium.uidriver.uicomponent`

**归属类**: `UiComponent`

**类型**: 函数

**描述**

获取控件selected属性内容

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### inputText

```python
def inputText(text: str, mode: InputTextMode = None) -> None
```

**归属模块**: `hypium.uidriver.uicomponent`

**归属类**: `UiComponent`

**类型**: 函数

**描述**

向控件中输入文本

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### clearText

```python
def clearText() -> None
```

**归属模块**: `hypium.uidriver.uicomponent`

**归属类**: `UiComponent`

**类型**: 函数

**描述**

清除控件中的文本

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### scrollSearch

```python
def scrollSearch(by: By, vertical: bool = None, offset: int = None) -> 'UiComponent'
```

**归属模块**: `hypium.uidriver.uicomponent`

**归属类**: `UiComponent`

**类型**: 函数

**描述**

在当前控件中上下滚动搜索目标控件

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| by | 目标控件选择器By |
| offset | 滚动起始点和结束点离控件边界的距离, 单位像素(设备api level >= 18支持) |
| vertical | 是否垂直滚动, 默认为垂直滚动(设备api level >= 18支持), 注意由于底层接口限制, 如果指定offset参数,<br>必须同时指定vertical参数，否则会执行异常 |

**返回值**

无返回值描述

**示例**

```python
# 滑动查找控件, 默认垂直方向滚动查找
scroll_area_component = driver.find_component(BY.type("List"))
if scroll_area_component:
# 垂直方向滚动查找
target_component = scroll_area_component.scrollSearch(BY.text("系统"))
# 水平方向滚动查找(api >= 18支持)
target_component = scroll_area_component.scrollSearch(BY.text("系统"), vertical=False)
# 设置滑动启动点距离滑动区域边缘的距离(deadzone), 注意不要超过可滑动区域控件高度(上下滑动)/宽度(左右滑动)的50%
# 注意由于底层接口限制, 如果指定offset参数, 必须同时指定vertical参数
target_component = scroll_area_component.scrollSearch(BY.text("系统"), vertical=True, offset=30)
```

### scrollToTop

```python
def scrollToTop(speed: int = 600) -> None
```

**归属模块**: `hypium.uidriver.uicomponent`

**归属类**: `UiComponent`

**类型**: 函数

**描述**

滚动到当前控件顶部, 注意某些控件可滚动区域和控件实际大小不同可能导致滚动失效

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### scrollToBottom

```python
def scrollToBottom(speed: int = 600) -> None
```

**归属模块**: `hypium.uidriver.uicomponent`

**归属类**: `UiComponent`

**类型**: 函数

**描述**

滚动到当前控件底部, 注意某些控件可滚动区域和控件实际大小不同可能导致滚动失效

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### getDescription

```python
def getDescription() -> str
```

**归属模块**: `hypium.uidriver.uicomponent`

**归属类**: `UiComponent`

**类型**: 函数

**描述**

获取控件description属性内容

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### getBounds

```python
def getBounds() -> Rect
```

**归属模块**: `hypium.uidriver.uicomponent`

**归属类**: `UiComponent`

**类型**: 函数

**描述**

获取控件边框位置

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

表示控件边框位置的Rect对象, 可访问该对象的left/right/top/bottom属性获取边框位置

**示例**

```python
# 无示例
```

### getBoundsCenter

```python
def getBoundsCenter() -> Point
```

**归属模块**: `hypium.uidriver.uicomponent`

**归属类**: `UiComponent`

**类型**: 函数

**描述**

获取控件中心店位置

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

表示控件中心点的Point对象, 可访问该对象的x/y属性获取坐标值, 可以调用to_tuple()方法转换为python的(x, y)形式

**示例**

```python
# 无示例
```

### dragTo

```python
def dragTo(target: 'UiComponent') -> None
```

**归属模块**: `hypium.uidriver.uicomponent`

**归属类**: `UiComponent`

**类型**: 函数

**描述**

将当前控件拖拽到另一个控件上

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| target | 另外一个控件对象 |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### pinchOut

```python
def pinchOut(scale: float) -> None
```

**归属模块**: `hypium.uidriver.uicomponent`

**归属类**: `UiComponent`

**类型**: 函数

**描述**

将控件按指定的比例进行捏合放大

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| scale | 指定放大的比例, 例如1.5 |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### pinchIn

```python
def pinchIn(scale: float) -> None
```

**归属模块**: `hypium.uidriver.uicomponent`

**归属类**: `UiComponent`

**类型**: 函数

**描述**

将控件按指定的比例进行捏合缩小

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| scale | 指定缩小的比例, 例如0.5 |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### getHint

```python
def getHint()
```

**归属模块**: `hypium.uidriver.uicomponent`

**归属类**: `UiComponent`

**类型**: 函数

**描述**

读取控件hint属性

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### getAllProperties

```python
def getAllProperties() -> JsonBase
```

**归属模块**: `hypium.uidriver.uicomponent`

**归属类**: `UiComponent`

**类型**: 函数

**描述**

获取所有属性

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

# hypium.uidriver.uiwindow

**类型**: `module`

## UiWindow

**类型**: `class`

**描述**

窗口对象, 提供窗口相关属性获取和窗口操作接口，
注意该类的方法只能顺序传参, 不支持通过key=value的方式指定参数
```
from hypium.uidriver.uiwindow import UiWindow
```

**导入方式**

```python
from hypium.uidriver.uiwindow import UiWindow
```

### getBundleName

```python
def getBundleName() -> str
```

**归属模块**: `hypium.uidriver.uiwindow`

**归属类**: `UiWindow`

**类型**: 函数

**描述**

获取窗口对应的应用包名

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### getBounds

```python
def getBounds() -> Rect
```

**归属模块**: `hypium.uidriver.uiwindow`

**归属类**: `UiWindow`

**类型**: 函数

**描述**

获取窗口边框位置

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### getTitle

```python
def getTitle() -> str
```

**归属模块**: `hypium.uidriver.uiwindow`

**归属类**: `UiWindow`

**类型**: 函数

**描述**

获取窗口title属性内容

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### getWindowMode

```python
def getWindowMode() -> WindowMode
```

**归属模块**: `hypium.uidriver.uiwindow`

**归属类**: `UiWindow`

**类型**: 函数

**描述**

获取窗口模式

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

返回WindowMode枚举类型，表示窗口所处的不同模式

**示例**

```python
# 无示例
```

### isFocused

```python
def isFocused() -> bool
```

**归属模块**: `hypium.uidriver.uiwindow`

**归属类**: `UiWindow`

**类型**: 函数

**描述**

获取窗口focused属性内容(是否获得焦点)

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### isActived

```python
def isActived() -> bool
```

**归属模块**: `hypium.uidriver.uiwindow`

**归属类**: `UiWindow`

**类型**: 函数

**描述**

获取窗口active属性内容(是否处于活动状态)

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### focus

```python
def focus() -> None
```

**归属模块**: `hypium.uidriver.uiwindow`

**归属类**: `UiWindow`

**类型**: 函数

**描述**

使当前窗口获得焦点

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### moveTo

```python
def moveTo(x: int, y: int) -> None
```

**归属模块**: `hypium.uidriver.uiwindow`

**归属类**: `UiWindow`

**类型**: 函数

**描述**

将当前窗口移动到指定坐标

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| x | 坐标x值 |
| y | 坐标y值 |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### resize

```python
def resize(width: int, height: int, direction: ResizeDirection) -> None
```

**归属模块**: `hypium.uidriver.uiwindow`

**归属类**: `UiWindow`

**类型**: 函数

**描述**

根据传入的宽、高和调整方向来调整窗口的大小。适用于支持调整大小的窗口。

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| width | 调整后窗口的宽度 |
| height | 调整后窗口的高度 |
| direction | 窗口调整的方向 |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### split

```python
def split() -> None
```

**归属模块**: `hypium.uidriver.uiwindow`

**归属类**: `UiWindow`

**类型**: 函数

**描述**

将窗口模式切换成分屏模式。适用于支持切换分屏模式的窗口

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### maximize

```python
def maximize() -> None
```

**归属模块**: `hypium.uidriver.uiwindow`

**归属类**: `UiWindow`

**类型**: 函数

**描述**

将窗口最大化。适用于支持窗口最大化操作的窗口

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### minimize

```python
def minimize() -> None
```

**归属模块**: `hypium.uidriver.uiwindow`

**归属类**: `UiWindow`

**类型**: 函数

**描述**

将窗口最小化。适用于支持窗口最小化操作的窗口

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### resume

```python
def resume() -> None
```

**归属模块**: `hypium.uidriver.uiwindow`

**归属类**: `UiWindow`

**类型**: 函数

**描述**

将窗口恢复到之前的窗口模式

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### close

```python
def close() -> None
```

**归属模块**: `hypium.uidriver.uiwindow`

**归属类**: `UiWindow`

**类型**: 函数

**描述**

关闭窗口

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

# hypium.webdriver.webdriver_setup_tool

**类型**: `module`

## WebDriverSetupTool

**类型**: `class`

**描述**

webdriver初始化工具, 需要用户自行部署chromedriver二进制文件到hypium安装目录的res/web_debug_tools/chromedriver_{version}目录下

**导入方式**

```python
from hypium.webdriver.webdriver_setup_tool import WebDriverSetupTool
```

### driver

```python
def driver() -> webdriver.Remote
```

**归属模块**: `hypium.webdriver.webdriver_setup_tool`

**归属类**: `WebDriverSetupTool`

**类型**: 属性

**描述**

selenium webdriver

### set_chromedriver_exe_path

```python
def set_chromedriver_exe_path(chromedriver_exe_path)
```

**归属模块**: `hypium.webdriver.webdriver_setup_tool`

**归属类**: `WebDriverSetupTool`

**类型**: 函数

**描述**

设置使用的chromedriver可执行文件路径

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| - | - |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### set_chromedriver_exe_search_path

```python
def set_chromedriver_exe_search_path(chromedriver_exe_search_path)
```

**归属模块**: `hypium.webdriver.webdriver_setup_tool`

**归属类**: `WebDriverSetupTool`

**类型**: 函数

**描述**

设置chromedriver存放路径, 可以存放多个版本和架构的chromedriver, 根据平台和设备webview版本自动匹配合适的chromedriver版本

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| chromedriver_exe_search_path | chromedriver保存路径, 目录结构如下:<br>chromedriver_exe_search_path<br>|--chromedriver_114<br>|-- chromedriver.exe  windows版本<br>|-- chromedriver      linux版本<br>|-- chromedriver.mac  mac版本<br>|--chromedriver_132<br>|-- chromedriver.exe windows版本<br>|-- chromedriver     linux版本<br>|-- chromedriver.mac  mac版本 |

**返回值**

无返回值描述

**示例**

```python
# 无示例
```

### connect

```python
def connect(bundle_name, remote_devtools_port=None, connection_timeout=60, options=None) -> webdriver.Remote
```

**归属模块**: `hypium.webdriver.webdriver_setup_tool`

**归属类**: `WebDriverSetupTool`

**类型**: 函数

**描述**

连接到指定应用的webview界面

**参数说明**

| 参数名称 | 参数说明 |
| --- | --- |
| bundle_name | 目标应用包名 |
| remote_devtools_port | 目标应用webview调试端口, 使用系统内置webview内核的应用无需设置,<br>如果是自定义webview内核的需要设置。 |
| connection_timeout | 连接超时时间 |
| options | 其他传递给selenium webdriver的options |

**返回值**

无返回值描述

**示例**

```python

# 首先需要到chromedriver网站下载对应的chromedriver, 放到hypium安装目录的res/web_debug_tools/chromedriver_{version}目录下
# 例如114版本的chromedriver放到res/web_debug_tools/chromedriver_114目录
# 创建web初始化工具
web_tools =  WebDriverSetupTool(driver)
# 连接应用的的webview
web_tools.connect("com.huawei.hmos.browser")
# 调用webdriver中方法(selenium的webdriver)
web_tools.driver.get("https://baidu.com")
# 关闭/释放driver
web_tools.close()
```

