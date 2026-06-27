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

#include "event_manager.h"

namespace OHOS {
namespace HiviewDFX {

bool EventManager::Start()
{
    if (currentState_ == STATE_RUNNING) {
        return false;
    }
    currentState_ = STATE_RUNNING;
    return true;
}

bool EventManager::Stop()
{
    if (currentState_ == STATE_IDLE) {
        return false;
    }
    currentState_ = STATE_STOPPED;
    return true;
}

bool EventManager::Pause()
{
    if (currentState_ != STATE_RUNNING) {
        return false;
    }
    currentState_ = STATE_PAUSED;
    return true;
}

bool EventManager::Resume()
{
    if (currentState_ != STATE_PAUSED) {
        return false;
    }
    currentState_ = STATE_RUNNING;
    return true;
}

bool EventManager::AddEventListener(const std::shared_ptr<IEventListener>& listener)
{
    if (listener == nullptr) {
        return false;
    }
    listeners_.push_back(listener);
    return true;
}

bool EventManager::RemoveEventListener(const std::shared_ptr<IEventListener>& listener)
{
    if (listener == nullptr) {
        return false;
    }
    for (auto it = listeners_.begin(); it != listeners_.end(); ++it) {
        if (*it == listener) {
            listeners_.erase(it);
            return true;
        }
    }
    return false;
}

int EventManager::GetListenerCount()
{
    return listeners_.size();
}

EventState EventManager::GetState()
{
    return currentState_;
}

bool EventManager::ProcessEvent(const EventInfo& event)
{
    if (currentState_ != STATE_RUNNING) {
        return false;
    }
    if (event.domain.empty() || event.eventName.empty()) {
        return false;
    }
    for (auto& listener : listeners_) {
        listener->OnEventReceived(event);
    }
    history_.push_back(event);
    if (history_.size() > maxHistorySize_) {
        history_.erase(history_.begin());
    }
    return true;
}

std::vector<EventInfo> EventManager::GetHistoryEvents(int count)
{
    if (count <= 0) {
        return {};
    }
    if (count > static_cast<int>(history_.size())) {
        return history_;
    }
    return std::vector<EventInfo>(history_.end() - count, history_.end());
}

} // namespace HiviewDFX
} // namespace OHOS
