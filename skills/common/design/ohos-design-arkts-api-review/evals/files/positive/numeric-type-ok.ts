// Eval file for rule: 合理使用数值类型
// 正例1：使用数值类型表示年龄
interface Person {
  age: int;  // 年龄，用于比较和计算
}

// 正例2：使用数值类型表示金额
interface Product {
  price: double;  // 价格，用于计算
  quantity: double;  // 数量，用于计算
}

// 正例3：使用数值类型表示尺寸
interface View {
  width: int;   // 宽度，用于布局计算
  height: int;  // 高度，用于布局计算
}

// 正例4：函数参数使用数值类型
/**
 * 计算总价
 * @param price 单价
 * @param count 数量
 * @returns 总价
 */
function calculateTotal(price: double, count: int): double {
  return price * count;
}

// 正例5：使用数值类型表示索引
function getItemByIndex(index: int): Item {
  // 实现...
}

// 正例6：使用数值类型表示百分比
interface Progress {
  percent: int;  // 0-100的数值
}
