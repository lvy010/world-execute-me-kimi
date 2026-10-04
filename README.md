# world-execute-me-kimi

这是一个从歌曲到 MP4 的 Kimi 娘音乐视频工程。它吸收了 `world.execute-me-dsh-pv` 的逐帧渲染/ffmpeg 出片方式，也保留了 `world.execute-me-ascii` 的章节、状态栏、双语字幕和随时间变化的终端美学。画面由 Python 逐帧绘制，默认输出 1280×720、24 fps、**3:32（212 秒）**。

## 你需要先准备什么

只需要先准备一份你有权使用的歌曲：

```text
world-execute-me-kimi/input/song.mp3
```

可选地再准备：

- `input/lyrics.lrc`：同步歌词；
- `input/kimi.png`：你希望使用的 Kimi 娘立绘，透明 PNG 最佳。

歌曲和角色图不随代码分发。没有角色图也没关系，工程内置了一个可运行的程序绘制角色。

## macOS 一次性安装

在“终端”中执行：

```sh
cd /Users/user/1005exe/world-execute-me-kimi
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
brew install ffmpeg                 # 已安装可跳过
```

检查工具和输入：

```sh
python kimi_video.py check
```

## 先看单帧和短预览

不需要歌曲就可以验证画面：

```sh
python kimi_video.py frame --time 42 --output preview/42.png
python kimi_video.py preview --seconds 8 --fps 12
```

预览默认使用静音轨道，输出 `out/kimi_preview.mp4`。可以用 `--audio input/song.mp3` 让预览带上歌曲。

## 输出完整 3:32 视频

把歌曲放好后执行：

```sh
python kimi_video.py render
```

输出：

```text
out/kimi_master.mp4   # 逐帧渲染后的母版
out/kimi.mp4          # 带音频、H.264/AAC、可直接播放的交付文件
```

默认渲染会把音频和画面裁切/补齐到 212 秒。想先用较低分辨率测试整条链路：

```sh
python kimi_video.py render --width 640 --height 360 --fps 12 --output out/kimi_test.mp4
```

正式交付建议使用默认参数；如果希望保留中间 PNG 帧，可加 `--frames-dir out/frames`，否则帧会通过管道直接送进 ffmpeg，不会占用大量磁盘空间。

## 运行流程

```text
歌曲/歌词/立绘
      ↓
check → LRC 解析 → 每帧绘制 Kimi 娘世界 → ffmpeg 编码
      ↓
out/kimi.mp4（3:32）
```

第一次完整渲染前，我建议你把 `frame --time 0`、`frame --time 110`、`frame --time 180` 生成的三张图发给我或先自己查看；我们可以据此调整 Kimi 娘的颜色、服装、字幕位置和故障强度，再渲染最终版。

## 权利与署名

请只放入你有权使用的音乐、歌词和角色图。这个仓库只包含代码和程序生成的默认画面，不包含参考项目中的歌曲、歌词原文或第三方模型。

