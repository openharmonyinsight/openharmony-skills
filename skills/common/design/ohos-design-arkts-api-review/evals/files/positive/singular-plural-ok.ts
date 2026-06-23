// Eval file for rule: 名词的单复数和接口语义匹配
// 正例1：返回单个对象使用单数
function getUser(): User { }
function getConfig(): Config { }
function getMessage(): Message { }

// 正例2：返回数组使用复数
function getUsers(): User[] { }
function getConfigs(): Config[] { }
function getMessages(): Message[] { }

// 正例3：关注整体使用单数
function getEventMap(): Map<string, Event> { }  // 关注Map整体，使用单数
function getOptionList(): Option[] { }  // 关注List整体，使用单数
function getUserCollection(): User[] { }  // 关注Collection整体，使用单数

// 正例4：关注子元素使用复数
function pushOptions(options: Option[]): void { }  // 关注多个配置项，使用复数
function setItems(items: Item[]): void { }  // 关注多个元素，使用复数
function addMessages(messages: Message[]): void { }  // 关注多条消息，使用复数

// 正例5：语义明确
// 返回单个用户
function getUserById(id: string): User { }

// 返回多个用户
function getUsersByIds(ids: string[]): User[] { }

// 返回用户列表（关注整体）
function getUserList(): User[] { }

// 返回用户数组（关注元素）
function getUsers(): User[] { }
