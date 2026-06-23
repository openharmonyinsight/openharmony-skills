// Eval file for rule: 禁止创建空属性接口
/**
 * 用户信息接口
 *
 * 正例说明：所有属性都有明确的类型定义和实际用途
 * - userId: 必需属性，用于业务逻辑中唯一标识用户
 * - userName: 必需属性，用于显示用户名称
 * - avatarUrl: 可选属性，用户可能未设置头像，但类型明确为string
 */
interface UserInfo {
  userId: string;  // 用户唯一标识，用于业务逻辑
  userName: string;  // 用户名称，显示用途
  avatarUrl?: string;  // 可选属性，有明确类型和用途
}

/**
 * 支付结果接口
 *
 * 正例说明：所有属性类型明确，可选属性有合理的业务场景
 * - orderId: 订单唯一标识，必需属性
 * - amount: 支付金额，必需属性
 * - timestamp: 支付时间戳，必需属性
 * - promotionId: 可选属性，部分支付方式可能无促销活动关联，类型明确为string
 */
interface PaymentResult {
  orderId: string;  // 订单ID
  amount: number;  // 支付金额
  timestamp: number;  // 支付时间戳
  // 可选属性，部分支付方式可能无此字段
  promotionId?: string;  // 关联的促销活动ID
}

/**
 * 配置选项接口
 *
 * 正例说明：所有可选属性都有明确的类型和合理的默认行为
 * - timeout: 超时时间，可选属性，不传时有默认值
 * - retries: 重试次数，可选属性，不传时有默认值
 * - enableCache: 是否启用缓存，可选属性，不传时有默认值
 */
interface ConfigOptions {
  timeout?: number;  // 超时时间，有默认值
  retries?: number;  // 重试次数，有默认值
  enableCache?: boolean;  // 是否启用缓存，有默认值
}

/**
 * API响应接口
 *
 * 正例说明：透传数据有明确的类型定义，不是any或unknown
 * - code: 响应状态码，必需属性
 * - message: 响应消息，必需属性
 * - data: 响应数据，使用明确的UserData类型而非any/unknown
 */
interface ApiResponse {
  code: number;  // 响应状态码
  message: string;  // 响应消息
  data: UserData;  // 响应数据，有明确的类型定义
}

/**
 * 事件载荷接口
 *
 * 正例说明：扩展属性有明确的类型约束
 * - eventType: 事件类型，必需属性
 * - payload: 扩展属性，使用Record<string, unknown>类型约束，而非直接使用unknown
 * - timestamp: 时间戳，必需属性
 */
interface EventPayload {
  eventType: string;
  payload: Record<string, unknown>;  // 扩展属性，有类型约束
  timestamp: number;
}

/**
 * 响应数据接口
 *
 * 正例说明：联合类型属性有明确的用途和类型定义
 * - status: 明确的联合类型，限定为三种状态
 * - result: 根据状态有不同类型，使用联合类型SuccessResult | ErrorResult
 */
interface ResponseData {
  status: 'success' | 'failed' | 'pending';  // 明确的联合类型
  result?: SuccessResult | ErrorResult;  // 根据状态有不同类型
}
