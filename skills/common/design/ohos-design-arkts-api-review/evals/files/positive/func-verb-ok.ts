// Eval file for rule: 函数名称应该是动词或动宾/介宾结构
// 正例1：动词结构
function start(): void { }
function stop(): void { }
function pause(): void { }
function resume(): void { }
function run(): void { }
function execute(): void { }

// 正例2：动宾结构
function createUser(): User { }
function sendMessage(): void { }
function getData(): Data { }
function startService(): void { }
function stopProcess(): void { }
function loadConfig(): Config { }

// 正例3：介宾结构
function onConfigurationUpdated(): void { }
function onEventReceived(): void { }
function onClick(): void { }
function beforeShutdown(): void { }
function afterLogin(): void { }

// 正例4：动介宾结构
function connectToServer(): void { }
function sendToQueue(): void { }
function readFromFile(): Data { }
function writeToFile(): void { }
function getFromCache(): Data { }

// 正例5：复合动宾结构
function startBootProcess(): void { }
function createUserSession(): Session { }
function initializeSystemConfig(): void { }
function validateUserInput(): boolean { }
