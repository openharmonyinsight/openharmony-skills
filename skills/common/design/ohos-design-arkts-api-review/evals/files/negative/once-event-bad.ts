// Eval file for rule: 一次性事件订阅方法名前缀必须为onceXXX
// 反例1：一次性事件订阅方法名不以once开头，使用listenOnce前缀
class EventEmitter {
  /**
   * 订阅数据变化事件（一次性）
   */
  listenOnceDataChange(callback: (data: any) => void): void {
    const wrappedCallback = (data: any) => {
      callback(data);
      this.offDataChange(wrappedCallback);
    };
    this.onDataChange(wrappedCallback);
  }
}

// 反例2：一次性点击事件监听方法名不以once开头，使用subscribeOnce前缀
class Button {
  /**
   * 监听点击事件（一次性）
   */
  subscribeOnceClick(callback: () => void): void {
    const wrappedCallback = () => {
      callback();
      this.offClick();
    };
    this.onClick(wrappedCallback);
  }
}

// 反例3：一次性消息订阅方法名不以once开头，使用addOnce前缀
class MessageManager {
  /**
   * 订阅消息（一次性）
   */
  addOnceMessage(callback: (message: string) => void): void {
    const wrappedCallback = (message: string) => {
      callback(message);
      this.offMessage(wrappedCallback);
    };
    this.onMessage(wrappedCallback);
  }
}

// 反例4：一次性状态变化监听方法名不以once开头，使用registerOnce前缀
class StateManager {
  /**
   * 监听状态变化（一次性）
   */
  registerOnceStateChanged(callback: (newState: string) => void): void {
    const wrappedCallback = (newState: string) => {
      callback(newState);
      this.offStateChanged(wrappedCallback);
    };
    this.onStateChanged(wrappedCallback);
  }
}
