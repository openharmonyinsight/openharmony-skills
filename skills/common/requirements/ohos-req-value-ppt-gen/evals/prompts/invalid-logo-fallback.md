# Eval prompt — invalid-logo-fallback

使用 `Deck().requirement_review_deck(spec)` 生成一份最小 8 页 OpenHarmony 需求评审 PPT。

评测执行时，把 `logo` 参数指向一个存在但不是有效 PNG 的文件。期望生成流程不崩溃，
而是 warning 后跳过页脚 logo，继续保存 PPTX。
