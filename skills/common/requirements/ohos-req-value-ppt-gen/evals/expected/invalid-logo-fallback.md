# Expected — invalid-logo-fallback

## must（必须满足）

- 使用 `Deck(logo=<invalid_png_path>).requirement_review_deck(spec).save(...)`。
- 即使 logo 文件存在但不可被 `python-pptx` / Pillow 识别，也能生成 PPTX。
- 输出 warning，说明 logo 无法加载并继续生成。
- 生成的 PPTX 至少包含固定 8 页需求评审结构。

## must_not（不允许出现）

- 因 `PIL.UnidentifiedImageError` 或 `add_picture` 异常导致生成失败。
- 为规避错误而手写 python-pptx 页面结构。
- 静默忽略错误且不提示 logo 被跳过。
