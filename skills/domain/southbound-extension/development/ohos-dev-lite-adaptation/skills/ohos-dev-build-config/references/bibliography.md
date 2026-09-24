# 参考资料汇总 — 编译构建配置器

---

## 1. 官方文档

1. **OpenHarmony编译构建子系统文档**  
   https://gitcode.com/openharmony/docs/blob/master/zh-cn/device-dev/subsystems/subsys-build-mini-lite.md

2. **构建系统编码规范与最佳实践**  
   https://gitcode.com/openharmony/docs/blob/master/zh-cn/device-dev/subsystems/subsys-build-gn-coding-style-and-best-practice.md

3. **productdefine_common产品配置仓库**（注：Lite系统使用vendor目录下的config.json，此仓库主要面向标准系统）  
   https://gitcode.com/openharmony/productdefine_common.git

4. **build_lite编译框架仓库** ⭐  
   https://github.com/openharmony/build_lite

5. **OpenHarmony官方文档站**  
   https://docs.openharmony.cn/

## 2. 技术文章

6. **OpenHarmony开发——GN快速上手**  
   https://zhuanlan.zhihu.com/p/679846981

7. **GN和Ninja的构建流程详解**  
   https://laval.csdn.net/67222b2a2db35d119502bd9c.html

8. **OpenHarmony移植案例：build lite配置目录全梳理**  
   https://cloud.tencent.com/developer/article/2531683

9. **GN语法及在鸿蒙的使用（百篇博客分析）**  
   https://juejin.cn/post/7015965733431541791

10. **如何通过--product-name找到编译明细**  
    https://www.cnblogs.com/riveruns/p/18429524

11. **OpenHarmony如何在鸿蒙开源仓增加新部件**  
    https://zhuanlan.zhihu.com/p/402953291

12. **OpenHarmony LLVM交叉编译工具链介绍**  
    https://huaweicloud.csdn.net/64ddf6599ce083432426b2d5.html

## 3. 移植案例

13. **ASR582X Combo Demo移植指南**  
    https://github.com/openharmony/docs/blob/master/zh-cn/device-dev/porting/porting-asr582x-combo-demo.md

14. **Bestechnic BES2600W Mini系统移植（GitCode 镜像）**  
    https://gitcode.com/openharmony/docs/blob/master/en/device-dev/porting/porting-bes2600w-on-minisystem-display-demo.md

14-1. **⭐ BES2600W Mini系统带屏移植（Gitee 官方 — 中文完整版）**  
    https://gitee.com/openharmony/docs/blob/master/zh-cn/device-dev/porting/porting-bes2600w-on-minisystem-display-demo.md

15. **STM32F407芯片移植实战**  
    https://cloud.tencent.com/developer/article/2535144

16. **一起来看看移植最新版本OpenHarmony到STM32F407**  
    https://zhuanlan.zhihu.com/p/510413799

17. **OpenHarmony LiteOS-M 3.1系统移植实战指南**  
    https://laval.csdn.net/69689a84b7c94a471369028d.html

## 4. 内核和架构

18. **OpenHarmony kernel_liteos_m仓库**  
    https://github.com/openharmony/kernel_liteos_m

19. **RISC-V MCU kernel_liteos_m适配**  
    https://github.com/riscv-mcu/kernel_liteos_m

20. **LiteOS-M内核概述**  
    https://gitcode.com/openharmony/docs/blob/master/en/device-dev/kernel/kernel-mini-overview.md

21. **如何添加新的芯片架构到OH编译工具链**  
    https://zhuanlan.zhihu.com/p/1904272883376718891

## 5. 链接脚本和启动代码

22. **CMSIS ARM Cortex-M通用链接脚本**  
    https://github.com/ARM-software/CMSIS_5/blob/develop/Device/ARM/ARMCM3/Source/GCC/gcc_arm.ld

23. **libopencm3 Cortex-M通用链接脚本**  
    https://github.com/libopencm3/libopencm3/blob/master/lib/cortex-m-generic.ld

24. **LiteOS移植指南：修改链接脚本**  
    https://git.opendao.cn/explore/95ac51caa47741a4a4c406cefbca0759/LiteOS/blob/master?path=doc/LiteOS_Porting_Guide_en/modifying-the-link-script.md

25. **移植OpenHarmony轻量系统：启动文件与链接**  
    https://developer.huawei.com/consumer/cn/blog/topic/03889764091180022

## 6. 构建工具和故障排除

26. **OpenHarmony编译框架概述**  
    https://harmonyosdev.csdn.net/67fdfc0dc7c7e505d345f291.html

27. **FAQ：模块如何单独编译构建**  
    https://forums.openharmony.cn/forum.php?mod=viewthread&tid=2993

28. **Ninja build error故障排查**  
    https://segmentfault.com/q/1010000045091470

29. **OpenHarmony编译系统：架构、隔离与实战**  
    https://www.cnblogs.com/getmoon/p/20294181

30. **深入理解OpenHarmony中的BUILD.gn**  
    https://laval.csdn.net/6968a529bb8be53418ab189d.html
