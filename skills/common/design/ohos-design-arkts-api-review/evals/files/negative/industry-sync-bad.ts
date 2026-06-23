// Eval file for rule: 与业界同步API名称且功能一致的API只提供同步方式
// 反例1：日志打印不应提供异步版本
async function logAsync(message: string): Promise<void> {
  return new Promise((resolve) => {
    setTimeout(() => {
      console.log(message);
      resolve();
    }, 0);
  });
}

// 反例2：事件订阅不应提供异步版本
async function onAsync(eventType: string, handler: EventHandler): Promise<void> {
  return new Promise((resolve) => {
    // 异步注册事件
    setTimeout(() => {
      eventRegistry.add(eventType, handler);
      resolve();
    }, 0);
  });
}

// 反例3：数组操作不应提供异步版本（如果业界只有同步版本）
async function pushAsync<T>(arr: T[], item: T): Promise<number> {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(arr.push(item));
    }, 0);
  });
}

// 反例4：JSON操作不应提供异步版本
async function parseJSONAsync(json: string): Promise<object> {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(JSON.parse(json));
    }, 0);
  });
}

// 反例5：数学运算不应提供异步版本
async function maxAsync(...values: number[]): Promise<number> {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(Math.max(...values));
    }, 0);
  });
}

// 反例6：日期操作不应提供异步版本
async function getTimeAsync(date: Date): Promise<number> {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(date.getTime());
    }, 0);
  });
}

// 反例7：字符串操作不应提供异步版本
async function toUpperCaseAsync(str: string): Promise<string> {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(str.toUpperCase());
    }, 0);
  });
}

// 反例8：同时提供同步和异步版本（当业界只有同步版本时）
class EventEmitter {
  // 业界只有同步版本
  on(eventType: string, handler: EventHandler): void { }

  // 不应提供异步版本
  async onAsync(eventType: string, handler: EventHandler): Promise<void> { }
}
