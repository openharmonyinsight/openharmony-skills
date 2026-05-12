---
rule_id: "StabilityCodeReview_ResourceManagement_005"
name: "JSON对象未关闭泄漏"
category: "资源管理"
severity: "MEDIUM"
language: ["cpp", "c", "c++"]
author: "OH-Department7 Stability Team"
---

# JSON对象未关闭泄漏

## 问题描述

使用json库（如cJSON、json-c等）相关操作完毕后应记得使用close/put释放内存。JSON对象在创建或解析时会分配内存，如果不及时释放，会导致内存泄漏。

## 检测示例

### ❌ 问题代码

```cpp
// 场景1：cJSON_Parse后异常分支未删除
cJSON* parse_config(const char* json_str) {
    cJSON* root = cJSON_Parse(json_str);  // 创建JSON对象
    if (root == nullptr) {
        return nullptr;
    }
    
    cJSON* name = cJSON_GetObjectItem(root, "name");
    if (name == nullptr) {
        return nullptr;  // 错误：root泄漏
    }
    
    cJSON* value = cJSON_GetObjectItem(root, "value");
    if (value == nullptr) {
        return nullptr;  // 错误：root泄漏
    }
    
    // 处理数据...
    return root;
}

// 场景2：cJSON_CreateObject后泄漏
cJSON* create_response(int code, const char* msg) {
    cJSON* root = cJSON_CreateObject();  // 创建JSON对象
    if (root == nullptr) {
        return nullptr;
    }
    
    cJSON* data = cJSON_CreateObject();
    if (data == nullptr) {
        return nullptr;  // 错误：root泄漏
    }
    
    if (cJSON_AddStringToObject(root, "message", msg) == nullptr) {
        cJSON_Delete(data);
        return nullptr;  // 错误：root泄漏
    }
    
    cJSON_AddItemToObject(root, "data", data);
    return root;
}

// 场景3：json-c库泄漏
struct json_object* load_config(const char* path) {
    struct json_object* root = json_object_from_file(path);  // 加载JSON
    if (root == nullptr) {
        return nullptr;
    }
    
    struct json_object* item = json_object_object_get(root, "config");
    if (item == nullptr) {
        return nullptr;  // 错误：root泄漏
    }
    
    // 处理config...
    return root;
}

// 场景4：循环中创建JSON对象泄漏
int process_array(const char* json_str) {
    cJSON* root = cJSON_Parse(json_str);
    if (root == nullptr) {
        return -1;
    }
    
    cJSON* arr = cJSON_GetObjectItem(root, "items");
    if (arr == nullptr) {
        cJSON_Delete(root);
        return -1;
    }
    
    int count = 0;
    cJSON* item = nullptr;
    cJSON_ArrayForEach(item, arr) {
        cJSON* copy = cJSON_Duplicate(item, 1);  // 复制对象
        if (copy == nullptr) {
            continue;  // 错误：如果循环中断，root可能泄漏
        }
        // 处理copy...
        cJSON_Delete(copy);
        count++;
    }
    
    cJSON_Delete(root);
    return count;
}

// 场景5：解析嵌套对象泄漏
int parse_nested(const char* json_str) {
    cJSON* root = cJSON_Parse(json_str);
    if (root == nullptr) {
        return -1;
    }
    
    cJSON* outer = cJSON_GetObjectItem(root, "outer");
    if (outer == nullptr) {
        return -1;  // 错误：root泄漏
    }
    
    cJSON* inner = cJSON_GetObjectItem(outer, "inner");
    if (inner == nullptr) {
        return -1;  // 错误：root泄漏
    }
    
    int value = cJSON_GetObjectItem(inner, "value")->valueint;
    cJSON_Delete(root);
    return value;
}
```

### ✅ 修复方案

```cpp
// 修复场景1：异常分支释放
cJSON* parse_config(const char* json_str) {
    cJSON* root = cJSON_Parse(json_str);
    if (root == nullptr) {
        return nullptr;
    }
    
    cJSON* name = cJSON_GetObjectItem(root, "name");
    if (name == nullptr) {
        cJSON_Delete(root);  // 正确：释放root
        return nullptr;
    }
    
    cJSON* value = cJSON_GetObjectItem(root, "value");
    if (value == nullptr) {
        cJSON_Delete(root);  // 正确：释放root
        return nullptr;
    }
    
    return root;  // 调用者负责释放
}

// 修复场景2：使用RAII封装
class CJsonGuard {
public:
    explicit CJsonGuard(cJSON* obj) : obj_(obj) {}
    ~CJsonGuard() { if (obj_) cJSON_Delete(obj_); }
    cJSON* get() const { return obj_; }
    cJSON* release() { cJSON* tmp = obj_; obj_ = nullptr; return tmp; }
private:
    cJSON* obj_;
};

cJSON* create_response(int code, const char* msg) {
    CJsonGuard root(cJSON_CreateObject());
    if (root.get() == nullptr) {
        return nullptr;
    }
    
    CJsonGuard data(cJSON_CreateObject());
    if (data.get() == nullptr) {
        return nullptr;  // root自动释放
    }
    
    if (cJSON_AddStringToObject(root.get(), "message", msg) == nullptr) {
        return nullptr;  // root和data自动释放
    }
    
    cJSON_AddItemToObject(root.get(), "data", data.release());
    return root.release();
}

// 修复场景3：json-c库使用json_object_put
int load_and_process(const char* path) {
    struct json_object* root = json_object_from_file(path);
    if (root == nullptr) {
        return -1;
    }
    
    struct json_object* item = json_object_object_get(root, "config");
    if (item == nullptr) {
        json_object_put(root);  // 正确：释放root
        return -1;
    }
    
    int result = 0;
    // 处理config...
    
    json_object_put(root);
    return result;
}

// 修复场景4：循环中正确管理
int process_array_safe(const char* json_str) {
    CJsonGuard root(cJSON_Parse(json_str));
    if (root.get() == nullptr) {
        return -1;
    }
    
    cJSON* arr = cJSON_GetObjectItem(root.get(), "items");
    if (arr == nullptr) {
        return -1;
    }
    
    int count = 0;
    cJSON* item = nullptr;
    cJSON_ArrayForEach(item, arr) {
        CJsonGuard copy(cJSON_Duplicate(item, 1));
        if (copy.get() == nullptr) {
            continue;
        }
        // 处理copy...
        count++;
    }
    
    return count;
}

// 修复场景5：goto统一清理
int parse_nested_goto(const char* json_str) {
    cJSON* root = nullptr;
    int result = -1;
    
    root = cJSON_Parse(json_str);
    if (root == nullptr) {
        goto error;
    }
    
    cJSON* outer = cJSON_GetObjectItem(root, "outer");
    if (outer == nullptr) {
        goto error;
    }
    
    cJSON* inner = cJSON_GetObjectItem(outer, "inner");
    if (inner == nullptr) {
        goto error;
    }
    
    result = cJSON_GetObjectItem(inner, "value")->valueint;
    
error:
    if (root) {
        cJSON_Delete(root);
    }
    return result;
}
```

## 检测范围

检查以下模式：

- `cJSON_Parse/cJSON_ParseWithOpts` 解析JSON
- `cJSON_CreateObject/cJSON_CreateArray` 创建JSON对象
- `cJSON_Duplicate` 复制JSON对象
- `json_object_new_object/json_object_new_array` (json-c库)
- `json_object_from_file/json_tokener_parse` (json-c库)
- 异常分支未调用`cJSON_Delete/json_object_put`

## 检测要点

1. 识别JSON对象创建操作
2. 追踪JSON变量到函数结束
3. 检查异常返回分支是否释放JSON对象
4. 排除使用RAII封装或返回JSON对象的情况

## 风险流分析（RiskFlow）

- **RISK_SOURCE**：创建/解析的JSON对象
- **RISK_TYPE**：内存泄漏
- **RISK_PATH**：JSON创建 -> 异常返回 -> 未close -> 内存泄漏
- **IMPACT_POINT**：内存资源耗尽、程序稳定性下降

## 影响分析（ImpactAnalysis）

- **Trigger**：异常分支返回时JSON对象未释放
- **Propagation**：内存泄漏累积，进程内存持续增长
- **Consequence**：内存耗尽、程序崩溃、服务不可用
- **Mitigation**：使用cJSON_Delete/json_object_put释放JSON对象，或使用RAII封装

## 误报排除

| 场景 | 识别特征 | 处理方式 |
|------|----------|----------|
| 返回JSON对象 | return json变量 | 不报 |
| 使用RAII封装 | CJsonGuard等 | 不报 |
| 有delete/put释放 | cJSON_Delete/json_object_put | 不报 |
| NOPROTECT标记 | 有 // NOPROTECT 注释 | 不报 |
| 第三方库 | 位于 third_party 目录 | 白名单排除 |
## 测试用例

### 触发用例（应该报）

```cpp
// test_ResourceManagement_005_trigger.cpp
cJSON* trigger_bad_1(const char* json_str) {
    cJSON* root = cJSON_Parse(json_str);  // 应该报：JSON泄漏
    if (root == nullptr) {
        return nullptr;
    }
    cJSON* item = cJSON_GetObjectItem(root, "key");
    if (item == nullptr) {
        return nullptr;  // root泄漏
    }
    return root;
}

cJSON* trigger_bad_2(int code) {
    cJSON* root = cJSON_CreateObject();  // 应该报：JSON泄漏
    if (root == nullptr) {
        return nullptr;
    }
    cJSON* data = cJSON_CreateObject();
    if (data == nullptr) {
        return nullptr;  // root泄漏
    }
    cJSON_AddItemToObject(root, "data", data);
    return root;
}

struct json_object* trigger_bad_3(const char* path) {
    struct json_object* root = json_object_from_file(path);  // 应该报：JSON泄漏
    if (root == nullptr) {
        return nullptr;
    }
    struct json_object* item = json_object_object_get(root, "config");
    if (item == nullptr) {
        return nullptr;  // root泄漏
    }
    return root;
}
```

### 安全用例（不应该报）

```cpp
// test_ResourceManagement_005_safe.cpp
cJSON* safe_good_1(const char* json_str) {
    cJSON* root = cJSON_Parse(json_str);
    if (root == nullptr) {
        return nullptr;
    }
    cJSON* item = cJSON_GetObjectItem(root, "key");
    if (item == nullptr) {
        cJSON_Delete(root);  // 安全：手动释放
        return nullptr;
    }
    return root;
}

cJSON* safe_good_2(const char* json_str) {
    CJsonGuard root(cJSON_Parse(json_str));  // 安全：RAII管理
    if (root.get() == nullptr) {
        return nullptr;
    }
    cJSON* item = cJSON_GetObjectItem(root.get(), "key");
    if (item == nullptr) {
        return nullptr;
    }
    return root.release();
}

// NOPROTECT: 测试代码
cJSON* noprotect_case(const char* json_str) {
    cJSON* root = cJSON_Parse(json_str);
    if (cJSON_GetObjectItem(root, "key") == nullptr) {
        return nullptr;
    }
    return root;
}
```