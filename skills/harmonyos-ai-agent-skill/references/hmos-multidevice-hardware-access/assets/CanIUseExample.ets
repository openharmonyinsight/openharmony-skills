
interface CapabilityResult {
  name: string;
  supported: boolean;
}

function checkLocationCapability() {
  try {
    if (canIUse("SystemCapability.Location.Location.Core")) {
      console.info("Location capability is supported");
    } else {
      console.info("Location capability is not supported");
    }
  } catch (err) {
    console.error(`Failed to check location capability: ${JSON.stringify(err)}`);
  }
}

function checkMultipleCapabilities(): CapabilityResult[] {
  const capabilities = [
    "SystemCapability.Location.Location.Core",
    "SystemCapability.Multimedia.Camera.Core",
    "SystemCapability.Communication.NFC.Core",
    "SystemCapability.Communication.Bluetooth.Core"
  ];

  const results: CapabilityResult[] = [];

  try {
    capabilities.forEach(cap => {
      try {
        const supported = canIUse(cap);
        const result: CapabilityResult = { name: cap, supported: supported };
        results.push(result);
        console.info(`${cap}: ${supported ? 'Supported' : 'Not Supported'}`);
      } catch (capErr) {
        console.error(`Failed to check ${cap}: ${JSON.stringify(capErr)}`);
        const result: CapabilityResult = { name: cap, supported: false };
        results.push(result);
      }
    });

    const supportedCount = results.filter(r => r.supported).length;
    console.info(`检查完成: ${supportedCount}/${capabilities.length} 个能力支持`);

    return results;
  } catch (err) {
    console.error(`Failed to check multiple capabilities: ${JSON.stringify(err)}`);
    return [];
  }
}

@Entry
@Component
struct CanIUseExample {
  @State checkResults: string = '';

  checkLocation() {
    checkLocationCapability();
  }

  checkAll() {
    const results = checkMultipleCapabilities();
    this.checkResults = results.map(r => `${r.name}: ${r.supported ? '✓' : '✗'}`).join('\n');
  }

  build() {
    Column() {
      Text('系统能力检查示例')
        .fontSize(20)
        .fontWeight(FontWeight.Bold)
        .margin({ top: 20, bottom: 20 })

      Button('检查位置服务能力')
        .onClick(() => {
          this.checkLocation();
        })
        .margin({ bottom: 10 })

      Button('检查多个系统能力')
        .onClick(() => {
          this.checkAll();
        })
        .margin({ bottom: 20 })

      if (this.checkResults) {
        Text(this.checkResults)
          .fontSize(12)
          .fontColor('#666666')
          .textAlign(TextAlign.Start)
          .padding(10)
          .backgroundColor('#F5F5F5')
          .borderRadius(8)
          .margin({ top: 10 })
      }
    }
    .width('100%')
    .height('100%')
    .padding(20)
  }
}
