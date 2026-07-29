# Demo UI 设计文档

## 设计信息
| 字段 | 值 |
|------|-----|
| 生成时间 | 2026-07-28 |
| 来源测试点文件 | demo_test_points_preference.md |
| 来源需求文件 | - |
| 选择领域 | ArkUI |
| 分组维度 | 按API |
| Demo页面数 | 1 |
| 控件总数 | 8 |
| 操作模式数 | 3 |
| 测试点覆盖 | 6/6 (100%) |

## 1. API 与系统能力清单
### 1.1 API 清单
| API编号 | API名称 | JSON文件 | 接口路径/方法 | 参数列表 | 错误码 | 关联测试点 | 对应需求ID | API验证状态 |
|----------|---------|----------|---------------|----------|--------|------------|------------|-------------|
| API-001 | preferences.put | - | @ohos.data.preferences put | key: string, value: string | 0, 401 | TP-PREF-001,003,004 | - | ⚠️ 无 API 参考 |
| API-002 | preferences.get | - | @ohos.data.preferences get | key: string | 0, 401 | TP-PREF-002,006 | - | ⚠️ 无 API 参考 |

## 2. 页面规划
### 2.1 页面总览
| 页面ID | 页面名称 | 涉及API | 测试点数 | 控件数 | 操作模式 | 导航标签 |
|--------|---------|---------|---------|--------|---------|---------|
| PAGE-001 | 偏好设置测试 | preferences.put, preferences.get | 6 | 8 | PM-001,PM-002,PM-003 | 偏好设置 |

### 2.2 页面分组策略
- 分组维度：按API
- API 关联合并记录：preferences.put 和 preferences.get 功能强相关，归入同一页面
- 拆分记录：无

### 2.3 操作模式定义
| 模式ID | 模式名称 | 适用页面 | 固定步骤数 | 差异字段 |
|--------|---------|---------|-----------|---------|
| PM-001 | 保存偏好 | PAGE-001 | 3 | key, value, 预期结果 |
| PM-002 | 查询偏好 | PAGE-001 | 2 | key, 预期结果 |
| PM-003 | 清除输入 | PAGE-001 | 1 | - |

## 3. 页面详细设计

### 3.1 页面：偏好设置测试 (PAGE-001)

#### 页面信息表
| 字段 | 值 |
|------|-----|
| 页面ID | PAGE-001 |
| 页面名称 | 偏好设置测试 |
| 涉及API | preferences.put, preferences.get |
| 测试点数 | 6 |
| 控件数 | 8 |

#### 页面区域描述
> **配置区：** 无
> **输入区：** input_001_key（key输入框）, input_001_value（value输入框）
> **操作区：** btn_001_save（保存按钮）, btn_001_query（查询按钮）, btn_001_clear（清除按钮）
> **结果区：** result_001_01（结果显示）, status_001_01（状态显示）

#### 控件清单
| 控件ID | 控件类型 | 控件标签 | 默认值 | 关联参数 | 说明 |
|--------|---------|---------|--------|---------|------|
| input_001_key | TextInput | 键 | '' | key | key输入框 |
| input_001_value | TextInput | 值 | '' | value | value输入框 |
| btn_001_save | Button | 保存 | - | - | 点击触发 preferences.put |
| btn_001_query | Button | 查询 | - | - | 点击触发 preferences.get |
| btn_001_clear | Button | 清除 | - | - | 点击清空输入框 |
| result_001_01 | Text | 结果 | '' | - | 显示操作结果文本 |
| status_001_01 | Text | 状态 | WAITING | - | 显示 PASS/FAIL/WAITING |
| log_001 | List | 日志 | - | - | 操作日志列表 |

#### 模式化映射
##### 模式 PM-001：保存偏好
**操作步骤：** 在 input_001_key 中输入 key → 在 input_001_value 中输入 value → 点击 btn_001_save → 查看 result_001_01 显示结果
**涉及控件：** input_001_key, input_001_value, btn_001_save, result_001_01, status_001_01

| 测试点ID | key | value | 预期结果 | 预期状态 |
|---------|-----|-------|---------|---------|
| TP-PREF-001 | test_key | hello | 保存成功 | PASS |
| TP-PREF-003 | (空) | hello | 参数错误 | FAIL |
| TP-PREF-004 | (超256字符) | hello | 参数错误 | FAIL |
| TP-PREF-006 | test_key | world | 保存成功 | PASS |

##### 模式 PM-002：查询偏好
**操作步骤：** 在 input_001_key 中输入 key → 点击 btn_001_query → 查看 result_001_01 显示结果
**涉及控件：** input_001_key, btn_001_query, result_001_01, status_001_01

| 测试点ID | key | 预期结果 | 预期状态 |
|---------|-----|---------|---------|
| TP-PREF-002 | test_key | hello | PASS |
| TP-PREF-006 | test_key | world | PASS |

##### 模式 PM-003：清除输入
**操作步骤：** 点击 btn_001_clear → 查看 input_001_key 和 input_001_value 清空
**涉及控件：** btn_001_clear, input_001_key, input_001_value, status_001_01

| 测试点ID | 预期状态 |
|---------|---------|
| TP-PREF-005 | WAITING |

## 4. 全局控件映射总表（模式化）
| 操作模式 | 适用测试点范围 | 所在页面 | 涉及控件ID | 操作步骤摘要 |
|---------|-------------|---------|-----------|------------|
| PM-001 | TP-PREF-001,003,004,006 | PAGE-001 | input_001_key,input_001_value,btn_001_save,result_001_01,status_001_01 | 输入key+value→保存→查看结果 |
| PM-002 | TP-PREF-002,006 | PAGE-001 | input_001_key,btn_001_query,result_001_01,status_001_01 | 输入key→查询→查看结果 |
| PM-003 | TP-PREF-005 | PAGE-001 | btn_001_clear,input_001_key,input_001_value,status_001_01 | 点击清除→验证清空 |

## 5. 导航结构
### 5.1 首页（Index）
首页 Grid 卡片，单卡片"偏好设置测试"，点击跳转 PAGE-001

### 5.2 页面路由表
| 路由路径 | 页面名称 | 页面ID | 说明 |
|---------|---------|--------|------|
| pages/Page001 | 偏好设置测试 | PAGE-001 | 偏好设置put/get测试 |

## 汇总
| 维度 | 数量 |
|------|------|
| Demo页面 | 1 |
| UI控件 | 8 |
| 操作模式 | 3 |
| 测试点覆盖 | 6/6 (100%) |

### 未覆盖测试点
无
