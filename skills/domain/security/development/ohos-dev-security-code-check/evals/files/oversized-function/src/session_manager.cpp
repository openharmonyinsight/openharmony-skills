// Fixture: oversized function for eval case 1.
// Contains one function well over the default 50 effective-line threshold.
// Blank lines, comments, and preprocessor directives do NOT count.

#include <string>
#include <vector>
#include <map>

namespace session {

struct SessionInfo {
    int userId;
    std::string token;
    int64_t expireAtMs;
    std::string bundleName;
};

class SessionManager {
public:
    // This function is intentionally oversized to exceed the 50-line default threshold.
    // A with-skill run must flag it; a well-structured baseline would split it.
    int RefreshAllSessions(std::vector<SessionInfo> &sessions, const std::map<int, std::string> &policy) {
        int refreshed = 0;
        for (auto &s : sessions) {
            if (s.expireAtMs <= 0) {
                continue;
            }
            auto it = policy.find(s.userId);
            if (it == policy.end()) {
                continue;
            }
            const std::string &rule = it->second;
            if (rule == "force-refresh") {
                s.token = GenerateToken(s.userId, s.bundleName);
                s.expireAtMs = Now() + DEFAULT_TTL_MS;
                refreshed++;
                LogRefresh(s.userId, "force");
            } else if (rule == "lazy-refresh") {
                if (s.expireAtMs - Now() < SOFT_THRESHOLD_MS) {
                    s.token = GenerateToken(s.userId, s.bundleName);
                    s.expireAtMs = Now() + DEFAULT_TTL_MS;
                    refreshed++;
                    LogRefresh(s.userId, "lazy");
                }
            } else if (rule == "evict") {
                s.token.clear();
                s.expireAtMs = 0;
                LogRefresh(s.userId, "evict");
            } else if (rule == "keep") {
                // no-op, keep current token
            } else if (rule == "rotate") {
                std::string newToken = GenerateToken(s.userId, s.bundleName);
                if (!newToken.empty() && newToken != s.token) {
                    s.token = newToken;
                    s.expireAtMs = Now() + DEFAULT_TTL_MS;
                    refreshed++;
                    LogRefresh(s.userId, "rotate");
                }
            } else if (rule == "audit") {
                AuditSession(s.userId, s.bundleName, s.token);
            } else if (rule == "throttle") {
                int64_t remaining = s.expireAtMs - Now();
                if (remaining > 0 && remaining < DEFAULT_TTL_MS / 2) {
                    s.expireAtMs = Now() + DEFAULT_TTL_MS;
                    LogRefresh(s.userId, "throttle-extended");
                    refreshed++;
                } else if (remaining <= 0) {
                    s.token = GenerateToken(s.userId, s.bundleName);
                    s.expireAtMs = Now() + DEFAULT_TTL_MS;
                    LogRefresh(s.userId, "throttle-expired");
                    refreshed++;
                }
            } else if (rule == "quarantine") {
                s.token.clear();
                s.expireAtMs = 0;
                s.bundleName = "quarantined:" + s.bundleName;
                LogRefresh(s.userId, "quarantine");
            } else {
                // unknown policy: skip but record
                LogRefresh(s.userId, "unknown:" + rule);
            }
            // additional housekeeping
            if (s.bundleName.empty()) {
                s.bundleName = "unknown";
            }
            if (s.userId < 0) {
                s.userId = 0;
            }
        }
        return refreshed;
    }

private:
    static constexpr int64_t DEFAULT_TTL_MS = 3600000;
    static constexpr int64_t SOFT_THRESHOLD_MS = 600000;
    std::string GenerateToken(int, const std::string &) { return "tok"; }
    int64_t Now() { return 0; }
    void LogRefresh(int, const std::string &) {}
    void AuditSession(int, const std::string &, const std::string &) {}
};

} // namespace session
