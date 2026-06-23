// Eval file for rule: 合理使用数值类型
// 反例1：使用字符串表示年龄
interface Person {
  age: string;  // 错误：年龄需要比较和计算，应使用 int
}

// 反例2：使用字符串表示金额
interface Product {
  price: string;  // 错误：价格需要计算，应使用 double
}

// 反例3：使用字符串表示尺寸
interface View {
  width: string;   // 错误：宽度需要布局计算，应使用 int
  height: string;  // 错误：高度需要布局计算，应使用 int
}

// 反例4：函数参数使用字符串表示数值
function calculateTotal(price: string, count: string): string {
  // 错误：数值参数应使用数值类型
  return (parseFloat(price) * parseInt(count)).toString();
}

// 反例5：使用字符串表示索引
function getItemByIndex(index: string): Item {
  // 错误：索引应使用 int 类型
}
