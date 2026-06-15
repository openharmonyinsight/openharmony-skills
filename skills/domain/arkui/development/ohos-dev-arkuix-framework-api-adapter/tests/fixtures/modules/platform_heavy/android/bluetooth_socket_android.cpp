#include "bluetooth_socket.h"
#include <jni.h>
#include <android/log.h>

#define LOG_TAG "BluetoothSocket"
#define LOGI(...) __android_log_print(ANDROID_LOG_INFO, LOG_TAG, __VA_ARGS__)
#define LOGE(...) __android_log_print(ANDROID_LOG_ERROR, LOG_TAG, __VA_ARGS__)

namespace OHOS {
namespace Bluetooth {

static JavaVM* g_jvm = nullptr;
static jclass g_socketClass = nullptr;
static jmethodID g_listenMethod = nullptr;

void BluetoothSocket::InitAndroid(JNIEnv* env) {
    env->GetJavaVM(&g_jvm);
    jclass clazz = env->FindClass("ohos/bluetooth/BluetoothSocket");
    g_socketClass = (jclass)env->NewGlobalRef(clazz);
    g_listenMethod = env->GetMethodID(g_socketClass, "sppListen", "(Ljava/lang/String;Lohos/bluetooth/SppOption;)I");
}

int BluetoothSocket::SppListen(const std::string& name, const SppOption& option) {
    JNIEnv* env = nullptr;
    bool attached = false;
    if (g_jvm->GetEnv((void**)&env, JNI_VERSION_1_6) != JNI_OK) {
        g_jvm->AttachCurrentThread(&env, nullptr);
        attached = true;
    }

    jstring jName = env->NewStringUTF(name.c_str());
    jobject jOption = CreateSppOptionJNI(env, option);
    jint result = env->CallIntMethod(g_socketClass, g_listenMethod, jName, jOption);

    env->DeleteLocalRef(jName);
    env->DeleteLocalRef(jOption);

    if (attached) {
        g_jvm->DetachCurrentThread();
    }
    return result;
}

int BluetoothSocket::SppAccept(int serverSocketCode) {
    JNIEnv* env = nullptr;
    bool attached = false;
    if (g_jvm->GetEnv((void**)&env, JNI_VERSION_1_6) != JNI_OK) {
        g_jvm->AttachCurrentThread(&env, nullptr);
        attached = true;
    }

    jmethodID acceptMethod = env->GetMethodID(g_socketClass, "sppAccept", "(I)I");
    jint result = env->CallIntMethod(g_socketClass, acceptMethod, serverSocketCode);

    if (attached) {
        g_jvm->DetachCurrentThread();
    }
    return result;
}

void BluetoothSocket::SppConnect(const std::string& deviceId, const SppOption& option) {
    JNIEnv* env = nullptr;
    bool attached = false;
    if (g_jvm->GetEnv((void**)&env, JNI_VERSION_1_6) != JNI_OK) {
        g_jvm->AttachCurrentThread(&env, nullptr);
        attached = true;
    }

    jstring jDeviceId = env->NewStringUTF(deviceId.c_str());
    jobject jOption = CreateSppOptionJNI(env, option);
    jmethodID connectMethod = env->GetMethodID(g_socketClass, "sppConnect", "(Ljava/lang/String;Lohos/bluetooth/SppOption;)V");
    env->CallVoidMethod(g_socketClass, connectMethod, jDeviceId, jOption);

    env->DeleteLocalRef(jDeviceId);
    env->DeleteLocalRef(jOption);

    if (attached) {
        g_jvm->DetachCurrentThread();
    }
}

jobject BluetoothSocket::CreateSppOptionJNI(JNIEnv* env, const SppOption& option) {
    jclass optionClass = env->FindClass("ohos/bluetooth/SppOption");
    jmethodID constructor = env->GetMethodID(optionClass, "<init>", "()V");
    jobject jOption = env->NewObject(optionClass, constructor);

    jfieldID typeField = env->GetFieldID(optionClass, "type", "I");
    jfieldID uuidField = env->GetFieldID(optionClass, "uuid", "Ljava/lang/String;");
    jfieldID secureField = env->GetFieldID(optionClass, "secure", "Z");

    env->SetIntField(jOption, typeField, static_cast<int>(option.type));
    env->SetObjectField(jOption, uuidField, env->NewStringUTF(option.uuid.c_str()));
    env->SetBooleanField(jOption, secureField, option.secure);

    env->DeleteLocalRef(optionClass);
    return jOption;
}

}
}
