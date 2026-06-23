// Eval file for rule: 事件订阅方法名前缀必须为onXXX
// 正例1：事件订阅方法名以on开头
class EventEmitter {
  /**
   * 订阅数据变化事件
   */
  onDataChange(callback: (data: any) => void): void {
    this.dataCallbacks.push(callback);
  }
}

// 正例2：事件监听方法
class Button {
  /**
   * 监听点击事件
   */
  onClick(callback: () => void): void {
    this.clickCallback = callback;
  }
}

// 正例3：消息订阅方法
class MessageManager {
  /**
   * 订阅消息
   */
  onMessage(callback: (message: string) => void): void {
    this.messageCallbacks.add(callback);
  }
}
