# Team Mapping

Only read this file when a violation needs the `team` field.

## Routing Heuristics

Use the most specific visible owner in this order:

1. File path or namespace owner, if obvious.
2. Directly accessed object or subsystem, such as NWeb, WebContents, GPU, Audio, mojo, storage, networking.
3. Standard rule context, only when path/object ownership is still unclear.
4. Nearest functional team from the table; explain the basis in `issue` when confidence is low.

Examples:
- `mojo::Connector`, mojo receiver binding, IPC plumbing: 基础框架.
- `WebContents`, `RenderFrameHost`, `NavigationController`, page loading: 网页浏览.
- NWeb object lifecycle, JSBridge-facing callback: 应用交互 unless the file path clearly belongs to another module.
- GPU mojo, `compositor_gpu_thread_`, rendering compositor: 渲染合成.
- Audio start/pause/stop/close, media playback path: 多媒体.
- Browser prefs, LocalStorage, Cache, IndexedDB: 存储.
- Logging, trace, crash dump only: DFX.

Do not invent a new team. If two teams are plausible, choose the team that owns the object being accessed, not the caller that happened to trigger the callback.

| 团队 | 职责范围 |
|------|---------|
| 交互安全 | 组件创建与生命周期、底座安全（沙箱隔离、站点隔离、内存安全增强）、跨平台 |
| 渲染引擎 | 渲染引擎核心 |
| 渲染合成 | 字体管理、深色模式、渲染模式、扩展安全区域、同层渲染、网页截图、网页缩放、全屏处理、LTR处理、Web组件帧率管控、独立GPU进程 |
| 交互动效 | 与原生界面交互（JS警告框、Toast、上下文菜单、右键菜单）、多模输入事件处理、密码填充 |
| 网络 | 网站证书管理、自定义网络（网络代理、自定义DNS、网页资源拦截、网络托管） |
| 网页浏览 | 网页加载、运行JS、postMessage、应用安全、内核升级、DevTools |
| 应用交互 | JSBridge、广告拦截、JSBridge管控 |
| 扩展 | 浏览器扩展 |
| 多媒体 | HEIF图片、网页音视频播放、网页摄像头、WebRTC、对接编解码、对接播控中心、PDF/Office |
| 存储 | IndexDB、LocalStorage、WebSQL、Cache |
| 外设服务 | 南向外设业务、打印、蓝牙、定位 |
| 全球化 | 多语言支持、网页翻译 |
| 无障碍 | 无障碍服务 |
| DFX | DFX基础服务、Logging、Trace、Crashdump |
| 性能 | 网络加速、Web组件资源调度 |
| 构建工程 | 编译框架、CICD基础设施 |
| 基础框架 | 基础库、IPC、MOJO基础服务 |
| JavaScript引擎 | V8引擎及JavaScript语言相关能力 |
| 新兴技术组 | WebAssembly、Web ML、AR/VR |
