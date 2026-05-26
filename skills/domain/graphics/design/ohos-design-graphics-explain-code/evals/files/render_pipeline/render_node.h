#ifndef RENDER_NODE_H
#define RENDER_NODE_H

#include <memory>
#include <mutex>
#include <atomic>
#include <functional>
#include <vector>
#include <string>

namespace OHOS::Rosen {

class RSRenderNode {
public:
    RSRenderNode(uint64_t nodeId) : nodeId_(nodeId) {}
    virtual ~RSRenderNode() = default;

    uint64_t GetNodeId() const { return nodeId_; }
    virtual void Prepare() = 0;
    virtual void Render() = 0;

    void SetVisible(bool visible) { isVisible_ = visible; }
    bool IsVisible() const { return isVisible_; }

    void AddChild(std::shared_ptr<RSRenderNode> child) {
        children_.push_back(child);
    }

    const std::vector<std::shared_ptr<RSRenderNode>>& GetChildren() const {
        return children_;
    }

protected:
    uint64_t nodeId_;
    bool isVisible_ = true;
    std::vector<std::shared_ptr<RSRenderNode>> children_;
};

class RSBaseRenderNode : public RSRenderNode {
public:
    RSBaseRenderNode(uint64_t nodeId) : RSRenderNode(nodeId) {}
    void Prepare() override;
    void Render() override;

    void SetBounds(float x, float y, float w, float h) {
        boundsX_ = x; boundsY_ = y; boundsW_ = w; boundsH_ = h;
    }
    float GetBoundsWidth() const { return boundsW_; }
    float GetBoundsHeight() const { return boundsH_; }

private:
    float boundsX_ = 0, boundsY_ = 0, boundsW_ = 0, boundsH_ = 0;
};

class RSRenderNodeDrawable {
public:
    static RSRenderNodeDrawable Create(std::shared_ptr<RSBaseRenderNode> node);

    void Draw();
    void UpdateCacheInfo();

    std::shared_ptr<RSBaseRenderNode> GetRenderNode() const { return renderNode_.lock(); }

private:
    std::weak_ptr<RSBaseRenderNode> renderNode_;
    std::mutex cacheMutex_;
    std::atomic<uint32_t> drawCount_{0};
    std::string cacheKey_;
};

} // namespace OHOS::Rosen

#endif // RENDER_NODE_H