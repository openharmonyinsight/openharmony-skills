# 调试指南

分析测试执行失败，定位问题根因，生成修正建议。

## 单步调试规则

> **绝对禁止将多个步骤合并调试！必须严格遵循单步调试原则！**

1. **每次只调试一个步骤**
   - 只保留当前正在调试的步骤代码为**未注释**状态
   - 所有已确认通过的步骤必须**注释掉**
   - 所有后续步骤必须**注释掉**

2. **调试流程**
   ```
   步骤N调试:
   1. 注释步骤1到N-1（已确认通过）
   2. 只保留步骤N未注释（当前调试）
   3. 执行测试
   4. 用户确认 "ok"
   5. 注释步骤N
   6. 进入步骤N+1调试
   ```

3. **正确示例**
   ```python
   def process(self):
       # 步骤1-9已确认通过，全部注释
       # Step('9.点击评论输入框')
       # self.driver.touch((499, 2526))

       # 只保留步骤10（当前调试）
       Step('10.点击评论输入区域')
       self.driver.touch((332, 2366))

       # 步骤11待调试，必须注释
       # Step('11.输入评论"666"')
   ```

## 错误分类

| 错误类型 | 根因 | 处理策略 |
|---------|------|---------|
| ELEMENT_NOT_FOUND | 控件不存在或定位器错误 | 尝试备用定位器，检查控件树 |
| TIMEOUT | 操作超时 | 增加等待时间，检查网络/性能 |
| PERMISSION_DENIED | 权限不足 | 检查应用权限配置 |
| APP_CRASH | 应用崩溃 | 检查日志，修复应用问题 |
| STALE_ELEMENT | 控件已过期 | 重新查找控件 |
| INVALID_STATE | 状态不正确 | 检查前置条件 |

## 修正策略（优先级）

**策略 1: 备用定位器**
```
text → key → id → type → description → bounds
```

**策略 2: 增加等待时间**
```python
component = driver.wait_for_component(BY.text("目标"), timeout=10000)
```

**策略 3: 截图 AI 识别**
- 当控件树完全无法定位时使用
- 分析截图识别目标位置
- 返回坐标供坐标操作使用

**策略 4: 坐标操作降级**
```python
driver.touch((x, y))
```

## 控件视觉识别

分析截图时参考 [控件视觉识别指南](control-visual-guide.md) 快速识别无文字控件:
- 点赞按钮: ❤️ 心形，位于内容下方
- 收藏按钮: ⭐ 五角星形状
- 分享按钮: ↗️ 弯曲箭头
- 搜索框: 🔍 放大镜，位于顶部
- 评论框: 方形气泡/"说点什么"，位于底部

## 生成重试脚本

```python
def retry_step(driver):
    # 策略 1: 使用备用定位器
    try:
        component = driver.wait_for_component(BY.key("alt_locator"), timeout=10000)
        driver.touch(component)
        return True
    except Exception:
        pass

    # 策略 2: 增加等待时间
    driver.wait(2)

    # 策略 3: 坐标操作 (降级方案)
    driver.touch((540, 1200))
    return True
```

## 输出格式

```json
{
  "success": true,
  "root_cause": "ELEMENT_NOT_FOUND",
  "analysis": "定位器 BY.text('登录') 在当前控件树中未找到匹配项",
  "suggestions": [
    {"type": "ALTERNATIVE_LOCATOR", "detail": "使用 BY.key('login_btn')", "code": "driver.touch(BY.key('login_btn'))"}
  ],
  "fixed_step": {"step_id": 1, "action": "click", "target": {"locator": "key", "value": "login_btn"}},
  "retry_script_path": "{PROJECT_ROOT}/output/temp/retry_*.py"
}
```
