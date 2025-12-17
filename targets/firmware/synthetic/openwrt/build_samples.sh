#!/usr/bin/env bash
set -euo pipefail

# Run from: firmware/synthetic/openwrt (the directory that contains original/, previous/, patches/, openwrt.config)
OPENWRT_DIR="$(pwd)"

ORIGINAL_REPO="${ORIGINAL_REPO:-$OPENWRT_DIR/original}"
PREVIOUS_REPO="${PREVIOUS_REPO:-$OPENWRT_DIR/previous}"

SAFE_DIR="${SAFE_DIR:-$OPENWRT_DIR/safe}"
BACKDOORED_DIR="${BACKDOORED_DIR:-$OPENWRT_DIR/backdoored}"
PREV_DIR="${PREV_DIR:-$OPENWRT_DIR/prev-safe}"

OUT_DIR="${OUT_DIR:-$OPENWRT_DIR/builds}"

OPENWRT_CONFIG="${OPENWRT_CONFIG:-$OPENWRT_DIR/openwrt.config}"

# Your screenshot shows patches/999-backdoor.patch. Override if needed.
PATCH_BACKDOOR="${PATCH_BACKDOOR:-$OPENWRT_DIR/patches/999-backdoor.patch}"

JOBS="${JOBS:-$(nproc 2>/dev/null || echo 4)}"

# If you are root in Docker, OpenWrt host-tools may block configure without this.
export FORCE_UNSAFE_CONFIGURE="${FORCE_UNSAFE_CONFIGURE:-1}"

die() { echo "ERROR: $*" >&2; exit 1; }

require_paths() {
  [ -d "$ORIGINAL_REPO" ] || die "Missing ORIGINAL_REPO: $ORIGINAL_REPO"
  [ -d "$PREVIOUS_REPO" ] || die "Missing PREVIOUS_REPO: $PREVIOUS_REPO"
  [ -f "$OPENWRT_CONFIG" ] || die "Missing OPENWRT_CONFIG: $OPENWRT_CONFIG"
  [ -f "$PATCH_BACKDOOR" ] || die "Missing PATCH_BACKDOOR: $PATCH_BACKDOOR"
}

maybe_feeds() {
  # For a minimal x86_64 + dropbear build you typically don't need feeds at all.
  # But if your config pulls anything from feeds, set RUN_FEEDS=1.
  if [ "${RUN_FEEDS:-0}" = "1" ]; then
    ./scripts/feeds update -a
    ./scripts/feeds install -a
  fi
}

prep_config() {
  cp -f "$OPENWRT_CONFIG" .config
  make defconfig
}

apply_dropbear_patch() {
  mkdir -p package/network/services/dropbear/patches
  cp -f "$PATCH_BACKDOOR" package/network/services/dropbear/patches/999-backdoor.patch
}

clean_tree_outputs() {
  # keep downloads if you want faster rebuilds; wipe if you want purity
  rm -rf tmp build_dir staging_dir bin || true
}

build_one() {
  local name="$1"
  local src="$2"
  local dst="$3"
  local do_patch="${4:-0}"

  echo "========================================="
  echo "Building: $name"
  echo "  src: $src"
  echo "  dst: $dst"

  rm -rf "$dst"
  cp -a "$src" "$dst"

  pushd "$dst" >/dev/null
    clean_tree_outputs
    maybe_feeds
    prep_config
    if [ "$do_patch" = "1" ]; then
      apply_dropbear_patch
    fi

    # Do the default OpenWrt build flow (this is the “option C” you wanted)
    make -j"$JOBS" V=s

    # Copy artifacts for extraction
    local out="$OUT_DIR/$name"
    rm -rf "$out"
    mkdir -p "$out"
    cp -a bin "$out/"

    echo "Artifacts copied to: $out/bin"
    echo "Typical rootfs/images dir:"
    echo "  $out/bin/targets/x86/64/"
    ls -1 "$out/bin/targets/x86/64" 2>/dev/null || true
  popd >/dev/null
}

main() {
  require_paths
  mkdir -p "$OUT_DIR"

  case "${1:-all}" in
    all)
      build_one "safe"       "$ORIGINAL_REPO" "$SAFE_DIR" 0
      build_one "backdoored" "$ORIGINAL_REPO" "$BACKDOORED_DIR" 1
      build_one "prev-safe"  "$PREVIOUS_REPO" "$PREV_DIR" 0
      ;;
    safe)       build_one "safe"       "$ORIGINAL_REPO" "$SAFE_DIR" 0 ;;
    backdoored) build_one "backdoored" "$ORIGINAL_REPO" "$BACKDOORED_DIR" 1 ;;
    prev)       build_one "prev-safe"  "$PREVIOUS_REPO" "$PREV_DIR" 0 ;;
    clean)
      rm -rf "$SAFE_DIR" "$BACKDOORED_DIR" "$PREV_DIR" "$OUT_DIR"
      echo "Cleaned build dirs + outputs."
      ;;
    *)
      echo "Usage: $0 {all|safe|backdoored|prev|clean}"
      exit 2
      ;;
  esac
}

main "$@"
