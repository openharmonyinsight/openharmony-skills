#ifndef DEMO_SERVICE_SESSION_MANAGER_H
#define DEMO_SERVICE_SESSION_MANAGER_H

#include <cstdint>

class Clock {
public:
    virtual ~Clock() = default;
    virtual int64_t NowMs() const = 0;
};

class SessionManager {
public:
    explicit SessionManager(const Clock *clock) : clock_(clock) {}
    bool IsSessionExpired(int64_t expireAtMs) const;

private:
    const Clock *clock_;
};

#endif
