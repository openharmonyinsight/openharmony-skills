// Eval file for rule: 禁止创建空class
// 正例1：有属性和方法的class
export class User {
  private name: string;
  private age: number;

  constructor(name: string, age: number) {
    this.name = name;
    this.age = age;
  }

  getName(): string {
    return this.name;
  }

  setAge(age: number): void {
    this.age = age;
  }
}

// 正例2：仅有构造函数的class也是合规的
export class Point {
  constructor(public x: number, public y: number) {}
}

// 正例3：有多个属性定义的class
export class Configuration {
  apiUrl: string = '';
  timeout: number = 5000;
  retryCount: number = 3;
  enableLog: boolean = false;
}

// 正例4：有方法的class
export class Calculator {
  add(a: number, b: number): number {
    return a + b;
  }

  subtract(a: number, b: number): number {
    return a - b;
  }
}

// 正例5：继承父类并添加新成员的class
export class AdminUser extends User {
  permissions: string[] = [];

  hasPermission(perm: string): boolean {
    return this.permissions.includes(perm);
  }
}

// 正例6：实现接口并添加成员的class
export class Logger implements ILogger {
  log(message: string): void {
    console.log(message);
  }

  error(message: string): void {
    console.error(message);
  }
}

// 正例7：有静态成员和实例成员的class
export class Database {
  private static instance: Database | null = null;
  private connection: Connection;

  private constructor() {
    this.connection = new Connection();
  }

  static getInstance(): Database {
    if (!Database.instance) {
      Database.instance = new Database();
    }
    return Database.instance;
  }

  query(sql: string): Result {
    return this.connection.execute(sql);
  }
}

// 正例8：泛型class有实际成员定义
export class Container<T> {
  private value: T;

  constructor(value: T) {
    this.value = value;
  }

  getValue(): T {
    return this.value;
  }

  setValue(value: T): void {
    this.value = value;
  }
}

// 正例9：抽象class有实际成员定义
export abstract class Animal {
  protected name: string;

  constructor(name: string) {
    this.name = name;
  }

  abstract makeSound(): void;

  move(): void {
    console.log(`${this.name} is moving`);
  }
}

// 正例10：有访问器的class
export class Temperature {
  private _celsius: number = 0;

  get celsius(): number {
    return this._celsius;
  }

  set celsius(value: number) {
    this._celsius = value;
  }

  get fahrenheit(): number {
    return this._celsius * 9 / 5 + 32;
  }
}

// 正例11：空class带继承
export class EmptyChild extends Parent {
}

// 正例12：空class带实现接口
export class Logger implements ILogger {
}
