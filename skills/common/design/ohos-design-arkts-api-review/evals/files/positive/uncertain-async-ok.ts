// Eval file for rule: 执行时长受外界影响且不确定的，API只提供异步方式
// 正例1：网络请求只提供异步方式
async function httpRequest(url: string, options?: RequestOptions): Promise<Response> {
  const response = await fetch(url, options);
  return response;
}

// 正例2：地理位置查询只提供异步方式
async function getCurrentLocation(): Promise<Location> {
  return new Promise((resolve, reject) => {
    navigator.geolocation.getCurrentPosition(
      (position) => resolve(position.coords),
      (error) => reject(error)
    );
  });
}

// 正例3：WiFi扫描只提供异步方式
async function scanWiFi(): Promise<WiFiNetwork[]> {
  return new Promise((resolve, reject) => {
    wifiScanner.startScan((networks) => {
      resolve(networks);
    }, (error) => {
      reject(error);
    });
  });
}

// 正例4：用户交互只提供异步方式
async function requestPermission(permission: string): Promise<boolean> {
  return new Promise((resolve) => {
    showDialog({
      title: 'Permission Required',
      message: `Grant ${permission} permission?`,
      onConfirm: () => resolve(true),
      onCancel: () => resolve(false)
    });
  });
}

// 正例5：文件选择对话框只提供异步方式
async function selectFile(options?: FileSelectOptions): Promise<File[]> {
  return new Promise((resolve, reject) => {
    filePicker.show(options, (files) => {
      resolve(files);
    }, (error) => {
      reject(error);
    });
  });
}

// 正例6：后台任务只提供异步方式
async function runBackgroundTask(task: BackgroundTask): Promise<TaskResult> {
  return new Promise((resolve, reject) => {
    taskRunner.run(task, (result) => {
      resolve(result);
    }, (error) => {
      reject(error);
    });
  });
}

// 正例7：蓝牙扫描只提供异步方式
async function scanBluetooth(): Promise<BluetoothDevice[]> {
  return new Promise((resolve, reject) => {
    bluetoothScanner.startScan((devices) => {
      resolve(devices);
    }, (error) => {
      reject(error);
    });
  });
}

// 正例8：推送通知只提供异步方式
async function requestNotificationPermission(): Promise<boolean> {
  return new Promise((resolve) => {
    notificationService.requestPermission((granted) => {
      resolve(granted);
    });
  });
}
