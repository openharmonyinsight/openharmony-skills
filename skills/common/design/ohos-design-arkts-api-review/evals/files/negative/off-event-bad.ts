// Eval file for rule: 取消事件订阅方法名前缀必须为offXXX
// 反例1：取消事件订阅方法名不以off开头，使用remove前缀
class EventEmitter {
  /**
   * 取消订阅数据变化事件
   */
  removeDataChange(callback: (data: any) => void): void {
    const index = this.dataCallbacks.indexOf(callback);
    if (index > -1) {
      this.dataCallbacks.splice(index, 1);
    }
  }
}

// 反例2：取消事件订阅方法名不以off开头，使用un前缀
class Button {
  /**
   * 取消监听点击事件
   */
  unClick(): void {
    this.clickCallback = null;
  }
}

// 反例3：取消事件订阅方法名不以off开头，使用detach前缀
class MessageManager {
  /**
   * 取消订阅消息
   */
  detachMessage(callback: (message: string) => void): void {
    this.messageCallbacks.delete(callback);
  }
}

// 反例4：取消事件订阅方法名不以off开头，使用deregister前缀
class FileWatcher {
  /**
   * 取消监听文件变化事件
   */
  deregisterFileChanged(callback: (filePath: string) => void): void {
    this.fileChangeCallbacks.delete(callback);
  }
}
