// Eval file for rule: 命名使用肯定表达式
// 正例1：使用肯定表达的布尔属性
interface ConnectionState {
  isConnected: boolean;      // 清晰：是否已连接
  isEnabled: boolean;         // 清晰：是否已启用
  isAvailable: boolean;       // 清晰：是否可用
  isHidden: boolean;          // 清晰：是否隐藏
  isClosed: boolean;          // 清晰：是否关闭
  isInvalid: boolean;         // 清晰：是否无效
}

// 正例2：使用肯定表达的函数命名
function enableFeature(): void { }      // 清晰：启用功能
function showElement(): void { }         // 清晰：显示元素
function openConnection(): void { }      // 清晰：打开连接
function activateUser(): void { }        // 清晰：激活用户

// 正例3：合理的对仗函数命名（无需检出）
function subscribe(callback: Callback): void { }
function unsubscribe(callback: Callback): void { }  // 与subscribe对仗，无需修改

function register(id: string): void { }
function unregister(id: string): void { }           // 与register对仗，无需修改

function lock(): void { }
function unlock(): void { }                         // 业界通用对仗，无需修改

// 正例4：业界通用惯例的否定前缀（无需检出）
function disconnect(): void { }       // 业界通用，与connect对仗
function undo(): void { }             // 业界通用操作
function unmount(): void { }          // 业界通用，与mount对仗
function unlink(): void { }           // 业界通用，与link对仗
