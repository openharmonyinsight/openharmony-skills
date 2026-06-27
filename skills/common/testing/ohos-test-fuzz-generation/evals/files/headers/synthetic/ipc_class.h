#ifndef IPC_CLASS_H
#define IPC_CLASS_H

#include <cstdint>
#include "iremote_broker.h"
#include "iremote_proxy.h"
#include "iremote_stub.h"
#include "message_parcel.h"

namespace OHOS {
namespace Display {

class IDisplayService : public IRemoteBroker {
public:
    DECLARE_INTERFACE_DESCRIPTOR(u"OHOS.Display.IDisplayService");

    enum Code {
        SET_BRIGHTNESS = 0,
        GET_BRIGHTNESS = 1,
        SET_POWER_STATUS = 2,
        REGISTER_CALLBACK = 3,
    };

    virtual int32_t SetBrightness(int32_t brightness) = 0;
    virtual int32_t GetBrightness() = 0;
    virtual int32_t SetPowerStatus(int32_t status) = 0;
    virtual int32_t RegisterCallback(const sptr<IRemoteObject> &callback) = 0;
};

class DisplayServiceProxy : public IRemoteProxy<IDisplayService> {
public:
    explicit DisplayServiceProxy(const sptr<IRemoteObject> &impl);
    ~DisplayServiceProxy() = default;

    int32_t SetBrightness(int32_t brightness) override;
    int32_t GetBrightness() override;
    int32_t SetPowerStatus(int32_t status) override;
    int32_t RegisterCallback(const sptr<IRemoteObject> &callback) override;

private:
    static inline BrokerDelegator<DisplayServiceProxy> delegator_;
};

class DisplayServiceStub : public IRemoteStub<IDisplayService> {
public:
    int32_t OnRemoteRequest(uint32_t code, MessageParcel &data, MessageParcel &reply,
                            MessageOption &option) override;
    int32_t SetBrightness(int32_t brightness) override;
    int32_t GetBrightness() override;
    int32_t SetPowerStatus(int32_t status) override;
    int32_t RegisterCallback(const sptr<IRemoteObject> &callback) override;
};

} // namespace Display
} // namespace OHOS

#endif // IPC_CLASS_H
