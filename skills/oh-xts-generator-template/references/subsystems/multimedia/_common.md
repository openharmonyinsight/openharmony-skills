# Multimedia 子系统配置

## 子系统基础信息

- **子系统名称**: multimedia
- **中文描述**: 多媒体子系统
- **主要模块**:
  - audio - 音频模块
  - image - 图像模块
  - camera - 相机模块
  - media - 媒体播放模块

## 子系统差异化配置

### 1. API 定义文件位置

Audio模块的API定义文件位于:
```
/interface/sdk-js/api/@ohos.multimedia.audio.d.ts
/interface/sdk-js/api/@ohos.multimedia.audioHaptic.d.ts
```

### 2. 测试文件位置

Audio模块的测试文件位于:
```
/test/xts/acts/multimedia/audio/audio_js_standard/
```

### 3. 子系统特有规则

#### 3.1 音频模块特性

Audio模块测试需要注意以下特性:

1. **设备依赖性**: AudioRenderer 和 AudioCapturer 创建可能依赖实际音频设备
2. **权限要求**: 某些操作需要特殊权限，如麦克风权限
3. **异步操作**: 大部分API都是异步的，需要使用async/await
4. **状态管理**: AudioRenderer/AudioCapturer 有明确的状态机，需要按照状态流程操作

#### 3.2 常用配置参数

- **AudioStreamInfo**:
  - samplingRate: 采样率 (SAMPLE_RATE_48000, SAMPLE_RATE_44100等)
  - channels: 声道数 (CHANNEL_1, CHANNEL_2等)
  - sampleFormat: 采样格式 (SAMPLE_FORMAT_S16LE, SAMPLE_FORMAT_F32LE等)
  - encodingType: 编码类型 (ENCODING_TYPE_RAW)

- **AudioRendererInfo**:
  - usage: 使用场景 (STREAM_USAGE_MUSIC, STREAM_USAGE_MEDIA等)
  - rendererFlags: 渲染标志

- **AudioCapturerInfo**:
  - source: 音频源类型 (SOURCE_TYPE_MIC, SOURCE_TYPE_VOICE_COMMUNICATION等)
  - capturerFlags: 捕获标志

#### 3.3 错误码处理

Audio模块的错误码范围: 6800101 - 6800301

常见错误码:
- 6800101: ERROR_INVALID_PARAM - 参数无效
- 6800102: ERROR_NO_MEMORY - 内存分配失败
- 6800103: ERROR_ILLEGAL_STATE - 状态不合法
- 6800104: ERROR_UNSUPPORTED - 不支持的功能
- 6800105: ERROR_TIMEOUT - 超时
- 6800201: ERROR_STREAM_LIMIT - 流限制
- 6800301: ERROR_SYSTEM - 系统错误

#### 3.4 测试用例编号规则

格式: `SUB_MULTIMEDIA_AUDIO_[API名称]_[类型]_[序号]`

类型包括:
- PARAM - 参数测试
- ERROR - 错误码测试
- RETURN - 返回值测试
- BOUNDARY - 边界值测试

#### 3.5 测试注意事项

1. **资源释放**: 测试完成后必须释放AudioRenderer/AudioCapturer资源
2. **状态转换**: 必须按照正确的状态顺序调用方法
3. **异步等待**: 某些状态转换需要等待，使用适当延时
4. **设备可用性**: 某些测试需要检测设备是否可用

## 测试模板

### AudioRenderer 测试模板

```typescript
import audio from '@ohos.multimedia.audio';

describe("AudioRendererTest", () => {
  it("SUB_MULTIMEDIA_AUDIO_XXX_001", Level.LEVEL0, async (done: Function) => {
    let audioStreamInfo: audio.AudioStreamInfo = {
      samplingRate: audio.AudioSamplingRate.SAMPLE_RATE_48000,
      channels: audio.AudioChannel.CHANNEL_2,
      sampleFormat: audio.AudioSampleFormat.SAMPLE_FORMAT_S16LE,
      encodingType: audio.AudioEncodingType.ENCODING_TYPE_RAW
    };

    let audioRendererInfo: audio.AudioRendererInfo = {
      usage: audio.StreamUsage.STREAM_USAGE_MUSIC,
      rendererFlags: 0
    };

    let audioRendererOptions: audio.AudioRendererOptions = {
      streamInfo: audioStreamInfo,
      rendererInfo: audioRendererInfo
    };

    try {
      let audioRenderer = await audio.createAudioRenderer(audioRendererOptions);
      // 测试逻辑
      expect(result).assertTrue();
      audioRenderer.release();
      done();
    } catch (error) {
      console.error(`Test failed: ${error}`);
      expect(false).assertTrue();
      done();
    }
  });
});
```

### AudioCapturer 测试模板

```typescript
import audio from '@ohos.multimedia.audio';

describe("AudioCapturerTest", () => {
  it("SUB_MULTIMEDIA_AUDIO_XXX_001", Level.LEVEL0, async (done: Function) => {
    let audioStreamInfo: audio.AudioStreamInfo = {
      samplingRate: audio.AudioSamplingRate.SAMPLE_RATE_48000,
      channels: audio.AudioChannel.CHANNEL_2,
      sampleFormat: audio.AudioSampleFormat.SAMPLE_FORMAT_S16LE,
      encodingType: audio.AudioEncodingType.ENCODING_TYPE_RAW
    };

    let audioCapturerInfo: audio.AudioCapturerInfo = {
      source: audio.SourceType.SOURCE_TYPE_MIC,
      capturerFlags: 0
    };

    let audioCapturerOptions: audio.AudioCapturerOptions = {
      streamInfo: audioStreamInfo,
      capturerInfo: audioCapturerInfo
    };

    try {
      let audioCapturer = await audio.createAudioCapturer(audioCapturerOptions);
      // 测试逻辑
      expect(result).assertTrue();
      audioCapturer.release();
      done();
    } catch (error) {
      console.error(`Test failed: ${error}`);
      expect(false).assertTrue();
      done();
    }
  });
});
```
