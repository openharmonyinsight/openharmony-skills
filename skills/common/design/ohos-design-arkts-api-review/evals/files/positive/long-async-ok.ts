// Eval file for rule: 执行时间长且受外界影响小的API优先提供异步方式
// 正例1：文件IO操作优先提供异步方式
async function readFile(path: string): Promise<string> {
  return await fs.readFile(path, 'utf-8');
}

// 可选：补充同步方式
function readFileSync(path: string): string {
  return fs.readFileSync(path, 'utf-8');
}

// 正例2：数据库操作优先提供异步方式
async function queryDatabase(sql: string, params?: any[]): Promise<any[]> {
  return await db.query(sql, params);
}

// 可选：补充同步方式
function queryDatabaseSync(sql: string, params?: any[]): any[] {
  return db.querySync(sql, params);
}

// 正例3：图片解码优先提供异步方式
async function decodeImage(buffer: Buffer): Promise<Image> {
  return await imageDecoder.decode(buffer);
}

// 可选：补充同步方式
function decodeImageSync(buffer: Buffer): Image {
  return imageDecoder.decodeSync(buffer);
}

// 正例4：音视频解码优先提供异步方式
async function decodeVideo(buffer: Buffer): Promise<VideoFrames> {
  return await videoDecoder.decode(buffer);
}

// 可选：补充同步方式
function decodeVideoSync(buffer: Buffer): VideoFrames {
  return videoDecoder.decodeSync(buffer);
}

// 正例5：IPC通信优先提供异步方式
async function callRemoteService(service: string, method: string, params: any[]): Promise<any> {
  return await ipcClient.call(service, method, params);
}

// 可选：补充同步方式
function callRemoteServiceSync(service: string, method: string, params: any): any {
  return ipcClient.callSync(service, method, params);
}

// 正例6：大文件处理优先提供异步方式
async function processLargeFile(path: string): Promise<ProcessResult> {
  return await fileProcessor.process(path);
}

// 可选：补充同步方式
function processLargeFileSync(path: string): ProcessResult {
  return fileProcessor.processSync(path);
}

// 正例7：压缩解压缩优先提供异步方式
async function compressFile(source: string, target: string): Promise<void> {
  return await compressor.compress(source, target);
}

// 可选：补充同步方式
function compressFileSync(source: string, target: string): void {
  return compressor.compressSync(source, target);
}

// 正例8：加密解密优先提供异步方式
async function encrypt(data: Buffer, key: string): Promise<Buffer> {
  return await crypto.encrypt(data, key);
}

// 可选：补充同步方式
function encryptSync(data: Buffer, key: string): Buffer {
  return crypto.encryptSync(data, key);
}
