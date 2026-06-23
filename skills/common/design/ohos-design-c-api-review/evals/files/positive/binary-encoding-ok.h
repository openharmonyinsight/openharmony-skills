// Eval file for rule: Byte[]/ArrayBuffer/Uint8Array类型给出编码格式
// 正例1：图片数据明确标注编码格式
/**
 * @brief 获取图片数据
 * @param imageId 图片ID
 * @param dataLen 输出参数，返回数据长度
 * @return 图片数据，编码格式为JPEG
 */
Byte* GetImageData(const char* imageId, size_t* dataLen);

// 正例2：字符数据明确标注编码格式
/**
 * @brief 获取文本内容
 * @param fileId 文件ID
 * @param dataLen 输出参数，返回数据长度
 * @return 文本内容，编码格式为UTF-8
 */
Byte* GetTextContent(const char* fileId, size_t* dataLen);

// 正例3：音频数据明确标注编码格式
/**
 * @brief 获取音频数据
 * @param audioId 音频ID
 * @param dataLen 输出参数，返回数据长度
 * @return 音频数据，编码格式为PCM，采样率16kHz，16位有符号整数
 */
Byte* GetAudioData(const char* audioId, size_t* dataLen);

// 正例4：视频帧数据明确标注编码格式
/**
 * @brief 获取视频帧数据
 * @param frameIndex 帧索引
 * @param dataLen 输出参数，返回数据长度
 * @return 帧数据，编码格式为NV21（YUV420SP）
 */
Byte* GetVideoFrame(int frameIndex, size_t* dataLen);

// 正例5：压缩数据明确标注编码格式
/**
 * @brief 获取压缩数据
 * @param dataId 数据ID
 * @param dataLen 输出参数，返回数据长度
 * @return 压缩数据，编码格式为GZIP
 */
Byte* GetCompressedData(const char* dataId, size_t* dataLen);

// 正例6：通过参数指定编码格式
/**
 * @brief 读取文件内容
 * @param filePath 文件路径
 * @param encoding 编码格式，如"utf-8"、"gbk"、"base64"等
 * @param dataLen 输出参数，返回数据长度
 * @return 文件内容数据
 */
Byte* ReadFileWithEncoding(const char* filePath, const char* encoding, size_t* dataLen);

// 正例7：通过返回结构包含编码信息
typedef struct {
    Byte* data;
    size_t dataLen;
    const char* encoding; // "jpeg", "png", "webp", "bmp"
} ImageData;

ImageData* GetImage(const char* id);
