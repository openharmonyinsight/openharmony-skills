#import <CoreBluetooth/CoreBluetooth.h>
#import <Foundation/Foundation.h>
#include "bluetooth_socket.h"

namespace OHOS {
namespace Bluetooth {

static CBCentralManager* g_centralManager = nil;
static CBPeripheralManager* g_peripheralManager = nil;

void BluetoothSocket::InitIOS() {
    dispatch_async(dispatch_get_main_queue(), ^{
        g_centralManager = [[CBCentralManager alloc] initWithDelegate:nil queue:nil];
        g_peripheralManager = [[CBPeripheralManager alloc] initWithDelegate:nil queue:nil];
    });
}

int BluetoothSocket::SppListen(const std::string& name, const SppOption& option) {
    if (!g_peripheralManager) {
        return -1;
    }

    CBUUID* serviceUuid = [CBUUID UUIDWithString:[NSString stringWithUTF8String:option.uuid.c_str()]];
    CBMutableService* service = [[CBMutableService alloc] initWithType:serviceUuid primary:YES];

    CBPeripheralManagerOptions options = @{
        CBPeripheralManagerOptionShowPowerAlertKey: @YES
    };

    [g_peripheralManager startAdvertising:@{
        CBAdvertisementDataServiceUUIDsKey: @[serviceUuid],
        CBAdvertisementDataLocalNameKey: [NSString stringWithUTF8String:name.c_str()]
    }];

    return 0;
}

int BluetoothSocket::SppAccept(int serverSocketCode) {
    NSLog(@"SppAccept not directly supported on iOS - requires delegate pattern");
    return -1;
}

void BluetoothSocket::SppConnect(const std::string& deviceId, const SppOption& option) {
    if (!g_centralManager) {
        return;
    }

    NSUUID* uuid = [[NSUUID alloc] initWithUUIDString:[NSString stringWithUTF8String:deviceId.c_str()]];
    NSArray* peripherals = [g_centralManager retrievePeripheralsWithIdentifiers:@[uuid]];

    if (peripherals.count > 0) {
        CBPeripheral* peripheral = peripherals[0];
        [g_centralManager connectPeripheral:peripheral options:nil];
    }
}

}
}
