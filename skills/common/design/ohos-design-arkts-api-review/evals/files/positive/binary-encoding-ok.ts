// Eval file for rule: Byte[]/ArrayBuffer/Uint8Array类型给出编码格式
// 正例1：图片数据明确标注编码格式
/**
 * 获取图片数据
 * @param imageId 图片ID
 * @returns 图片数据，编码格式为JPEG
 */
function getImageData(imageId: string): ArrayBuffer;

// 正例2：字符数据明确标注编码格式
/**
 * 获取文本内容
 * @param fileId 文件ID
 * @returns 文本内容，编码格式为UTF-8
 */
function getTextContent(fileId: string): Uint8Array;

// 正例3：音频数据明确标注编码格式
/**
 * 获取音频数据
 * @param audioId 音频ID
 * @returns 音频数据，编码格式为PCM，采样率16kHz，16位有符号整数
 */
function getAudioData(audioId: string): ArrayBuffer;

// 正例4：视频帧数据明确标注编码格式
/**
 * 获取视频帧数据
 * @param frameIndex 帧索引
 * @returns 帧数据，编码格式为NV21（YUV420SP）
 */
function getVideoFrame(frameIndex: number): Uint8Array;

// 正例5：压缩数据明确标注编码格式
/**
 * 获取压缩数据
 * @param dataId 数据ID
 * @returns 压缩数据，编码格式为GZIP
 */
function getCompressedData(dataId: string): ArrayBuffer;

// 正例6：通过参数指定编码格式
/**
 * 读取文件内容
 * @param filePath 文件路径
 * @param encoding 编码格式，如'utf-8'、'gbk'、'base64'等
 * @returns 文件内容数据
 */
function readFile(filePath: string, encoding: string): Uint8Array;

// 正例7：通过返回类型结构包含编码信息
interface ImageData {
  data: ArrayBuffer;
  encoding: 'jpeg' | 'png' | 'webp' | 'bmp';
}

function getImage(id: string): ImageData;
