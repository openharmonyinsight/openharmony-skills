// Eval file for rule: Byte[]/ArrayBuffer/Uint8Array类型给出编码格式
// 反例1：图片数据未标注编码格式
/**
 * @brief 获取图片数据
 * @param imageId 图片ID
 * @param dataLen 输出参数，返回数据长度
 * @return 图片数据
 */
Byte* GetImageDataBad(const char* imageId, size_t* dataLen);
// 错误：图片数据可能涉及多种编码格式（JPEG、PNG、BMP等），未明确标注编码格式

// 反例2：字符数据未标注编码格式
/**
 * @brief 获取文本内容
 * @param fileId 文件ID
 * @param dataLen 输出参数，返回数据长度
 * @return 文本内容
 */
Byte* GetTextContentBad(const char* fileId, size_t* dataLen);
// 错误：文本内容可能涉及多种字符编码（UTF-8、GBK、ISO-8859-1等），未明确标注编码格式

// 反例3：音频数据未标注编码格式
/**
 * @brief 获取音频数据
 * @param audioId 音频ID
 * @param dataLen 输出参数，返回数据长度
 * @return 音频数据
 */
Byte* GetAudioDataBad(const char* audioId, size_t* dataLen);
// 错误：音频数据可能涉及多种编码格式（PCM、MP3、AAC等），未明确标注编码格式

// 反例4：视频帧数据未标注编码格式
/**
 * @brief 获取视频帧数据
 * @param frameIndex 帧索引
 * @param dataLen 输出参数，返回数据长度
 * @return 帧数据
 */
Byte* GetVideoFrameBad(int frameIndex, size_t* dataLen);
// 错误：视频帧数据可能涉及多种编码格式（NV21、NV12、I420等），未明确标注编码格式

// 反例5：压缩数据未标注编码格式
/**
 * @brief 获取压缩数据
 * @param dataId 数据ID
 * @param dataLen 输出参数，返回数据长度
 * @return 压缩数据
 */
Byte* GetCompressedDataBad(const char* dataId, size_t* dataLen);
// 错误：压缩数据可能涉及多种编码格式（GZIP、ZLIB、LZ4等），未明确标注编码格式

// 反例6：二进制数据未说明格式
/**
 * @brief 下载文件
 * @param url 下载地址
 * @param dataLen 输出参数，返回数据长度
 * @return 文件二进制数据
 */
Byte* DownloadFileBad(const char* url, size_t* dataLen);
// 错误：文件二进制数据的格式未知，开发者无法正确处理
