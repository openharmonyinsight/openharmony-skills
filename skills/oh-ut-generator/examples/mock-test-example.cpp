/*
 * Copyright (c) 2025 Huawei Device Co., Ltd.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include <gtest/gtest.h>
#include <gmock/gmock.h>
#include "service.h"
#include "mock_service.h"

using namespace testing;
using namespace OHOS;

class ServiceWithMockTest : public testing::Test {
public:
    static void SetUpTestCase(void) {}
    static void TearDownTestCase(void) {}
    void SetUp() override {
        mockDependency_ = std::make_shared<MockDependency>();
        instance_ = std::make_shared<Service>(mockDependency_);
    }
    void TearDown() override {
        instance_.reset();
        mockDependency_.reset();
    }

protected:
    std::shared_ptr<Service> instance_;
    std::shared_ptr<MockDependency> mockDependency_;
};

/**
 * @tc.name: ServiceWithMockTest_ProcessWithDependency_001
 * @tc.desc: Verify ProcessWithDependency calls dependency method correctly
 * @tc.type: FUNC
 * @tc.require: I123456
 */
HWTEST_F(ServiceWithMockTest, ProcessWithDependency_001, TestSize.Level1) {
    GTEST_LOG_(INFO) << "ServiceWithMockTest-begin ProcessWithDependency_001";
    ASSERT_NE(instance_, nullptr);
    ASSERT_NE(mockDependency_, nullptr);

    // Setup expectations
    EXPECT_CALL(*mockDependency_, Initialize())
        .WillOnce(Return(true));
    EXPECT_CALL(*mockDependency_, ProcessData(_))
        .WillOnce(Return(ERR_OK));

    // Prepare test data
    std::string data = "test data";

    // Call the target function
    int result = instance_->ProcessWithDependency(data);

    // Verify result
    EXPECT_EQ(result, ERR_OK);

    GTEST_LOG_(INFO) << "ServiceWithMockTest-end ProcessWithDependency_001";
}

/**
 * @tc.name: ServiceWithMockTest_ProcessWithDependency_002
 * @tc.desc: Verify ProcessWithDependency handles dependency initialization failure
 * @tc.type: FUNC
 * @tc.require: I123456
 */
HWTEST_F(ServiceWithMockTest, ProcessWithDependency_002, TestSize.Level1) {
    GTEST_LOG_(INFO) << "ServiceWithMockTest-begin ProcessWithDependency_002";
    ASSERT_NE(instance_, nullptr);
    ASSERT_NE(mockDependency_, nullptr);

    // Setup expectations - initialization fails
    EXPECT_CALL(*mockDependency_, Initialize())
        .WillOnce(Return(false));

    // Prepare test data
    std::string data = "test data";

    // Call the target function
    int result = instance_->ProcessWithDependency(data);

    // Verify result - should return error when initialization fails
    EXPECT_EQ(result, ERR_FAILED);

    GTEST_LOG_(INFO) << "ServiceWithMockTest-end ProcessWithDependency_002";
}

/**
 * @tc.name: ServiceWithMockTest_ProcessWithDependency_003
 * @tc.desc: Verify ProcessWithDependency handles data processing failure
 * @tc.type: FUNC
 * @tc.require: I123456
 */
HWTEST_F(ServiceWithMockTest, ProcessWithDependency_003, TestSize.Level1) {
    GTEST_LOG_(INFO) << "ServiceWithMockTest-begin ProcessWithDependency_003";
    ASSERT_NE(instance_, nullptr);
    ASSERT_NE(mockDependency_, nullptr);

    // Setup expectations - processing fails
    EXPECT_CALL(*mockDependency_, Initialize())
        .WillOnce(Return(true));
    EXPECT_CALL(*mockDependency_, ProcessData(_))
        .WillOnce(Return(ERR_INVALID_PARAMETER));

    // Prepare test data
    std::string data = "invalid data";

    // Call the target function
    int result = instance_->ProcessWithDependency(data);

    // Verify result - should return error when processing fails
    EXPECT_EQ(result, ERR_INVALID_PARAMETER);

    GTEST_LOG_(INFO) << "ServiceWithMockTest-end ProcessWithDependency_003";
}

/**
 * @tc.name: ServiceWithMockTest_NotifyCallback_001
 * @tc.desc: Verify NotifyCallback triggers dependency callback correctly
 * @tc.type: FUNC
 * @tc.require: I123456
 */
HWTEST_F(ServiceWithMockTest, NotifyCallback_001, TestSize.Level1) {
    GTEST_LOG_(INFO) << "ServiceWithMockTest-begin NotifyCallback_001";
    ASSERT_NE(instance_, nullptr);
    ASSERT_NE(mockDependency_, nullptr);

    // Setup expectations with parameter verification
    EXPECT_CALL(*mockDependency_, OnEvent(Eq(EVENT_TYPE_COMPLETE)))
        .WillOnce(Return(true));

    // Call the target function
    bool result = instance_->NotifyCallback(EVENT_TYPE_COMPLETE);

    // Verify result
    EXPECT_TRUE(result);

    GTEST_LOG_(INFO) << "ServiceWithMockTest-end NotifyCallback_001";
}

/**
 * @tc.name: ServiceWithMockTest_MultipleCalls_001
 * @tc.desc: Verify multiple calls to dependency method
 * @tc.type: FUNC
 * @tc.require: I123456
 */
HWTEST_F(ServiceWithMockTest, MultipleCalls_001, TestSize.Level1) {
    GTEST_LOG_(INFO) << "ServiceWithMockTest-begin MultipleCalls_001";
    ASSERT_NE(instance_, nullptr);
    ASSERT_NE(mockDependency_, nullptr);

    // Setup expectations for multiple calls
    EXPECT_CALL(*mockDependency_, ProcessData(_))
        .Times(3)
        .WillRepeatedly(Return(ERR_OK));

    // Call the target function multiple times
    for (int i = 0; i < 3; i++) {
        std::string data = "test data " + std::to_string(i);
        int result = instance_->ProcessWithDependency(data);
        EXPECT_EQ(result, ERR_OK);
    }

    GTEST_LOG_(INFO) << "ServiceWithMockTest-end MultipleCalls_001";
}
