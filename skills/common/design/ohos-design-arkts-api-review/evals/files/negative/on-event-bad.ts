// Eval file for rule: 事件订阅方法名前缀必须为onXXX
// 反例1：事件订阅方法名不以on开头，使用listen前缀
class EventEmitter {
  /**
   * 订阅数据变化事件
   */
  listenDataChange(callback: (data: any) => void): void {
    this.dataCallbacks.push(callback);
  }
}

// 反例2：事件订阅方法名不以on开头，使用subscribe前缀
class Button {
  /**
   * 监听点击事件
   */
  subscribeClick(callback: () => void): void {
    this.clickCallback = callback;
  }
}

// 反例3：事件订阅方法名不以on开头，使用register前缀
class StateManager {
  /**
   * 监听状态变化
   */
  registerStateChanged(callback: (newState: string) => void): void {
    this.stateCallbacks.push(callback);
  }
}

// 反例4：事件订阅方法名以On开头但首字母大写
class NetworkManager {
  /**
   * 监听连接事件
   */
  OnConnected(callback: () => void): void {
    this.connectedCallbacks.push(callback);
  }
}
