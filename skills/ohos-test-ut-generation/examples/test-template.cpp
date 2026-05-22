/*
 * Copyright (c) 2026 Huawei Device Co., Ltd.
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
#include "被测头文件.h"

using namespace testing::ext;  // MUST包含，HWTEST宏在此命名空间

namespace OHOS {
namespace XxxModule {

class BBoxDetectorTest : public testing::Test {
public:
    static void SetUpTestCase();     // 所有测试前执行一次
    static void TearDownTestCase();  // 所有测试后执行一次
    void SetUp() override;           // 每个测试前执行
    void TearDown() override;        // 每个测试后执行
    
    BBoxDetector* detector_;         // MUST初始化，否则SEGFAULT
};

void BBoxDetectorTest::SetUpTestCase() {}
void BBoxDetectorTest::TearDownTestCase() {}
void BBoxDetectorTest::SetUp() { detector_ = new BBoxDetector(); }
void BBoxDetectorTest::TearDown() { delete detector_; }

/**
 * @tc.name: GetSectionInfo_001
 * @tc.desc: 验证使用有效段名获取Section信息成功
 * @tc.type: FUNC
 * @tc.require: issueNumber
 */
HWTEST_F(BBoxDetectorTest, GetSectionInfo_001, TestSize.Level1)
{
    GTEST_LOG_(INFO) << "GetSectionInfo_001 start";
    
    std::string sectionName = "section1";
    SectionInfo info;
    
    bool result = detector_->GetSectionInfo(sectionName, info);
    EXPECT_TRUE(result);
    
    GTEST_LOG_(INFO) << "GetSectionInfo_001 end";
}

/**
 * @tc.name: GetSectionInfo_002
 * @tc.desc: 验证空字符串输入返回失败
 * @tc.type: FUNC
 * @tc.require: issueNumber
 */
HWTEST_F(BBoxDetectorTest, GetSectionInfo_002, TestSize.Level2)
{
    GTEST_LOG_(INFO) << "GetSectionInfo_002 start";
    
    std::string sectionName = "";
    SectionInfo info;
    
    bool result = detector_->GetSectionInfo(sectionName, info);
    EXPECT_FALSE(result);
    
    GTEST_LOG_(INFO) << "GetSectionInfo_002 end";
}

} // namespace XxxModule
} // namespace OHOS