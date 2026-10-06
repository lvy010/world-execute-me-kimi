# NOTICE：第三方素材与许可

本仓库代码按 [LICENSE](LICENSE)（MIT）发布。第三方素材不随代码许可转让，仍由各自权利人控制。

## Kimi 角色素材

- `film/third_party_references/kimi_reference_20261005/maid-left.webp` 是 Kimi 角色立绘。
- `film/third_party_references/kimi_reference_20261005/kimi-study.webp` 是场景参考图。
- `film/third_party_references/kimi_reference_20261005/expressions/cat-*.webp` 是本项目使用的猫咪表情变体。
- 页面头像、记忆卡片、字符画和替身帧均由上述 Kimi 素材在构建时派生。

角色素材的作者、授权范围和商用条件不由本仓库的 MIT 许可改变。发布改编素材时请保留你取得素材时的授权记录，并遵守相应的非商业与署名要求。

## hakimi web 前端

- `film/vendor/kimi-web-frontend/` 和 `film/vendor/kimi-client-ui-cordis/` 保留上游前端 bundle、包信息和许可证。
- `film/kimi_web_frontend_20260927/kimi_components.css` 是从上游组件包提取的样式，按其 MIT 许可保留。
- 前端 bundle 内的 React、JSX runtime、React DOM 和 scheduler 许可见 [LICENSES/React-MIT.txt](LICENSES/React-MIT.txt)。

## 字体

- `film/ai_mascot_mv_world_execute_20260926/fonts/` 中的 Space Mono Bold 与 Anton Regular 按各自 OFL 文本分发。
- Consolas、微软雅黑和 Segoe UI Symbol 使用系统字体，不随仓库分发。

## 不在本仓库里的

| 东西 | 权利人 | 获取方式 |
|---|---|---|
| `world.execute(me);` | Mili | 自备音频，放到 `input/song.mp3` |
| 歌词 | Mili | 构建时从 LRCLIB 获取或自备 LRC；本仓库只保存不含文字的时间数据 |
| 替身舞者帧 | 本项目构建产物 | 由 `tools/placeholder_h3.py` 使用 Kimi 立绘生成 |

音乐和歌词的权利不包含在本仓库代码许可中。发布视频时请遵守 [Mili 官方使用指引](https://projectmili.com/copyright-guidelines)。

## 声明

这是非官方 Kimi 同人项目，与 Moonshot AI、Mili 或素材作者没有从属或合作关系，也未经其认可。
