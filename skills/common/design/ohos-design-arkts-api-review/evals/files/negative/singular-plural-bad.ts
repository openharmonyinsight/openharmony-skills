// Eval file for rule: 名词的单复数和接口语义匹配
// 反例1：返回单个对象使用复数
function getUsers(): User { }  // 返回单个对象，应改为getUser
function getConfigs(): Config { }  // 返回单个对象，应改为getConfig
function getMessages(): Message { }  // 返回单个对象，应改为getMessage

// 反例2：返回数组使用单数
function getUser(): User[] { }  // 返回数组，应改为getUsers
function getConfig(): Config[] { }  // 返回数组，应改为getConfigs
function getMessage(): Message[] { }  // 返回数组，应改为getMessages

// 反例3：关注整体但使用复数
function getEventMaps(): Map<string, Event> { }  // 返回单个Map，应改为getEventMap
function getOptionLists(): Option[] { }  // 返回单个List，应改为getOptionList

// 反例4：关注子元素但使用单数
function pushOption(options: Option[]): void { }  // 参数是复数，应改为pushOptions
function setItem(items: Item[]): void { }  // 参数是复数，应改为setItems
function addMessage(messages: Message[]): void { }  // 参数是复数，应改为addMessages

// 反例5：语义不匹配
// 错误：返回单个对象，但使用复数
view.getEventMaps()  // return a map，应为getEventMap

// 正确：返回单个Map
view.getEventMap()

// 错误：options是一个对象，但使用单数
router.push(url, option)  // options是一个对象，以kv的形式保存一些配置项

// 正确：使用复数
router.push(url, options)
