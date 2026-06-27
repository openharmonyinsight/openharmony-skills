# 示例API错误码

## 401 参数校验失败

**错误信息**

Parameter validation failed.

**错误描述**

在调用示例API进行参数校验时，如果传入的参数不符合要求，系统会产生此错误码。

**可能原因**

1. 必填参数未传入。

2. 参数类型不匹配。

3. 参数值超出允许范围。

**处理步骤**

1. 检查必填参数是否传入。

   根据API参考文档，确认所有必填参数均已正确传入。例如，`performOperation` 接口要求必须传入 `input` 参数。

   ```typescript
   // 错误示例：缺少必填参数
   api.performOperation();

   // 正确示例：传入必填参数
   api.performOperation("valid input");
   ```

2. 检查参数类型是否匹配。

   确认传入参数的类型与API定义的类型一致。例如，如果接口要求 `string` 类型，不要传入 `number` 类型。

   ```typescript
   // 类型不匹配示例
   api.performOperation(123);  // 错误：传入的是 number 类型

   // 类型正确示例
   api.performOperation("123");  // 正确：传入的是 string 类型
   ```

3. 检查参数值是否在允许范围内。

   某些参数可能有取值范围限制。确认传入的值在允许的范围内。

   ```typescript
   // 示例：检查字符串长度
   if (input.length > 1000) {
     console.error("输入过长，最大支持1000个字符");
   }
   ```

> **说明**：参数校验失败通常发生在API调用的早期阶段，开发者应优先检查参数的完整性、类型和取值范围。

## 403 权限拒绝

**错误信息**

Permission denied.

**错误描述**

在调用需要权限的API时，如果应用未获得相应的系统权限，系统会产生此错误码。

**可能原因**

1. 应用未在 `module.json5` 中声明所需权限。

2. 应用声明了权限但未获得用户授权。

3. 调用了系统API但应用不是系统应用。

**处理步骤**

1. 检查权限声明。

   在应用的 `module.json5` 文件中，确认已声明所需的权限。例如，示例API需要 `ohos.permission.EXAMPLE` 权限。

   ```json5
   {
     "requestPermissions": [
       {
         "name": "ohos.permission.EXAMPLE",
         "reason": "$string:example_permission_reason",
         "usedScene": {
           "abilities": ["EntryAbility"],
           "when": "inuse"
         }
       }
     ]
   }
   ```

2. 检查用户授权状态。

   确认用户已授予应用相应权限。可以通过 `abilityAccessCtrl.createAtManager().checkAccessToken()` 检查权限状态。

   ```typescript
   import abilityAccessCtrl from '@ohos.abilityAccessCtrl';

   let atManager = abilityAccessCtrl.createAtManager();
   let grantStatus = await atManager.checkAccessToken(tokenID, 'ohos.permission.EXAMPLE');
   if (grantStatus !== abilityAccessCtrl.GrantStatus.PERMISSION_GRANTED) {
     console.error("权限未授予");
   }
   ```

3. 确认应用类型与API级别匹配。

   如果调用的是 `@systemapi` 标记的系统API，确认应用是系统应用。非系统应用只能调用公共API。

> **说明**：权限错误通常与应用的权限配置和用户授权相关，开发者应确保权限声明正确并已获得用户授权。

## 404 资源未找到

**错误信息**

Resource not found.

**错误描述**

当请求的资源（如文件、数据项、配置信息等）不存在或已被删除时，系统会产生此错误码。

**可能原因**

1. 请求的资源ID不正确。

2. 资源已被删除。

3. 资源路径不正确。

**处理步骤**

1. 检查资源ID是否正确。

   确认传入的资源标识符与实际存在的资源匹配。例如，在使用 `getResource` 接口时，确保资源ID有效。

   ```typescript
   let resourceId = 12345;
   try {
     let resource = await api.getResource(resourceId);
   } catch (e) {
     console.error("资源ID无效：" + resourceId);
   }
   ```

2. 检查资源是否存在。

   在操作资源前，先检查资源是否存在。可以通过 `hasResource` 等查询接口验证。

   ```typescript
   let exists = await api.hasResource(resourceId);
   if (!exists) {
     console.warn("资源不存在，请检查资源ID");
   }
   ```

3. 检查资源路径是否正确。

   如果使用路径访问资源，确认路径格式正确且从正确的根目录开始。

   ```typescript
   // 错误示例：相对路径可能找不到资源
   let path = "data/config.json";

   // 正确示例：使用绝对路径或正确的相对路径
   let path = "/etc/data/config.json";
   ```

> **说明**：资源未找到错误通常与资源标识或路径有关，开发者应确保使用正确的资源标识符并验证资源存在性。

## 500 内部服务错误

**错误信息**

Internal service error.

**错误描述**

当服务端处理请求时发生内部异常，无法完成请求，系统会产生此错误码。此类错误通常不是由客户端调用导致的，而是服务端内部问题。

**可能原因**

1. 服务端资源耗尽（如内存不足、连接数过多）。

2. 服务端内部逻辑异常。

3. 后端依赖服务不可用。

**处理步骤**

1. 记录详细的错误信息。

   捕获完整的错误对象，包括错误码、错误消息和堆栈信息，便于后续定位问题。

   ```typescript
   try {
     await api.performOperation(input);
   } catch (e) {
     console.error("内部服务错误：", JSON.stringify(e));
   }
   ```

2. 检查设备资源使用情况。

   确认设备内存、存储等资源充足。某些内部错误可能由资源不足导致。

3. 稍后重试请求。

   内部服务错误可能是暂时性的，可以采用重试机制。建议使用指数退避策略。

   ```typescript
   async function retryWithBackoff(fn, maxRetries = 3) {
     for (let i = 0; i < maxRetries; i++) {
       try {
         return await fn();
       } catch (e) {
         if (e.code === 500 && i < maxRetries - 1) {
           let delay = Math.pow(2, i) * 1000;  // 1s, 2s, 4s
           await new Promise(resolve => setTimeout(resolve, delay));
         } else {
           throw e;
         }
       }
     }
   }
   ```

> **说明**：内部服务错误通常是服务端问题，客户端应记录错误信息并采用合理的重试策略。如果错误持续发生，请联系系统管理员。
