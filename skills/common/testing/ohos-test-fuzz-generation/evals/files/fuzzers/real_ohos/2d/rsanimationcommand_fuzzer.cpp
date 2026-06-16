/*
 * Copyright (c) 2024 Huawei Device Co., Ltd.
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

#include "rsanimationcommand_fuzzer.h"

#include <securec.h>

#include "command/rs_animation_command.h"

namespace OHOS {
    using namespace Rosen;

    class RSRenderAnimationFuzzMock : public RSRenderAnimation {
    public:
        RSRenderAnimationFuzzMock() : RSRenderAnimation() {}
        explicit RSRenderAnimationFuzzMock(AnimationId id) : RSRenderAnimation(id) {}
        ~RSRenderAnimationFuzzMock() override = default;
        void RebuildPropertyValue(float fraction) override {}
    };

    namespace {
        const uint8_t* data_ = nullptr;
        size_t size_ = 0;
        size_t pos;
    }

    /*
    * describe: get data from outside untrusted data(data_) which size is according to sizeof(T)
    * tips: only support basic type
    */
    template<class T>
    T GetData()
    {
        T object {};
        size_t objectSize = sizeof(object);
        if (data_ == nullptr || objectSize > size_ - pos) {
            return object;
        }
        errno_t ret = memcpy_s(&object, objectSize, data_ + pos, objectSize);
        if (ret != EOK) {
            return {};
        }
        pos += objectSize;
        return object;
    }

    /*
    * get a string from data_
    */
    std::string GetStringFromData(int strlen)
    {
        char cstr[strlen];
        cstr[strlen - 1] = '\0';
        for (int i = 0; i < strlen - 1; i++) {
            cstr[i] = GetData<char>();
        }
        std::string str(cstr);
        return str;
    }

    void CreateAnimationFuzzerTest()
    {
        // get data
        RSContext context;
        NodeId targetId = GetData<NodeId>();
        AnimationId animId = GetData<AnimationId>();
        AnimationCallbackEvent event = GetData<AnimationCallbackEvent>();
        uint64_t token = GetData<uint64_t>();
        PropertyId propertyId = GetData<PropertyId>();

        // AnimationCallBack
        auto callback = [](NodeId nodeId, AnimationId animId, uint64_t token, AnimationCallbackEvent event) {};
        AnimationCommandHelper::SetAnimationCallbackProcessor(callback);
        AnimationCommandHelper::AnimationCallback(context, targetId, animId, token, event);

        // test
        std::shared_ptr<RSRenderAnimation> animation = nullptr;
        AnimationCommandHelper::CreateAnimation(context, targetId, animation);

        animation = std::make_shared<RSRenderAnimationFuzzMock>();
        AnimationCommandHelper::CreateAnimation(context, targetId, animation);
        AnimationCommandHelper::CancelAnimation(context, targetId, propertyId);

        std::shared_ptr<RSBaseRenderNode> node = std::make_shared<RSBaseRenderNode>(targetId);
        context.GetMutableNodeMap().RegisterRenderNode(node);
        AnimationCommandHelper::CreateAnimation(context, targetId, animation);
        AnimationCommandHelper::CancelAnimation(context, targetId, propertyId);
    }

    void CreateParticleAnimationFuzzerTest()
    {
        // get data
        RSContext context;
        NodeId targetId = GetData<NodeId>();

        // test
        AnimationCommandHelper::CreateParticleAnimationNG(context, targetId, 0, nullptr);
        std::shared_ptr<RSRenderParticleAnimation> particleAnimation = std::make_shared<RSRenderParticleAnimation>();
        AnimationCommandHelper::CreateParticleAnimationNG(context, targetId, 0, particleAnimation);
        std::shared_ptr<RSBaseRenderNode> node = std::make_shared<RSBaseRenderNode>(targetId);
        context.GetMutableNodeMap().RegisterRenderNode(node);
        AnimationCommandHelper::CreateParticleAnimationNG(context, targetId, 0, particleAnimation);
    }

    void InteractiveAnimatiorFuzzerTest()
    {
        // get data
        RSContext context;
        NodeId targetId = GetData<NodeId>();
        AnimationId animationId = GetData<NodeId>();
        InteractiveImplictAnimatorId animatorId = GetData<InteractiveImplictAnimatorId>();
        float fraction = GetData<float>();
        bool isImmediately = GetData<bool>();
        RSInteractiveAnimationPosition position = GetData<RSInteractiveAnimationPosition>();
        std::vector<std::pair<NodeId, AnimationId>> animations;
        animations.emplace_back(targetId, animationId);

        AnimationCommandHelper::DestoryInteractiveAnimator(context, animatorId);
        AnimationCommandHelper::InteractiveAnimatorAddAnimations(context, animatorId, animations);
        AnimationCommandHelper::PauseInteractiveAnimator(context, animatorId);
        AnimationCommandHelper::ContinueInteractiveAnimator(context, animatorId);
        AnimationCommandHelper::FinishInteractiveAnimator(context, animatorId, position);
        AnimationCommandHelper::ReverseInteractiveAnimator(context, animatorId);
        AnimationCommandHelper::SetFractionInteractiveAnimator(context, animatorId, fraction);

        AnimationCommandHelper::CreateInteractiveAnimator(context, targetId, animations, isImmediately);
        AnimationCommandHelper::InteractiveAnimatorAddAnimations(context, animatorId, animations);
        AnimationCommandHelper::PauseInteractiveAnimator(context, animatorId);
        AnimationCommandHelper::ContinueInteractiveAnimator(context, animatorId);
        AnimationCommandHelper::FinishInteractiveAnimator(context, animatorId, position);
        AnimationCommandHelper::ReverseInteractiveAnimator(context, animatorId);
        AnimationCommandHelper::SetFractionInteractiveAnimator(context, animatorId, fraction);
        AnimationCommandHelper::DestoryInteractiveAnimator(context, animatorId);

        // test CreateInteractiveAnimatorGroup
        RSAnimationTimingProtocol timingProtocol;
        int duration = GetData<int>();
        int startDelay = GetData<int>();
        int repeatCount = GetData<int>();
        float speed = GetData<float>();
        bool autoReverse = GetData<bool>();
        timingProtocol.SetDuration(duration);
        timingProtocol.SetStartDelay(startDelay);
        timingProtocol.SetRepeatCount(repeatCount);
        timingProtocol.SetSpeed(speed);
        timingProtocol.SetAutoReverse(autoReverse);

        AnimationCommandHelper::CreateInteractiveAnimatorGroup(
            context, animatorId, animations, isImmediately, timingProtocol);
    }

    bool DoSomethingInterestingWithMyAPI(const uint8_t* data, size_t size)
    {
        if (data == nullptr) {
            return false;
        }
        // initialize
        data_ = data;
        size_ = size;
        pos = 0;
        InteractiveAnimatiorFuzzerTest();
        return true;
    }
}

/* Fuzzer entry point */
extern "C" int LLVMFuzzerTestOneInput(const uint8_t* data, size_t size)
{
    /* Run your code on data */
    OHOS::DoSomethingInterestingWithMyAPI(data, size);
    return 0;
}
