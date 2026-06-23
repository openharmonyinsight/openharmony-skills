// Eval file for rule: 事件触发方法名称必须为emit
// 正例1：事件发射器使用emit方法
class EventEmitter {
  private listeners = new Map<string, Array<(data: any) => void>>();

  /**
   * 触发事件
   * @param eventName 事件名称
   * @param data 事件数据
   */
  emit(eventName: string, data: any): void {
    const callbacks = this.listeners.get(eventName);
    if (callbacks) {
      callbacks.forEach(callback => callback(data));
    }
  }
}

// 正例2：观察者模式使用emit方法
class Subject {
  private observers: Array<(data: any) => void> = [];

  /**
   * 通知所有观察者
   * @param data 通知数据
   */
  emit(data: any): void {
    this.observers.forEach(observer => observer(data));
  }
}

// 正例3：发布订阅模式使用emit方法
class PubSub {
  private subscribers = new Map<string, Array<(data: any) => void>>();

  /**
   * 发布事件
   * @param topic 主题
   * @param message 消息
   */
  emit(topic: string, message: any): void {
    const callbacks = this.subscribers.get(topic);
    if (callbacks) {
      callbacks.forEach(callback => callback(message));
    }
  }
}
