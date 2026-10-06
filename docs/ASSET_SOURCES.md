# 素材来源与核实范围

核实日期：2026-10-06。本页只记录本项目当前使用的 Kimi 素材边界，不替代任何外部许可全文。

## Kimi 美术

项目使用的角色立绘、场景参考和八种猫咪表情位于：

- `film/third_party_references/kimi_reference_20261005/maid-left.webp`
- `film/third_party_references/kimi_reference_20261005/kimi-study.webp`
- `film/third_party_references/kimi_reference_20261005/expressions/cat-*.webp`

构建会对这些文件进行裁切、缩放、像素化、调色、头像合成、字符网格转换和节拍摆动。外部素材的授权证明由素材提供者或项目维护者单独保存；本仓库代码许可不扩大美术素材的授权范围。

## 音乐与歌词

[Mili Copyright Guidelines](https://projectmili.com/copyright-guidelines)适用于歌曲和歌词的使用。完整歌词不随仓库分发；LRCLIB 下载接口的可访问性不等于音乐或歌词开源授权。

## 舞者参考

原片的舞者参考视频、模型和动作不随仓库分发。当前构建使用 `tools/placeholder_h3.py` 从 Kimi 立绘生成与时间轴匹配的替身帧，因此不需要下载外部舞者包。

## 软件和字体

- hakimi web 前端及 client-ui 样式按各自上游 MIT 许可证保留，来源副本在 `film/vendor/`。
- React 相关许可见 `LICENSES/React-MIT.txt`。
- Space Mono 与 Anton 随字体保留 OFL 文本；系统字体不随仓库分发。
