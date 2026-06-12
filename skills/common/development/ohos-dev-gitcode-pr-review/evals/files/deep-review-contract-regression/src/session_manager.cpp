#include "session_manager.h"

bool SessionManager::IsSessionExpired(int64_t expireAtMs) const
{
    if (expireAtMs <= 0) {
        return false;
    }
    return clock_->NowMs() >= expireAtMs;
}
