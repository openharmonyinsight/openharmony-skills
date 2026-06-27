#include <gtest/gtest.h>

TEST(MetricsLoggerTest, CacheHitRecordsCounter)
{
    MetricsLogger logger;
    logger.LogCacheHit("bundle");
    EXPECT_EQ(GetCounterValue("cache.hit"), 1);
}
