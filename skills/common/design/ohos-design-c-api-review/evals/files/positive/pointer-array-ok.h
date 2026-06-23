// Eval file for rule: 指针数组属性明确化
// 正例1：指向单个对象的指针
/**
 * @param configs Pointer to the child process configs object to be destroyed.
 */
int32_t DestroyChildProcessConfigs(ChildProcessConfig* configs);

// 正例2：指向数组的指针
/**
 * @param array Indicates the pointer to a Pixelmap array.
 * @param count Number of elements in the array.
 */
int32_t SetPixelmapArray(Pixelmap** array, int32_t count);

// 正例3：指向单个结构体的指针
/**
 * @param nodeEvent Indicates the pointer to an ArkUI_NodeEvent object.
 */
int32_t ProcessNodeEvent(ArkUI_NodeEvent* nodeEvent);

// 正例4：说明数组边界
/**
 * @param durations Indicates the pointer to the frame duration array.
 * @param count Number of frame durations.
 */
int32_t SetFrameDurations(int32_t* durations, int32_t count);

// 正例5：指向缓冲区的指针
/**
 * @param buffer Pointer to the output buffer.
 * @param bufferSize Size of the buffer in bytes.
 */
int32_t ReadData(void* buffer, size_t bufferSize);
