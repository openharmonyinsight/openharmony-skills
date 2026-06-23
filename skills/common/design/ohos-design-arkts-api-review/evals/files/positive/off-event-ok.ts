// Eval file for rule: 取消事件订阅方法名前缀必须为offXXX
// 正例1：取消事件订阅方法名以off开头
class EventEmitter {
  /**
   * 取消订阅数据变化事件
   */
  offDataChange(callback: (data: any) => void): void {
    const index = this.dataCallbacks.indexOf(callback);
    if (index > -1) {
      this.dataCallbacks.splice(index, 1);
    }
  }
}

// 正例2：取消事件监听方法
class Button {
  /**
   * 取消监听点击事件
   */
  offClick(): void {
    this.clickCallback = null;
  }
}

// 正例3：取消消息订阅方法
class MessageManager {
  /**
   * 取消订阅消息
   */
  offMessage(callback: (message: string) => void): void {
    this.messageCallbacks.delete(callback);
  }
}
