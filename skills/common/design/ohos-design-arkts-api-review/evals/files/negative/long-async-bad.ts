// Eval file for rule: 执行时间长且受外界影响小的API优先提供异步方式
// 反例1：文件IO只提供同步方式
function readFile(path: string): string {
  return fs.readFileSync(path, 'utf-8');  // 应优先提供异步方式
}

// 反例2：数据库操作只提供同步方式
function queryDatabase(sql: string, params?: any[]): any[] {
  return db.querySync(sql, params);  // 应优先提供异步方式
}

// 反例3：图片解码只提供同步方式
function decodeImage(buffer: Buffer): Image {
  return imageDecoder.decodeSync(buffer);  // 应优先提供异步方式
}

// 反例4：音视频解码只提供同步方式
function decodeVideo(buffer: Buffer): VideoFrames {
  return videoDecoder.decodeSync(buffer);  // 应优先提供异步方式
}

// 反例5：IPC通信只提供同步方式
function callRemoteService(service: string, method: string, params: any): any {
  return ipcClient.callSync(service, method, params);  // 应优先提供异步方式
}

// 反例6：大文件处理只提供同步方式
function processLargeFile(path: string): ProcessResult {
  return fileProcessor.processSync(path);  // 应优先提供异步方式
}

// 反例7：压缩解压缩只提供同步方式
function compressFile(source: string, target: string): void {
  return compressor.compressSync(source, target);  // 应优先提供异步方式
}

// 反例8：加密解密只提供同步方式
function encrypt(data: Buffer, key: string): Buffer {
  return crypto.encryptSync(data, key);  // 应优先提供异步方式
}

// 反例9：优先提供同步方式，异步方式作为补充（应相反）
class FileReader {
  // 同步版本作为主要API（错误）
  read(path: string): string {
    return fs.readFileSync(path, 'utf-8');
  }

  // 异步版本作为补充（错误，应优先提供异步方式）
  async readAsync(path: string): Promise<string> {
    return await fs.readFile(path, 'utf-8');
  }
}
