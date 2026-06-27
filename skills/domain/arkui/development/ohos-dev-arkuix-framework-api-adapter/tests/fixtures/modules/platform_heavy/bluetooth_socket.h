#pragma once
#include <string>

namespace OHOS {
namespace Bluetooth {

enum class SppType {
    SPP_RFCOMM = 0,
    SPP_LE = 1
};

struct SppOption {
    SppType type;
    std::string uuid;
    bool secure;
};

class BluetoothSocket {
public:
    static void Init();
    static int SppListen(const std::string& name, const SppOption& option);
    static int SppAccept(int serverSocketCode);
    static void SppConnect(const std::string& deviceId, const SppOption& option);

#if defined(__ANDROID__)
    static void InitAndroid(JNIEnv* env);
    static jobject CreateSppOptionJNI(JNIEnv* env, const SppOption& option);
#elif defined(__APPLE__)
    static void InitIOS();
#endif
};

}
}
