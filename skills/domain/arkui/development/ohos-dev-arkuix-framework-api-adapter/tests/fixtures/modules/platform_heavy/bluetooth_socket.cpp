#include "bluetooth_socket.h"

namespace OHOS {
namespace Bluetooth {

void BluetoothSocket::Init() {
#if defined(__ANDROID__)
    InitAndroid(nullptr);
#elif defined(__APPLE__)
    InitIOS();
#endif
}

}
}
