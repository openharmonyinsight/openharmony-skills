#include "session_manager.h"

#include <gtest/gtest.h>

namespace {
class FixedClock final : public Clock {
public:
    int64_t NowMs() const override
    {
        return 1000;
    }
};
}

TEST(SessionManagerTest, ExpiredWhenTimestampMissing)
{
    FixedClock clock;
    SessionManager manager(&clock);
    EXPECT_TRUE(manager.IsSessionExpired(0));
}

TEST(SessionManagerTest, ExpiredWhenTimestampInPast)
{
    FixedClock clock;
    SessionManager manager(&clock);
    EXPECT_TRUE(manager.IsSessionExpired(500));
}
