// Eval file for rule: 禁止创建空interface
// 反例1：完全空的interface
/**
 * 空接口 - 没有任何定义
 */
interface EmptyInterface {
}

// 反例2：只有注释的interface
/**
 * 占位接口
 * TODO: 后续补充定义
 */
interface PlaceholderInterface {
  // 待添加
}

// 反例3：空的泛型interface
/**
 * 泛型空接口
 */
interface GenericEmpty<T> {
}

// 反例4：继承但不添加任何新成员的interface
/**
 * 只继承不扩展
 */
interface NoNewMembers extends UserInfo {
}

// 反例5：只有空行的interface
/**
 * 带空行的空接口
 */
interface BlankLines {


}

// 反例6：使用分号但无实际内容的interface
/**
 * 分号形式的空接口
 */
interface SemicolonEmpty {
  ;
  ;
}

// 反例7：多个连续空interface
/**
 * 第一个空接口
 */
interface FirstEmpty {
}

/**
 * 第二个空接口
 */
interface SecondEmpty {
}

// 反例8：嵌套在命名空间中的空interface
namespace ApiTypes {
  /**
   * 空的嵌套接口
   */
  interface NestedEmpty {
  }
}

// 反例9：导出的空interface
/**
 * 导出的空接口
 */
export interface ExportedEmpty {
}
