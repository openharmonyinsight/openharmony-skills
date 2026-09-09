# demoTaskManager(任务管理)

本模块提供任务管理能力，用于创建、查询和取消后台任务。

> **说明**
>
> 本模块首批开放以下API，起始版本为9，能力由系统提供。
> 导入方式：
> ```js
> import demoTaskManager from '@ohos.demo.taskmanager';
> ```

## demoTaskManager.createTask9+

创建一个后台任务。需要权限 ohos.permission.RUNNING_TASKS。

**系统能力**：SystemCapability.Demo.TaskManager

**参数**：

| 参数名 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| taskInfo | [TaskInfo](#taskinfo) | 是 | 任务信息 |
| callback | AsyncCallback&lt;number&gt; | 是 | 回调函数，返回任务ID |

**返回值**：AsyncCallback&lt;number&gt;

**错误码**：

| 错误码ID | 错误信息 |
| --- | --- |
| 401 | Parameter error. Possible causes: 1. Mandatory parameters are left unspecified. |

**示例**：

```ts
import demoTaskManager from '@ohos.demo.taskmanager';

let taskInfo: demoTaskManager.TaskInfo = {
  name: 'demoTask',
  delay: 1000
};

demoTaskManager.createTask(taskInfo, (err, taskId) => {
  if (err) {
    console.error(`createTask failed, code is $ {err.code}, message is ${err.message}`);
    return;
  }
  console.info(`createTask success, taskId: ${taskId}`);
});
```

## demoTaskManager.queryTasks9+

查询当前所有任务，该接口会 recieve 任务列表并返回给调用方。任务在 UiAbility 退出后自动销毁。

**系统能力**：SystemCapability.Demo.TaskManager

**返回值**：Promise&lt;Array&lt;[TaskInfo](#taskinfo)&gt;&gt;

**完整示例**：

```ts
import demoTaskManager from '@ohos.demo.taskmanager';

async function queryAll() {
  let tasks = await demoTaskManager.queryTasks();
  tasks.forEach((task) => {
    console.info(`task name: ${task.name}`);
```

## TaskInfo9+

任务信息描述。

**属性**：

| 名称 | 类型 | 可读 | 可写 | 说明 |
| --- | --- | --- | --- | --- |
| name | string | 是 | 是 | 任务名称 |
| delay | number | 是 | 是 | 延迟时间，单位ms |
