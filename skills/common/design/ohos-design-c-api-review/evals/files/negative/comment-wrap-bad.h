// Eval file for rule: 注释包裹规范
// 反例1：关键字未使用包裹格式
/**
 * The default value is 0.
 */
// 问题：应明确0是代码字面量

// 反例2：true/false未使用包裹格式
/**
 * true means enabled, false means disabled.
 */
// 问题：true/false作为字面量应有明确格式

// 反例3：{@link}被反引号包裹（错误）
/**
 * Call `{@link close}` method to release resources.
 */
// 问题：{@link}标签不应使用反引号包裹

// 反例4：源码符号未包裹
/**
 * Call the setEnabled method with true to enable.
 */
// 问题：setEnabled是函数名，应使用标准格式
