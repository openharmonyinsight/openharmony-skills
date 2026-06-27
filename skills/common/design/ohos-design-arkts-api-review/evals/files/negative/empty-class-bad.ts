// Eval file for rule: 禁止创建空class
// 反例1：完全空的class
export class EmptyClass {
}

// 反例2：仅有注释的class
export class OnlyCommentsClass {
  // 这是一个没有任何实际内容的类
  // TODO: 后续补充实现
}

// 反例3：仅有类型参数的class
export class GenericContainer<T> {
}

// 反例4：多个类名声明但都是空的
export class Handler {
}

export class Processor {
}

// 反例5：空class带继承
export class EmptyChild extends Parent {
}

// 反例6：空class实现接口但不添加任何内容
export class EmptyImplementation implements IInterface {
}

// 反例7：abstract空class
export abstract class AbstractEmpty {
}

// 反例8：export default空class
export default class DefaultEmpty {
}

// 反例9：带有装饰器但空的class
@Decorator
export class DecoratedEmpty {
}

// 反例10：混合场景 - 一个文件中有多个空class
export class ConfigManager {
}

export class DataProcessor {
}

export class ResultHandler {
}
