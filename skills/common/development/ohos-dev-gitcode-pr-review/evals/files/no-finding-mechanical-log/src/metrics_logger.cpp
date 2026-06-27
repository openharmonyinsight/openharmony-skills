#include <string>

class MetricsLogger {
public:
    void LogCacheHit(const std::string &key) const
    {
        HILOG_DEBUG(LOG_CORE, "cache-hit key=%{public}s", key.c_str());
        RecordCounter("cache.hit");
    }

private:
    void RecordCounter(const std::string &name) const;
};
