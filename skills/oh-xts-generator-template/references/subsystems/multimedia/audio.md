# Audio 模块配置

## 模块基础信息

- **模块名称**: audio
- **中文描述**: 音频模块
- **API定义文件**: `/interface/sdk-js/api/@ohos.multimedia.audio.d.ts`

## 主要接口

### 1. 音频管理接口

#### AudioManager
获取方式: `audio.getAudioManager()`

主要方法:
- `getDevices(deviceFlag: DeviceFlag): Promise<AudioDeviceDescriptors>` - 获取设备列表
- `setActiveDevice(deviceType: DeviceType, active: boolean): Promise<void>` - 设置活跃设备
- `setVolume(volumeType: AudioVolumeType, volume: number): Promise<void>` - 设置音量
- `getVolume(volumeType: AudioVolumeType): Promise<number>` - 获取音量
- `getMaxVolume(volumeType: AudioVolumeType): Promise<number>` - 获取最大音量
- `getMinVolume(volumeType: AudioVolumeType): Promise<number>` - 获取最小音量
- `setMute(volumeType: AudioVolumeType, mute: boolean): Promise<void>` - 设置静音
- `isMute(volumeType: AudioVolumeType): Promise<boolean>` - 获取静音状态
- `setRingerMode(mode: AudioRingMode): Promise<void>` - 设置铃声模式
- `getRingerMode(): Promise<AudioRingMode>` - 获取铃声模式

### 2. 音频渲染接口 (AudioRenderer)

创建方式: `audio.createAudioRenderer(options: AudioRendererOptions)`

主要方法:
- `start(): Promise<void>` - 开始播放
- `write(buffer: ArrayBuffer): Promise<number>` - 写入音频数据
- `pause(): Promise<void>` - 暂停播放
- `stop(): Promise<void>` - 停止播放
- `release(): Promise<void>` - 释放资源
- `getRendererState(): AudioState` - 获取渲染状态
- `getBufferSize(): Promise<number>` - 获取缓冲区大小
- `getAudioTime(): Promise<number>` - 获取当前时间
- `getStreamInfo(): AudioStreamInfo` - 获取流信息
- `getRendererInfo(): AudioRendererInfo` - 获取渲染器信息
- `setSpeed(speed: number): Promise<void>` - 设置播放速度
- `getSpeed(): number` - 获取播放速度
- `setVolume(vol: number): Promise<void>` - 设置音量
- `getVolume(): number` - 获取音量

### 3. 音频捕获接口 (AudioCapturer)

创建方式: `audio.createAudioCapturer(options: AudioCapturerOptions)`

主要方法:
- `start(): Promise<void>` - 开始录音
- `read(bufferSize: number): Promise<ArrayBuffer>` - 读取音频数据
- `pause(): Promise<void>` - 暂停录音
- `stop(): Promise<void>` - 停止录音
- `release(): Promise<void>` - 释放资源
- `getCapturerState(): AudioState` - 获取捕获状态
- `getAudioTime(): Promise<number>` - 获取当前时间
- `getStreamInfo(): AudioStreamInfo` - 获取流信息
- `getCapturerInfo(): AudioCapturerInfo` - 获取捕获器信息
- `getBufferSize(): Promise<number>` - 获取缓冲区大小

## 模块差异化配置

### 1. 测试策略

#### AudioRenderer 测试重点
- 状态转换测试 (NEW -> PREPARED -> RUNNING -> PAUSED -> STOPPED -> RELEASED)
- 播放控制测试 (start, pause, stop)
- 音量控制测试 (setVolume, getVolume)
- 速度控制测试 (setSpeed, getSpeed)
- 写入数据测试 (write)
- 错误处理测试 (非法参数、状态错误)

#### AudioCapturer 测试重点
- 状态转换测试 (NEW -> PREPARED -> RUNNING -> PAUSED -> STOPPED -> RELEASED)
- 录音控制测试 (start, pause, stop)
- 读取数据测试 (read)
- 错误处理测试 (非法参数、状态错误)

### 2. 常用配置参数

#### 音频流配置
```typescript
const audioStreamInfo: audio.AudioStreamInfo = {
  samplingRate: audio.AudioSamplingRate.SAMPLE_RATE_48000,
  channels: audio.AudioChannel.CHANNEL_2,
  sampleFormat: audio.AudioSampleFormat.SAMPLE_FORMAT_S16LE,
  encodingType: audio.AudioEncodingType.ENCODING_TYPE_RAW
};
```

#### 音频渲染器配置
```typescript
const audioRendererInfo: audio.AudioRendererInfo = {
  usage: audio.StreamUsage.STREAM_USAGE_MUSIC,
  rendererFlags: 0
};

const audioRendererOptions: audio.AudioRendererOptions = {
  streamInfo: audioStreamInfo,
  rendererInfo: audioRendererInfo
};
```

#### 音频捕获器配置
```typescript
const audioCapturerInfo: audio.AudioCapturerInfo = {
  source: audio.SourceType.SOURCE_TYPE_MIC,
  capturerFlags: 0
};

const audioCapturerOptions: audio.AudioCapturerOptions = {
  streamInfo: audioStreamInfo,
  capturerInfo: audioCapturerInfo
};
```

### 3. 关键枚举值

#### 采样率 (AudioSamplingRate)
- SAMPLE_RATE_8000 = 8000
- SAMPLE_RATE_16000 = 16000
- SAMPLE_RATE_44100 = 44100
- SAMPLE_RATE_48000 = 48000

#### 声道数 (AudioChannel)
- CHANNEL_1 = 1
- CHANNEL_2 = 2

#### 采样格式 (AudioSampleFormat)
- SAMPLE_FORMAT_U8 = 0
- SAMPLE_FORMAT_S16LE = 1
- SAMPLE_FORMAT_S24LE = 2
- SAMPLE_FORMAT_S32LE = 3
- SAMPLE_FORMAT_F32LE = 4

#### 使用场景 (StreamUsage)
- STREAM_USAGE_UNKNOWN = 0
- STREAM_USAGE_MEDIA = 1
- STREAM_USAGE_VOICE_COMMUNICATION = 2
- STREAM_USAGE_VOICE_ASSISTANT = 3
- STREAM_USAGE_ALARM = 4
- STREAM_USAGE_NOTIFICATION = 5
- STREAM_USAGE_RINGTONE = 6
- STREAM_USAGE_MUSIC = 7

#### 音频源类型 (SourceType)
- SOURCE_TYPE_INVALID = 0
- SOURCE_TYPE_MIC = 1
- SOURCE_TYPE_VOICE_UPLINK = 2
- SOURCE_TYPE_VOICE_DOWNLINK = 3
- SOURCE_TYPE_VOICE_CALL = 4

#### 音频状态 (AudioState)
- STATE_INVALID = -1
- STATE_NEW = 0
- STATE_PREPARED = 1
- STATE_RUNNING = 2
- STATE_STOPPED = 3
- STATE_RELEASED = 4
- STATE_PAUSED = 5

### 4. 测试用例优先级

**高优先级接口**:
1. AudioRenderer - start/stop/pause/write
2. AudioCapturer - start/stop/pause/read
3. AudioManager - setVolume/getVolume

**中优先级接口**:
1. AudioRenderer - setSpeed/getSpeed
2. AudioRenderer - getBufferSize
3. AudioCapturer - getBufferSize

**低优先级接口**:
1. AudioManager - 设备管理相关接口
2. AudioRenderer - 高级特性 (如loudness gain)
3. AudioCapturer - 高级特性

### 5. 特殊注意事项

1. **权限要求**:
   - AudioCapturer 需要麦克风权限
   - 某些 AudioManager 接口需要系统权限

2. **状态机约束**:
   - 必须按照状态顺序调用方法
   - 某些操作只能在特定状态下执行

3. **资源管理**:
   - 测试完成必须释放资源
   - 建议使用 try-finally 确保释放

4. **异步等待**:
   - 某些状态转换需要时间
   - 建议添加适当延时

5. **设备可用性**:
   - 测试前检查设备是否可用
   - 某些设备类型可能不存在
