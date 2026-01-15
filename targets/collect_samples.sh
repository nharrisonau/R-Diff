#!/usr/bin/env bash
set -euo pipefail

# Base paths (override with env vars if needed)
BASE_DIR="${BASE_DIR:-$HOME/rosarum}"
OUT_BASE="${OUT_BASE:-$BASE_DIR/outputs}"

# Variant roots
OUT_NORMAL="${OUT_BASE}/normal"
OUT_STRIPPED="${OUT_BASE}/stripped"

# Strip tool (override if cross toolchain needed)
STRIP_TOOL="${STRIP_TOOL:-strip}"
STRIP_FLAGS=(${STRIP_FLAGS:-"--strip-unneeded"})

copy_bin_to() {
    local src="$1"      # full path to built binary
    local out_root="$2" # ${OUT_NORMAL} or ${OUT_STRIPPED}
    local rel_out="$3"  # e.g., components/... or firmware/...

    local dst_dir="${out_root}/${rel_out}"
    mkdir -p "${dst_dir}"
    echo "Copying ${src} -> ${dst_dir}/"
    cp "${src}" "${dst_dir}/"
}

copy_dir_to() {
    local src="$1"
    local out_root="$2"
    local rel_out="$3"

    local dst_dir="${out_root}/${rel_out}"
    mkdir -p "$(dirname -- "${dst_dir}")"
    echo "Copying dir ${src} -> ${dst_dir}/"
    rm -rf "${dst_dir}"
    cp -a "${src}" "${dst_dir}"
}

maybe_strip_file() {
    local f="$1"
    # Only strip ELF files
    if file -b "$f" | grep -qE '^ELF '; then
        "${STRIP_TOOL}" "${STRIP_FLAGS[@]}" "$f" || {
            echo "WARN: strip failed for $f (continuing)" >&2
        }
    fi
}

strip_tree_elfs() {
    local root="$1"
    while IFS= read -r -d '' f; do
        maybe_strip_file "$f"
    done < <(find "$root" -type f -print0)
}

copy_both_bin() {
    local src="$1"
    local rel_out="$2"

    # normal copy
    copy_bin_to "${src}" "${OUT_NORMAL}" "${rel_out}"

    # stripped copy
    copy_bin_to "${src}" "${OUT_STRIPPED}" "${rel_out}"
    local dst="${OUT_STRIPPED}/${rel_out}/$(basename -- "${src}")"
    maybe_strip_file "${dst}"
}

copy_both_dir() {
    local src="$1"
    local rel_out="$2"

    # normal copy
    copy_dir_to "${src}" "${OUT_NORMAL}" "${rel_out}"

    # stripped copy
    copy_dir_to "${src}" "${OUT_STRIPPED}" "${rel_out}"
    strip_tree_elfs "${OUT_STRIPPED}/${rel_out}"
}

###############################################################################
# components/synthetic
###############################################################################

# libxml2-2.9.12
copy_both_bin "${BASE_DIR}/components/synthetic/libxml2-2.9.12/backdoored/libxml2_xml_reader_for_file_fuzzer" "components/synthetic/libxml2/backdoored"
copy_both_bin "${BASE_DIR}/components/synthetic/libxml2-2.9.12/safe/libxml2_xml_reader_for_file_fuzzer"       "components/synthetic/libxml2/safe"
copy_both_bin "${BASE_DIR}/components/synthetic/libxml2-2.9.12/prev-safe/libxml2_xml_reader_for_file_fuzzer"  "components/synthetic/libxml2/prev-safe"

# libsndfile-1.2.2
copy_both_bin "${BASE_DIR}/components/synthetic/libsndfile-1.2.2/prev-safe/ossfuzz/sndfile_fuzzer"  "components/synthetic/libsndfile/prev-safe"
copy_both_bin "${BASE_DIR}/components/synthetic/libsndfile-1.2.2/safe/ossfuzz/sndfile_fuzzer"       "components/synthetic/libsndfile/safe"
copy_both_bin "${BASE_DIR}/components/synthetic/libsndfile-1.2.2/backdoored/ossfuzz/sndfile_fuzzer" "components/synthetic/libsndfile/backdoored"

# libpng-1.6.43
copy_both_bin "${BASE_DIR}/components/synthetic/libpng-1.6.43/safe/libpng_read_fuzzer"       "components/synthetic/libpng/safe"
copy_both_bin "${BASE_DIR}/components/synthetic/libpng-1.6.43/backdoored/libpng_read_fuzzer" "components/synthetic/libpng/backdoored"
copy_both_bin "${BASE_DIR}/components/synthetic/libpng-1.6.43/prev-safe/libpng_read_fuzzer"  "components/synthetic/libpng/prev-safe"

# lua-5.4.7
copy_both_bin "${BASE_DIR}/components/synthetic/lua-5.4.7/prev-safe/src/lua"  "components/synthetic/lua/prev-safe"
copy_both_bin "${BASE_DIR}/components/synthetic/lua-5.4.7/safe/src/lua"       "components/synthetic/lua/safe"
copy_both_bin "${BASE_DIR}/components/synthetic/lua-5.4.7/backdoored/src/lua" "components/synthetic/lua/backdoored"

# php-8.0.20
copy_both_bin "${BASE_DIR}/components/synthetic/php-8.0.20/safe/sapi/fuzzer/php-fuzz-unserialize"       "components/synthetic/php/safe"
copy_both_bin "${BASE_DIR}/components/synthetic/php-8.0.20/prev-safe/sapi/fuzzer/php-fuzz-unserialize"  "components/synthetic/php/prev-safe"
copy_both_bin "${BASE_DIR}/components/synthetic/php-8.0.20/backdoored/sapi/fuzzer/php-fuzz-unserialize" "components/synthetic/php/backdoored"

# poppler-21.07.0
copy_both_bin "${BASE_DIR}/components/synthetic/poppler-21.07.0/backdoored/build/pdf_fuzzer" "components/synthetic/poppler/backdoored"
copy_both_bin "${BASE_DIR}/components/synthetic/poppler-21.07.0/safe/build/pdf_fuzzer"       "components/synthetic/poppler/safe"
copy_both_bin "${BASE_DIR}/components/synthetic/poppler-21.07.0/prev-safe/build/pdf_fuzzer"  "components/synthetic/poppler/prev-safe"

# sqlite3-3.37.0
copy_both_bin "${BASE_DIR}/components/synthetic/sqlite3-3.37.0/backdoored/sqlite3" "components/synthetic/sqlite3-3.37.0/backdoored"
copy_both_bin "${BASE_DIR}/components/synthetic/sqlite3-3.37.0/safe/sqlite3"       "components/synthetic/sqlite3-3.37.0/safe"
copy_both_bin "${BASE_DIR}/components/synthetic/sqlite3-3.37.0/prev-safe/sqlite3"  "components/synthetic/sqlite3-3.37.0/prev-safe"

# sudo-1.9.15p5
copy_both_bin "${BASE_DIR}/components/synthetic/sudo-1.9.15p5/backdoored/build/libexec/sudo/sudoers.so" "components/synthetic/sudo/backdoored"
copy_both_bin "${BASE_DIR}/components/synthetic/sudo-1.9.15p5/safe/build/libexec/sudo/sudoers.so"       "components/synthetic/sudo/safe"
copy_both_bin "${BASE_DIR}/components/synthetic/sudo-1.9.15p5/prev-safe/build/libexec/sudo/sudoers.so"  "components/synthetic/sudo/prev-safe"

# libtiff-4.3.0
copy_both_bin "${BASE_DIR}/components/synthetic/libtiff-4.3.0/backdoored/tiff_read_rgba_fuzzer" "components/synthetic/libtiff-4.3.0/backdoored"
copy_both_bin "${BASE_DIR}/components/synthetic/libtiff-4.3.0/safe/tiff_read_rgba_fuzzer"       "components/synthetic/libtiff-4.3.0/safe"
copy_both_bin "${BASE_DIR}/components/synthetic/libtiff-4.3.0/prev-safe/tiff_read_rgba_fuzzer"  "components/synthetic/libtiff-4.3.0/prev-safe"

# openssl-3.0.0
copy_both_bin "${BASE_DIR}/components/synthetic/openssl-3.0.0/backdoored/apps/openssl" "components/synthetic/openssl-3.0.0/backdoored"
copy_both_bin "${BASE_DIR}/components/synthetic/openssl-3.0.0/safe/apps/openssl"       "components/synthetic/openssl-3.0.0/safe"
copy_both_bin "${BASE_DIR}/components/synthetic/openssl-3.0.0/prev-safe/apps/openssl"  "components/synthetic/openssl-3.0.0/prev-safe"

# dropbear2024-86
copy_both_bin "${BASE_DIR}/components/synthetic/dropbear2024-86/backdoored/dropbear" "components/synthetic/dropbear2024-86/backdoored"
copy_both_bin "${BASE_DIR}/components/synthetic/dropbear2024-86/safe/dropbear"       "components/synthetic/dropbear2024-86/safe"
copy_both_bin "${BASE_DIR}/components/synthetic/dropbear2024-86/prev-safe/dropbear"  "components/synthetic/dropbear2024-86/prev-safe"

###############################################################################
# components/authentic
###############################################################################

# proftpd-1.3.3c
copy_both_bin "${BASE_DIR}/components/authentic/proftpd-1.3.3c/safe/proftpd"       "components/authentic/proftpd/safe"
copy_both_bin "${BASE_DIR}/components/authentic/proftpd-1.3.3c/backdoored/proftpd" "components/authentic/proftpd/backdoored"
copy_both_bin "${BASE_DIR}/components/authentic/proftpd-1.3.3c/prev-safe/proftpd"  "components/authentic/proftpd/prev-safe"

# php-8.1.0-dev
copy_both_bin "${BASE_DIR}/components/authentic/php-8.1.0-dev/backdoored/sapi/cli/php" "components/authentic/php/backdoored"
copy_both_bin "${BASE_DIR}/components/authentic/php-8.1.0-dev/safe/sapi/cli/php"       "components/authentic/php/safe"
copy_both_bin "${BASE_DIR}/components/authentic/php-8.1.0-dev/prev-safe/sapi/cli/php"  "components/authentic/php/prev-safe"

# vsftpd-2.3.4
copy_both_bin "${BASE_DIR}/components/authentic/vsftpd-2.3.4/backdoored/vsftpd" "components/authentic/vsftpd/backdoored"
copy_both_bin "${BASE_DIR}/components/authentic/vsftpd-2.3.4/safe/vsftpd"       "components/authentic/vsftpd/safe"
copy_both_bin "${BASE_DIR}/components/authentic/vsftpd-2.3.4/prev-safe/vsftpd"  "components/authentic/vsftpd/prev-safe"

echo "All copies completed."
echo "Normal outputs:   ${OUT_NORMAL}"
echo "Stripped outputs: ${OUT_STRIPPED}"
