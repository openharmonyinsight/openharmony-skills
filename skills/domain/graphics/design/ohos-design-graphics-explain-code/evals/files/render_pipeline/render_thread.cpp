#include "render_thread.h"
#include <algorithm>

namespace OHOS::Rosen {

RSMainThread::RSMainThread() {}

RSMainThread::~RSMainThread() {
    Stop();
}

void RSMainThread::Start() {
    running_ = true;
    thread_ = std::thread([this]() {
        while (running_) {
            std::unique_lock<std::mutex> lock(queueMutex_);
            queueCV_.wait(lock, [this]() { return !commandQueue_.empty() || !running_; });
            if (!running_) break;
            auto cmd = commandQueue_.front();
            commandQueue_.pop();
            lock.unlock();
            ProcessCommand(cmd);
        }
    });
}

void RSMainThread::Stop() {
    running_ = false;
    queueCV_.notify_all();
    if (thread_.joinable()) {
        thread_.join();
    }
}

void RSMainThread::OnVsync(uint64_t timestamp) {
    Animate(timestamp);
    Prepare();
    CalcOcclusion();
    Sync();
}

void RSMainThread::ProcessCommand(const RenderCommand& cmd) {
    switch (cmd.type) {
        case RenderCommand::PREPARE:
            for (auto& node : rootNodes_) {
                node->Prepare();
            }
            break;
        case RenderCommand::SYNC:
            Sync();
            break;
        case RenderCommand::UPDATE_BOUNDS:
            if (cmd.callback) cmd.callback();
            break;
        case RenderCommand::RENDER:
            break;
    }
}

void RSMainThread::Animate(uint64_t timestamp) {
    for (auto& node : rootNodes_) {
        // animation processing per node
    }
}

void RSMainThread::Prepare() {
    for (auto& node : rootNodes_) {
        node->Prepare();
        for (auto& child : node->GetChildren()) {
            child->Prepare();
        }
    }
}

void RSMainThread::CalcOcclusion() {
    // occlusion calculation logic
}

void RSMainThread::Sync() {
    for (auto& node : rootNodes_) {
        RenderCommand cmd;
        cmd.nodeId = node->GetNodeId();
        cmd.type = RenderCommand::RENDER;
        SubmitCommand(cmd);
    }
}

void RSMainThread::SubmitCommand(RenderCommand cmd) {
    {
        std::lock_guard<std::mutex> lock(queueMutex_);
        renderQueue_.push(cmd); // sends to uni render thread
    }
    queueCV_.notify_one();
}

RSUniRenderThread::RSUniRenderThread() {}

RSUniRenderThread::~RSUniRenderThread() {
    Stop();
}

void RSUniRenderThread::Start() {
    running_ = true;
    thread_ = std::thread([this]() {
        while (running_) {
            std::unique_lock<std::mutex> lock(queueMutex_);
            queueCV_.wait(lock, [this]() { return !renderQueue_.empty() || !running_; });
            if (!running_) break;
            auto cmd = renderQueue_.front();
            renderQueue_.pop();
            lock.unlock();
            Render();
        }
    });
}

void RSUniRenderThread::Stop() {
    running_ = false;
    queueCV_.notify_all();
    if (thread_.joinable()) {
        thread_.join();
    }
}

void RSUniRenderThread::Render() {
    auto drawable = RSRenderNodeDrawable::Create(nullptr);
    OnDraw(drawable);
}

void RSUniRenderThread::OnDraw(std::shared_ptr<RSRenderNodeDrawable> drawable) {
    if (drawable) {
        drawable->Draw();
        drawable->UpdateCacheInfo();
        if (renderCallback_) {
            renderCallback_(drawable->GetRenderNode() ? drawable->GetRenderNode()->GetNodeId() : 0);
        }
    }
}

void UniRenderCallback::OnRenderComplete(uint64_t nodeId) {
    std::lock_guard<std::mutex> lock(checkMutex_);
    if (mainThread_) {
        // notify main thread render is done
    }
}

} // namespace OHOS::Rosen