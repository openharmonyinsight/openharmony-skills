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

#ifndef EVENT_MANAGER_H
#define EVENT_MANAGER_H

#include <string>
#include <vector>
#include <memory>

namespace OHOS {
namespace HiviewDFX {

enum EventState {
    STATE_IDLE = 0,
    STATE_RUNNING = 1,
    STATE_PAUSED = 2,
    STATE_STOPPED = 3,
};

enum EventType {
    TYPE_FAULT = 0,
    TYPE_STATISTIC = 1,
    TYPE_SECURITY = 2,
    TYPE_BEHAVIOR = 3,
};

struct EventInfo {
    std::string domain;
    std::string eventName;
    EventType type;
    EventState state;
};

class IEventListener {
public:
    virtual ~IEventListener() = default;
    virtual void OnEventReceived(const EventInfo& event) = 0;
};

class EventManager {
public:
    EventManager() = default;
    ~EventManager() = default;

    bool Start();
    bool Stop();
    bool Pause();
    bool Resume();
    bool AddEventListener(const std::shared_ptr<IEventListener>& listener);
    bool RemoveEventListener(const std::shared_ptr<IEventListener>& listener);
    int GetListenerCount();
    EventState GetState();
    bool ProcessEvent(const EventInfo& event);
    std::vector<EventInfo> GetHistoryEvents(int count);

private:
    EventState currentState_ = STATE_IDLE;
    std::vector<std::shared_ptr<IEventListener>> listeners_;
    std::vector<EventInfo> history_;
    int maxHistorySize_ = 100;
};

} // namespace HiviewDFX
} // namespace OHOS

#endif // EVENT_MANAGER_H
