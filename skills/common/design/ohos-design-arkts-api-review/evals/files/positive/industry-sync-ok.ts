// Eval file for rule: 与业界同步API名称且功能一致的API只提供同步方式
// 正例1：日志打印（业界同步API）
console.log('message');
console.error('error message');
console.warn('warning message');
console.info('info message');

// 正例2：事件订阅（业界同步API）
eventEmitter.on('event', handler);
eventEmitter.off('event', handler);
eventEmitter.once('event', handler);

// 正例3：数组操作（业界同步API）
const arr = [1, 2, 3];
arr.push(4);
arr.pop();
arr.shift();
arr.unshift(0);
const filtered = arr.filter(x => x > 1);
const mapped = arr.map(x => x * 2);

// 正例4：对象操作（业界同步API）
const obj = { a: 1, b: 2 };
const keys = Object.keys(obj);
const values = Object.values(obj);
const entries = Object.entries(obj);
const merged = Object.assign({}, obj, { c: 3 });

// 正例5：JSON操作（业界同步API）
const json = JSON.stringify({ a: 1 });
const obj2 = JSON.parse(json);

// 正例6：数学运算（业界同步API）
const max = Math.max(1, 2, 3);
const min = Math.min(1, 2, 3);
const abs = Math.abs(-5);
const round = Math.round(3.5);

// 正例7：日期操作（业界同步API）
const now = new Date();
const timestamp = now.getTime();
const year = now.getFullYear();
const month = now.getMonth();

// 正例8：字符串操作（业界同步API）
const str = 'hello';
const upper = str.toUpperCase();
const lower = str.toLowerCase();
const trimmed = str.trim();
const split = str.split('');
