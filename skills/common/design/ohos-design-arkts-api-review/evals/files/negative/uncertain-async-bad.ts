// Eval file for rule: 执行时长受外界影响且不确定的，API只提供异步方式
// 反例1：网络请求提供同步方式
function httpRequestSync(url: string, options?: RequestOptions): Response {
  // 同步网络请求，阻塞线程
  const xhr = new XMLHttpRequest();
  xhr.open('GET', url, false);  // false表示同步
  xhr.send();
  return xhr.response;
}

// 反例2：地理位置查询提供同步方式
function getCurrentLocationSync(): Location {
  // 同步获取位置，无法实现或会阻塞线程
  let location: Location;
  navigator.geolocation.getCurrentPosition((position) => {
    location = position.coords;
  });
  return location;  // 返回undefined或阻塞
}

// 反例3：WiFi扫描提供同步方式
function scanWiFiSync(): WiFiNetwork[] {
  // 同步扫描WiFi，会阻塞线程
  let networks: WiFiNetwork[];
  wifiScanner.startScan((result) => {
    networks = result;
  });
  return networks;  // 返回undefined或阻塞
}

// 反例4：用户交互提供同步方式
function requestPermissionSync(permission: string): boolean {
  // 同步请求权限，会阻塞UI线程
  let granted = false;
  showDialog({
    title: 'Permission Required',
    message: `Grant ${permission} permission?`,
    onConfirm: () => granted = true,
    onCancel: () => granted = false
  });
  // 等待用户响应（阻塞）
  while (dialogIsOpen) {
    // 阻塞UI线程
  }
  return granted;
}

// 反例5：文件选择对话框提供同步方式
function selectFileSync(options?: FileSelectOptions): File[] {
  // 同步选择文件，会阻塞线程
  let files: File[];
  filePicker.show(options, (result) => {
    files = result;
  });
  return files;  // 返回undefined或阻塞
}

// 反例6：后台任务提供同步方式
function runBackgroundTaskSync(task: BackgroundTask): TaskResult {
  // 同步运行后台任务，会阻塞线程
  let result: TaskResult;
  taskRunner.run(task, (r) => {
    result = r;
  });
  return result;  // 返回undefined或阻塞
}

// 反例7：蓝牙扫描提供同步方式
function scanBluetoothSync(): BluetoothDevice[] {
  // 同步扫描蓝牙，会阻塞线程
  let devices: BluetoothDevice[];
  bluetoothScanner.startScan((result) => {
    devices = result;
  });
  return devices;  // 返回undefined或阻塞
}

// 反例8：同时提供同步和异步版本（对于执行时间不确定的API）
class HttpClient {
  // 异步版本（正确）
  async request(url: string): Promise<Response> {
    return await fetch(url);
  }

  // 同步版本（错误，不应提供）
  requestSync(url: string): Response {
    const xhr = new XMLHttpRequest();
    xhr.open('GET', url, false);
    xhr.send();
    return xhr.response;
  }
}
