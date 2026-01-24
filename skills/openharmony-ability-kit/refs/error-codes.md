# 元能力错误码速查

> Ability Kit 常见错误码及解决方案

## 导入
```typescript
import { BusinessError } from '@kit.BasicServicesKit';

try {
  await this.context.startAbility(want);
} catch (err) {
  const error = err as BusinessError;
  console.error(`Error ${error.code}: ${error.message}`);
}
```

---

## 高频错误码

| 错误码 | 错误信息 | 原因 | 解决方案 |
|--------|----------|------|----------|
| **16000001** | The specified ability does not exist | Ability不存在 | 检查want中bundleName/moduleName/abilityName拼写 |
| **16000004** | Cannot start an invisible component | 目标组件不可见 | 目标ability设置`exported: true`或申请权限 |
| **16000011** | The context does not exist | Context已失效 | 检查Ability是否已销毁，避免在销毁后调用 |
| **16000050** | Internal error | 内部错误 | 检查want数据大小(<100KB)，重试 |
| **16000053** | The ability is not on the top of UI | 非顶层应用 | 确保应用在前台顶层再执行免安装启动 |
| **16200001** | The caller has been released | Caller已释放 | 重新调用startAbilityByCall获取新Caller |
| **16200002** | The callee does not exist | Callee不存在 | 检查目标Ability是否已启动并注册Callee |

---

## Ability启动错误（16000xxx）

| 错误码 | 说明 | 快速解决 |
|--------|------|----------|
| 16000001 | Ability不存在 | 检查 bundleName/abilityName 是否正确，确认应用已安装 |
| 16000002 | Ability类型错误 | ServiceExtension需用connectServiceExtensionAbility |
| 16000004 | 不可见组件 | 设置 exported=true 或申请 START_INVISIBLE_ABILITY 权限 |
| 16000005 | 进程权限校验失败 | 检查进程权限配置 |
| 16000006 | 不允许跨用户操作 | 不支持跨用户启动 |
| 16000007 | 服务繁忙 | 稍后重试 |
| 16000008 | 众测应用过期 | 众测应用已过有效期 |
| 16000009 | Wukong模式禁止 | 退出Wukong模式后操作 |
| 16000011 | Context不存在 | Ability可能已销毁 |
| 16000012 | 应用被管控 | 应用被系统管控，考虑卸载 |
| 16000013 | 应用被EDM管控 | 联系企业设备管理员 |
| 16000015 | 服务超时 | 稍后重试 |
| 16000018 | API 11+禁止显式跳转三方 | 使用隐式启动或openLink |
| 16000019 | 隐式启动无匹配 | 检查action/entities/uri配置 |
| 16000050 | 内部错误 | 检查want数据大小，重试 |
| 16000053 | 应用非顶层 | 确保应用在前台 |
| 16000055 | 免安装超时 | 网络问题，重试 |

---

## 应用实例错误

| 错误码 | 说明 | 快速解决 |
|--------|------|----------|
| 16000071 | 不支持应用分身 | 在app.json5配置multiAppMode |
| 16000073 | appCloneIndex无效 | 检查分身索引是否有效 |
| 16000076 | APP_INSTANCE_KEY无效 | 检查实例key是否存在 |
| 16000077 | 实例数量达上限 | 删除已有实例或调整上限 |
| 16000078 | 不支持多实例 | 配置多实例或在2in1设备操作 |

---

## Caller/Callee错误（16200xxx）

| 错误码 | 说明 | 快速解决 |
|--------|------|----------|
| 16200001 | Caller已释放 | 重新调用startAbilityByCall |
| 16200002 | Callee不存在 | 目标Ability需注册Callee方法 |
| 16200004 | 方法已注册 | 避免重复注册同名方法 |
| 16200005 | 方法未注册 | 先在Callee端注册方法 |

---

## WantAgent错误（16000151+）

| 错误码 | 说明 | 快速解决 |
|--------|------|----------|
| 16000151 | WantAgent无效 | 检查WantAgent对象是否存在 |

---

## 启动框架错误（28800xxx）

| 错误码 | 说明 | 快速解决 |
|--------|------|----------|
| 28800001 | 启动任务不存在 | 检查startup配置和任务实现 |
| 28800002 | 循环依赖 | 检查启动任务依赖关系 |
| 28800003 | 任务执行错误 | 检查任务代码和异常处理 |
| 28800004 | 执行超时 | 调整超时时间或优化任务 |

---

## 错误处理模板

```typescript
import { UIAbility, Want } from '@kit.AbilityKit';
import { BusinessError } from '@kit.BasicServicesKit';

export default class EntryAbility extends UIAbility {
  async startTarget() {
    const want: Want = {
      bundleName: 'com.example.target',
      abilityName: 'TargetAbility'
    };

    try {
      await this.context.startAbility(want);
    } catch (err) {
      const error = err as BusinessError;
      switch (error.code) {
        case 16000001:
          console.error('目标Ability不存在，请检查包名和Ability名');
          break;
        case 16000004:
          console.error('目标组件不可见，需要exported=true');
          break;
        case 16000011:
          console.error('Context已失效，Ability可能已销毁');
          break;
        case 16000050:
          console.error('内部错误，请检查want数据大小并重试');
          break;
        default:
          console.error(`启动失败: ${error.code} - ${error.message}`);
      }
    }
  }
}
```

---

## 调试命令

```bash
# 检查应用是否安装
hdc shell bm dump -a

# 查看特定应用的包信息
hdc shell bm dump -n com.example.app

# 查看Ability详情
hdc shell aa dump -a
```

---

## 通用错误码

| 错误码 | 说明 |
|--------|------|
| 201 | 权限不足 |
| 401 | 参数错误（必填参数缺失或类型错误） |
| 801 | 能力不支持（设备不支持该功能） |
