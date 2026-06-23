// Eval file for rule: 约束限制合理
// 反例1：违背用户直觉/行业惯例 - 文件名不允许包含空格，但业界几乎所有系统都允许
/**
 * Save content to a file.
 *
 * @param { string } fileName - Name of the file. Cannot contain spaces.
 *   This is because the underlying storage system uses spaces as delimiters.
 * @param { string } content - Content to write.
 * @returns { Promise<void> }
 * @syscap SystemCapability.FileManagement.File.FileIO
 * @since 10
 */
function saveFile(fileName: string, content: string): Promise<void>;

// 反例2：无明确技术必要性 - @Builder嵌套使用要求内外入参对象一致，原因复杂难懂
/**
 * Custom component builder.
 *
 * @Builder
 * Note: When nesting @Builder decorators, the parameter objects of the inner and outer
 * @Builder methods must be exactly the same type. Otherwise, rendering will fail silently.
 * This is due to internal state management synchronization requirements in the framework's
 * rendering pipeline.
 *
 * @param { Object } params - Builder parameters.
 */
@Builder function MyBuilder(params: Object) { }

// 反例3：约束条件过多 - RelativeContainer描述了过多使用限制
/**
 * A relative layout container.
 *
 * Constraints:
 * 1. Child components must set at least one horizontal anchor and one vertical anchor.
 * 2. The anchor target must be the container or another child component within the container.
 * 3. Child components cannot reference themselves as anchors.
 * 4. Anchors cannot form circular references.
 * 5. The guideline must be set before being referenced by child components.
 * 6. The barrier must be set before being referenced by child components.
 * 7. When setting bias, the value must be between 0 and 1.
 * 8. Chain mode only supports Spread, SpreadInside, and Packed.
 * 9. Components in a chain must be positioned along the same axis.
 * 10. Weight values must be positive numbers.
 * 11. Match parent constraints cannot be combined with wrap content.
 * 12. Percent-based sizing requires the parent to have a defined size.
 *
 * @syscap SystemCapability.ArkUI.ArkUI.Full
 * @since 9
 */
class RelativeContainer { }

// 反例4：限制合理使用场景 - 上传图片强制限制 <= 1MB，但实际业务场景经常需要高清大图
/**
 * Upload an image to the server.
 *
 * @param { string } uri - Image URI. The image size must not exceed 1MB.
 *   If the image exceeds 1MB, an error will be thrown.
 * @param { ImageUploadOptions } options - Upload options.
 * @returns { Promise<UploadResult> }
 * @throws { BusinessError } 401 - Parameter error.
 * @throws { BusinessError } 1500001 - Image size exceeds 1MB limit.
 * @syscap SystemCapability.Multimedia.Image
 * @since 10
 */
function uploadImage(uri: string, options?: ImageUploadOptions): Promise<UploadResult>;

// 反例5：违背用户直觉 - 数组参数不允许为空数组，违背了"空数组表示无数据"的常见语义
/**
 * Set the list of selected items.
 *
 * @param { Array<string> } items - Selected item IDs. The array cannot be empty.
 *   An empty array will throw an error.
 * @syscap SystemCapability.ArkUI.ArkUI.Full
 * @since 10
 */
setSelectedItems(items: Array<string>): void;

// 反例6：无明确技术必要性 - 回调函数参数名必须和特定字符串完全匹配
/**
 * Register a listener for state changes.
 *
 * @param { string } type - Event type. Must be exactly "stateChange" (case-sensitive).
 *   Other values like "statechange" or "STATE_CHANGE" will be silently ignored.
 * @param { Callback<State> } callback - Callback function.
 * @syscap SystemCapability.Utils.Lang
 * @since 10
 */
on(type: string, callback: Callback<State>): void;

// 反例7：限制合理使用场景 - 连接超时设置的最大值过小，不能满足慢网络场景
/**
 * Set the HTTP connection timeout.
 *
 * @param { number } timeout - Timeout in milliseconds. The value must be between 1 and 5000 (5 seconds).
 * @syscap SystemCapability.Communication.NetStack
 * @since 10
 */
setConnectTimeout(timeout: number): void;

// 反例8：约束条件过多 - 单个接口声明了大量互斥的约束条件
/**
 * Create an animation with specific parameters.
 *
 * Constraints:
 * 1. Duration must be between 16ms and 1000ms.
 * 2. Delay must be a non-negative integer.
 * 3. Easing must be one of: linear, ease, ease-in, ease-out, ease-in-out, spring.
 * 4. Fill mode must be one of: none, forwards, backwards, both.
 * 5. Iteration count must be a positive integer or "infinite".
 * 6. Direction must be one of: normal, reverse, alternate, alternate-reverse.
 * 7. When direction is "alternate" or "alternate-reverse", iteration count must be greater than 1.
 * 8. Spring easing cannot be combined with "infinite" iteration count.
 * 9. Fill mode "backwards" requires a non-zero delay.
 * 10. The sum of duration and delay cannot exceed 3000ms.
 *
 * @param { AnimationOptions } options - Animation options.
 * @returns { Animation } Animation instance.
 * @syscap SystemCapability.ArkUI.ArkUI.Full
 * @since 10
 */
function createAnimation(options: AnimationOptions): Animation;
