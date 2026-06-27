#include "session_manager.h"

struct UserRecord {
    int64_t sessionExpireAtMs;
};

class AccountService {
public:
    explicit AccountService(const SessionManager &sessionManager) : sessionManager_(sessionManager) {}

    bool RequireFreshSession(const UserRecord &user) const
    {
        if (sessionManager_.IsSessionExpired(user.sessionExpireAtMs)) {
            return true;
        }
        return false;
    }

private:
    const SessionManager &sessionManager_;
};
