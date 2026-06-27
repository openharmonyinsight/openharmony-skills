// Eval file for rule: Byte[]/ArrayBuffer/Uint8Array类型给出编码格式
// 反例1：图片数据未标注编码格式
/**
 * 获取图片数据
 * @param imageId 图片ID
 * @returns 图片数据
 */
function getImageData(imageId: string): ArrayBuffer;
// 错误：图片数据可能涉及多种编码格式（JPEG、PNG、BMP等），未明确标注编码格式

// 反例2：字符数据未标注编码格式
/**
 * 获取文本内容
 * @param fileId 文件ID
 * @returns 文本内容
 */
function getTextContent(fileId: string): Uint8Array;
// 错误：文本内容可能涉及多种字符编码（UTF-8、GBK、ISO-8859-1等），未明确标注编码格式

// 反例3：音频数据未标注编码格式
/**
 * 获取音频数据
 * @param audioId 音频ID
 * @returns 音频数据
 */
function getAudioData(audioId: string): ArrayBuffer;
// 错误：音频数据可能涉及多种编码格式（PCM、MP3、AAC等），未明确标注编码格式

// 反例4：视频帧数据未标注编码格式
/**
 * 获取视频帧数据
 * @param frameIndex 帧索引
 * @returns 帧数据
 */
function getVideoFrame(frameIndex: number): Uint8Array;
// 错误：视频帧数据可能涉及多种编码格式（NV21、NV12、I420等），未明确标注编码格式

// 反例5：压缩数据未标注编码格式
/**
 * 获取压缩数据
 * @param dataId 数据ID
 * @returns 压缩数据
 */
function getCompressedData(dataId: string): ArrayBuffer;
// 错误：压缩数据可能涉及多种编码格式（GZIP、ZLIB、LZ4等），未明确标注编码格式

// 反例6：二进制数据未说明格式
/**
 * 下载文件
 * @param url 下载地址
 * @returns 文件二进制数据
 */
function downloadFile(url: string): ArrayBuffer;
// 错误：文件二进制数据的格式未知，开发者无法正确处理
