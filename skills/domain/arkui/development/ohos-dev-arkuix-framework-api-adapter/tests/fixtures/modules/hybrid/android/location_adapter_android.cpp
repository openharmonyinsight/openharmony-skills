#include "location_adapter.h"
#include <jni.h>
#include <android/log.h>

#define LOG_TAG "LocationAdapter"
#define LOGI(...) __android_log_print(ANDROID_LOG_INFO, LOG_TAG, __VA_ARGS__)

namespace OHOS {
namespace Location {

static JavaVM* g_jvm = nullptr;
static jclass g_locationClass = nullptr;

class AndroidLocationAdapter : public LocationAdapter {
public:
    bool StartLocating(const LocationRequest& request) override {
        JNIEnv* env = GetEnv();
        jmethodID method = env->GetStaticMethodID(g_locationClass,
            "startLocating", "(IJ)V");
        env->CallStaticVoidMethod(g_locationClass, method,
            static_cast<jint>(request.priority),
            static_cast<jlong>(request.intervalMs));
        return true;
    }

    bool StopLocating() override {
        JNIEnv* env = GetEnv();
        jmethodID method = env->GetStaticMethodID(g_locationClass, "stopLocating", "()V");
        env->CallStaticVoidMethod(g_locationClass, method);
        return true;
    }

    LocationInfo GetCachedLocation() override {
        JNIEnv* env = GetEnv();
        jmethodID method = env->GetStaticMethodID(g_locationClass,
            "getCachedLocation", "()Lohos/location/LocationInfo;");
        jobject jLocation = env->CallStaticObjectMethod(g_locationClass, method);

        LocationInfo info = {};
        if (jLocation) {
            jclass clazz = env->GetObjectClass(jLocation);
            info.latitude = env->GetDoubleField(jLocation,
                env->GetFieldID(clazz, "latitude", "D"));
            info.longitude = env->GetDoubleField(jLocation,
                env->GetFieldID(clazz, "longitude", "D"));
            info.accuracy = env->GetFloatField(jLocation,
                env->GetFieldID(clazz, "accuracy", "F"));
            env->DeleteLocalRef(jLocation);
        }
        return info;
    }

    void SetLocationCallback(std::function<void(const LocationInfo&)> callback) override {
        callback_ = callback;
    }

private:
    JNIEnv* GetEnv() {
        JNIEnv* env = nullptr;
        if (g_jvm->GetEnv((void**)&env, JNI_VERSION_1_6) != JNI_OK) {
            g_jvm->AttachCurrentThread(&env, nullptr);
        }
        return env;
    }

    std::function<void(const LocationInfo&)> callback_;
};

}
}
