// Eval file for rule: 一次性事件订阅方法名前缀必须为onceXXX
// 正例1：一次性事件订阅方法名以once开头
class EventEmitter {
  /**
   * 订阅数据变化事件（一次性）
   */
  onceDataChange(callback: (data: any) => void): void {
    const wrappedCallback = (data: any) => {
      callback(data);
      this.offDataChange(wrappedCallback);
    };
    this.onDataChange(wrappedCallback);
  }
}

// 正例2：一次性事件监听方法
class Button {
  /**
   * 监听点击事件（一次性）
   */
  onceClick(callback: () => void): void {
    const wrappedCallback = () => {
      callback();
      this.offClick();
    };
    this.onClick(wrappedCallback);
  }
}

// 正例3：一次性消息订阅方法
class MessageManager {
  /**
   * 订阅消息（一次性）
   */
  onceMessage(callback: (message: string) => void): void {
    const wrappedCallback = (message: string) => {
      callback(message);
      this.offMessage(wrappedCallback);
    };
    this.onMessage(wrappedCallback);
  }
}
