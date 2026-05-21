#ifndef RENDER_THREAD_H
#define RENDER_THREAD_H

#include <thread>
#include <mutex>
#include <condition_variable>
#include <queue>
#include <functional>
#include <memory>
#include <atomic>
#include "render_node.h"

namespace OHOS::Rosen {

struct RenderCommand {
    uint64_t nodeId;
    enum CommandType {
        PREPARE,
        RENDER,
        UPDATE_BOUNDS,
        SYNC,
    } type;
    std::function<void()> callback;
};

class RSMainThread {
public:
    RSMainThread();
    ~RSMainThread();

    void Start();
    void Stop();

    void OnVsync(uint64_t timestamp);
    void ProcessCommand(const RenderCommand& cmd);
    void Animate(uint64_t timestamp);
    void Prepare();
    void CalcOcclusion();
    void Sync();

    void SubmitCommand(RenderCommand cmd);

private:
    std::thread thread_;
    std::atomic<bool> running_{false};
    std::queue<RenderCommand> commandQueue_;
    std::mutex queueMutex_;
    std::condition_variable queueCV_;
    std::vector<std::shared_ptr<RSBaseRenderNode>> rootNodes_;
};

class RSUniRenderThread {
public:
    RSUniRenderThread();
    ~RSUniRenderThread();

    void Start();
    void Stop();

    void Render();
    void OnDraw(std::shared_ptr<RSRenderNodeDrawable> drawable);

    void RegisterCallback(std::function<void(uint64_t)> cb) {
        renderCallback_ = cb;
    }

private:
    std::thread thread_;
    std::atomic<bool> running_{false};
    std::queue<RenderCommand> renderQueue_;
    std::mutex queueMutex_;
    std::condition_variable queueCV_;
    std::function<void(uint64_t)> renderCallback_;
};

class UniRenderCallback {
public:
    void OnRenderComplete(uint64_t nodeId);

    void SetMainThread(RSMainThread* mainThread) {
        mainThread_ = mainThread;
    }

private:
    RSMainThread* mainThread_ = nullptr;
    std::mutex checkMutex_;
};

} // namespace OHOS::Rosen

#endif // RENDER_THREAD_H