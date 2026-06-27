#ifndef NO_PARAM_CLASS_H
#define NO_PARAM_CLASS_H

#include <cstdint>

namespace OHOS {
namespace Memory {

class MemoryMonitor {
public:
    MemoryMonitor() = default;
    ~MemoryMonitor() = default;

    void Start();
    void Stop();
    void Reset();
    int32_t GetTotalMemory() const;
    int32_t GetAvailableMemory() const;
    void DumpStatus() const;
};

} // namespace Memory
} // namespace OHOS

#endif // NO_PARAM_CLASS_H
