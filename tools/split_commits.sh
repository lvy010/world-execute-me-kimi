#!/usr/bin/env bash
set -euo pipefail

# Create a reviewable sequence of small commits for this project.
# This script commits locally only. It never pushes and it deliberately leaves
# the uploaded song, generated out/ files, and generated screenshot caches out
# of the history.

repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root"

commit_paths() {
  local message="$1"
  shift
  local paths=()
  local path
  for path in "$@"; do
    if [[ -e "$path" ]] || [[ -n "$(git ls-files -- "$path")" ]]; then
      paths+=("$path")
    fi
  done
  if (( ${#paths[@]} == 0 )); then
    return 0
  fi
  git add -A -- "${paths[@]}"
  if git diff --cached --quiet; then
    return 0
  fi
  git commit -m "$message"
}

commit_paths "chore: add repository metadata and commit helper" \
  .gitignore LICENSE tools/split_commits.sh
commit_paths "docs: add third-party license texts" LICENSES
commit_paths "docs: describe the Kimi adaptation" README.md KIMI_ADAPTATION.md NOTICE.md
commit_paths "docs: record Kimi asset boundaries" docs
commit_paths "build: add package manifests and Python requirements" package.json package-lock.json requirements.txt
commit_paths "docs: explain local audio and lyric inputs" input/README.md
commit_paths "build: add the reproducible render entry point" build.py
commit_paths "data: add timing and stand-in manifests" data
commit_paths "tools: add lyric acquisition utilities" tools/lyrics.py
commit_paths "tools: generate Kimi stand-in motion" tools/placeholder_h3.py
commit_paths "assets: add shared film fonts" film/ai_mascot_mv_world_execute_20260926/fonts
commit_paths "assets: add Kimi character references" film/third_party_references/kimi_reference_20261005
commit_paths "motion: add timing and motion evaluation" film/mmd_motion_eval_20260927
commit_paths "frontend: add the web bundle" film/vendor/kimi-web-frontend
commit_paths "frontend: add the Cordis bundle" film/vendor/kimi-client-ui-cordis
commit_paths "frontend: add shared HTML frame helpers" film/kimi_web_frontend_20260927/build_frame.py film/kimi_web_frontend_20260927/kimi_components.css film/kimi_web_frontend_20260927/icons.py
commit_paths "frontend: add the shared page renderer" film/kimi_web_frontend_20260927/seg_page.py
commit_paths "frontend: add boot page choreography" film/kimi_web_frontend_20260927/batch_a1.py
commit_paths "frontend: add pretraining page choreography" film/kimi_web_frontend_20260927/batch_a2.py
commit_paths "frontend: add identity page choreography" film/kimi_web_frontend_20260927/batch_a3.py
commit_paths "frontend: add alignment page choreography" film/kimi_web_frontend_20260927/batch_b.py
commit_paths "frontend: add deployment page choreography" film/kimi_web_frontend_20260927/batch_c.py
commit_paths "frontend: add context page choreography" film/kimi_web_frontend_20260927/batch_e.py
commit_paths "frontend: add execution page choreography" film/kimi_web_frontend_20260927/batch_f.py
commit_paths "frontend: add outro page choreography" film/kimi_web_frontend_20260927/batch_g.py
commit_paths "frontend: add wave and page utilities" \
  film/kimi_web_frontend_20260927/kimi_her.py \
  film/kimi_web_frontend_20260927/kimi_wave.py \
  film/kimi_web_frontend_20260927/kimi_gpu.py \
  film/kimi_web_frontend_20260927/extract_css.py \
  film/kimi_web_frontend_20260927/seg_shot.mjs \
  film/kimi_web_frontend_20260927/sung_words.py
commit_paths "frontend: add visual patch modules" \
  film/kimi_web_frontend_20260927/kimi_patch_fix.py \
  film/kimi_web_frontend_20260927/kimi_patch_r1.py \
  film/kimi_web_frontend_20260927/kimi_patch_e.py \
  film/kimi_web_frontend_20260927/kimi_patch_f.py \
  film/kimi_web_frontend_20260927/kimi_patch_g.py \
  film/kimi_web_frontend_20260927/kimi_patch_mem.py \
  film/kimi_web_frontend_20260927/f2_closeup.py
commit_paths "frontend: add generated avatar and memory assets" \
  film/kimi_web_frontend_20260927/avatars \
  film/kimi_web_frontend_20260927/cat_stills \
  film/kimi_web_frontend_20260927/mem_sprites
commit_paths "frontend: add runtime maps and transition audio" \
  film/kimi_web_frontend_20260927/chime_g.wav \
  film/kimi_web_frontend_20260927/cursor.json \
  film/kimi_web_frontend_20260927/disclosure_map.json
commit_paths "tui: add terminal drawing primitives" film/tui_pv_world_execute_20260926/tuikit.py
commit_paths "tui: add first generation scene engine" film/tui_pv_world_execute_20260926/full
commit_paths "tui: add continuity director foundations" \
  film/tui_pv_world_execute_20260926/continuity_full_v1 \
  film/tui_pv_world_execute_20260926/continuity_full_v2/v2.py \
  film/tui_pv_world_execute_20260926/continuity_full_v2/cuts.py \
  film/tui_pv_world_execute_20260926/continuity_full_v2/kit.py \
  film/tui_pv_world_execute_20260926/continuity_full_v2/words.py \
  film/tui_pv_world_execute_20260926/continuity_full_v2/grok_rig.py \
  film/tui_pv_world_execute_20260926/continuity_full_v2/h3_full.py
commit_paths "tui: add boot and pretraining scenes" \
  film/tui_pv_world_execute_20260926/continuity_full_v2/scenes_boot.py \
  film/tui_pv_world_execute_20260926/continuity_full_v2/s_boot.py \
  film/tui_pv_world_execute_20260926/continuity_full_v2/scenes.py \
  film/tui_pv_world_execute_20260926/continuity_full_v2/s_pretrain.py \
  film/tui_pv_world_execute_20260926/continuity_full_v2/s_sft.py \
  film/tui_pv_world_execute_20260926/continuity_full_v2/scenes_sft.py
commit_paths "tui: add deployment scenes" \
  film/tui_pv_world_execute_20260926/continuity_full_v2/scenes_deploy.py \
  film/tui_pv_world_execute_20260926/continuity_full_v2/s_deploy.py
commit_paths "tui: add evaluation scenes" \
  film/tui_pv_world_execute_20260926/continuity_full_v2/scenes_eval.py \
  film/tui_pv_world_execute_20260926/continuity_full_v2/s_eval.py
commit_paths "tui: add execution scenes" \
  film/tui_pv_world_execute_20260926/continuity_full_v2/scenes_exec.py \
  film/tui_pv_world_execute_20260926/continuity_full_v2/s_exec.py
commit_paths "tui: add reward scenes" \
  film/tui_pv_world_execute_20260926/continuity_full_v2/scenes_reward.py \
  film/tui_pv_world_execute_20260926/continuity_full_v2/s_reward.py
commit_paths "tui: add user-left scenes" \
  film/tui_pv_world_execute_20260926/continuity_full_v2/scenes_userleft.py \
  film/tui_pv_world_execute_20260926/continuity_full_v2/s_userleft.py
commit_paths "tui: add chorus and transition scenes" \
  film/tui_pv_world_execute_20260926/continuity_full_v2/scenes_chorus1.py \
  film/tui_pv_world_execute_20260926/continuity_full_v2/scenes_chorus2.py \
  film/tui_pv_world_execute_20260926/continuity_full_v2/s_chorus1.py \
  film/tui_pv_world_execute_20260926/continuity_full_v2/s_chorus2.py \
  film/tui_pv_world_execute_20260926/continuity_full_v2/s_final.py
commit_paths "tui: add sidebar and ASCII experiments" \
  film/tui_pv_world_execute_20260926/sidebar_chorus_v1 \
  film/tui_pv_world_execute_20260926/video_ascii_v1 \
  film/mmd_motion_eval_20260927/pv_full.py
commit_paths "chore: remove superseded prototype files" \
  ASSET_CREDITS.md assets config.json kimi_video.py render.sh run.sh

echo
echo "Local commit sequence complete. Nothing was pushed."
echo "Review the remaining status before uploading:"
git status --short
