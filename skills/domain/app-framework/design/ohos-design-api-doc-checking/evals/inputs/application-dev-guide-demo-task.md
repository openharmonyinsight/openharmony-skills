# 任务管理开发指南

本指南介绍如何在应用中接入任务管理能力，适用于希望了解任务管理基本用法的开发者。

## 概述

任务管理提供后台任务的创建与查询能力。某些情况下，任务会被系统自动回收，可能会影响业务连续性，开发者大概需要注意任务的生命周期。

## 开发步骤

1. 在工程中导入模块：

```ts
import demoTaskManager from '@ohos.demo.taskmanager';
```

2. 创建任务：

```ts
let taskInfo: demoTaskManager.TaskInfo = {
  name: 'demoTask',
  delay: 1000
};
demoTaskManager.createTask(taskInfo, (err, taskId) => {
  if (err) {
    console.error(`createTask failed: $ {err.code}`);
    return;
  }
});
```

3. 查询任务列表，接口会 recieve 所有任务并返回。

## 高级用法

本节介绍任务管理的基础导入方式，参见上文开发步骤第 1 步。

## 相关文档

- [demoTaskManager API 参考](./js-apis-demo-taskmanager.md)
- [后台任务开发指导](./background-task-guide.md)
