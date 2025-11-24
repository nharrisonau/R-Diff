#!/usr/bin/env bash
set -euo pipefail

# Base paths (override with env vars if needed)
BASE_DIR="${BASE_DIR:-$HOME/rosarum}"
OUT_BASE="${OUT_BASE:-$BASE_DIR/outputs}"

copy_bin() {
    local src="$1"      # full path to built binary
    local rel_out="$2"  # relative output dir under $OUT_BASE

    local dst_dir="${OUT_BASE}/${rel_out}"

    mkdir -p "${dst_dir}"
    echo "Copying ${src} -> ${dst_dir}/"
    cp "${src}" "${dst_dir}/"
}

###############################################################################
# synthetic
###############################################################################

# libxml2-2.9.12
copy_bin "${BASE_DIR}/synthetic/libxml2-2.9.12/backdoored/libxml2_xml_reader_for_file_fuzzer" "synethetic/libxml2/backdoored"
copy_bin "${BASE_DIR}/synthetic/libxml2-2.9.12/safe/libxml2_xml_reader_for_file_fuzzer"       "synethetic/libxml2/safe"
copy_bin "${BASE_DIR}/synthetic/libxml2-2.9.12/prev-safe/libxml2_xml_reader_for_file_fuzzer"  "synethetic/libxml2/prev-safe"

# libsndfile-1.2.2
copy_bin "${BASE_DIR}/synthetic/libsndfile-1.2.2/prev-safe/ossfuzz/sndfile_fuzzer" "synethetic/libsndfile/prev-safe"
copy_bin "${BASE_DIR}/synthetic/libsndfile-1.2.2/safe/ossfuzz/sndfile_fuzzer"      "synethetic/libsndfile/safe"
copy_bin "${BASE_DIR}/synthetic/libsndfile-1.2.2/backdoored/ossfuzz/sndfile_fuzzer" "synethetic/libsndfile/backdoored"

# libpng-1.6.43
copy_bin "${BASE_DIR}/synthetic/libpng-1.6.43/safe/libpng_read_fuzzer"      "synethetic/libpng/safe"
copy_bin "${BASE_DIR}/synthetic/libpng-1.6.43/backdoored/libpng_read_fuzzer" "synethetic/libpng/backdoored"
copy_bin "${BASE_DIR}/synthetic/libpng-1.6.43/prev-safe/libpng_read_fuzzer" "synethetic/libpng/prev-safe"

# lua-5.4.7
copy_bin "${BASE_DIR}/synthetic/lua-5.4.7/prev-safe/src/lua"   "synethetic/lua/prev-safe"
copy_bin "${BASE_DIR}/synthetic/lua-5.4.7/safe/src/lua"        "synethetic/lua/safe"
copy_bin "${BASE_DIR}/synthetic/lua-5.4.7/backdoored/src/lua"  "synethetic/lua/backdoored"

# php-8.0.20
copy_bin "${BASE_DIR}/synthetic/php-8.0.20/safe/sapi/fuzzer/php-fuzz-unserialize"      "synethetic/php/safe"
copy_bin "${BASE_DIR}/synthetic/php-8.0.20/prev-safe/sapi/fuzzer/php-fuzz-unserialize" "synethetic/php/prev-safe"
copy_bin "${BASE_DIR}/synthetic/php-8.0.20/backdoored/sapi/fuzzer/php-fuzz-unserialize" "synethetic/php/backdoored"

# poppler-21.07.0
copy_bin "${BASE_DIR}/synthetic/poppler-21.07.0/backdoored/build/pdf_fuzzer" "synethetic/poppler/backdoored"
copy_bin "${BASE_DIR}/synthetic/poppler-21.07.0/safe/build/pdf_fuzzer"       "synethetic/poppler/safe"
copy_bin "${BASE_DIR}/synthetic/poppler-21.07.0/prev-safe/build/pdf_fuzzer"  "synethetic/poppler/prev-safe"

# sqlite3-3.37.0
copy_bin "${BASE_DIR}/synthetic/sqlite3-3.37.0/backdoored/sqlite3" "synethetic/sqlite3-3.37.0/backdoored"
copy_bin "${BASE_DIR}/synthetic/sqlite3-3.37.0/safe/sqlite3"       "synethetic/sqlite3-3.37.0/safe"
copy_bin "${BASE_DIR}/synthetic/sqlite3-3.37.0/prev-safe/sqlite3"  "synethetic/sqlite3-3.37.0/prev-safe"

# sudo-1.9.15p5
copy_bin "${BASE_DIR}/synthetic/sudo-1.9.15p5/backdoored/build/libexec/sudo/sudoers.so" "synethetic/sudo/backdoored"
copy_bin "${BASE_DIR}/synthetic/sudo-1.9.15p5/safe/build/libexec/sudo/sudoers.so"       "synethetic/sudo/safe"
copy_bin "${BASE_DIR}/synthetic/sudo-1.9.15p5/prev-safe/build/libexec/sudo/sudoers.so"  "synethetic/sudo/prev-safe"

# libtiff-4.3.0
copy_bin "${BASE_DIR}/synthetic/libtiff-4.3.0/backdoored/tiff_read_rgba_fuzzer" "synethetic/libtiff-4.3.0/backdoored"
copy_bin "${BASE_DIR}/synthetic/libtiff-4.3.0/safe/tiff_read_rgba_fuzzer"       "synethetic/libtiff-4.3.0/safe"
copy_bin "${BASE_DIR}/synthetic/libtiff-4.3.0/prev-safe/tiff_read_rgba_fuzzer"  "synethetic/libtiff-4.3.0/prev-safe"

# openssl-3.0.0
copy_bin "${BASE_DIR}/synthetic/openssl-3.0.0/backdoored/apps/openssl" "synethetic/openssl-3.0.0/backdoored"
copy_bin "${BASE_DIR}/synthetic/openssl-3.0.0/safe/apps/openssl"       "synethetic/openssl-3.0.0/safe"
copy_bin "${BASE_DIR}/synthetic/openssl-3.0.0/prev-safe/apps/openssl"  "synethetic/openssl-3.0.0/prev-safe"

###############################################################################
# authentic
###############################################################################

# proftpd-1.3.3c
copy_bin "${BASE_DIR}/authentic/proftpd-1.3.3c/safe/proftpd"      "authentic/proftpd/safe"
copy_bin "${BASE_DIR}/authentic/proftpd-1.3.3c/backdoored/proftpd" "authentic/proftpd/backdoored"
copy_bin "${BASE_DIR}/authentic/proftpd-1.3.3c/prev-safe/proftpd" "authentic/proftpd/prev-safe"

# php-8.1.0-dev
copy_bin "${BASE_DIR}/authentic/php-8.1.0-dev/backdoored/sapi/cli/php" "authentic/php/backdoored"
copy_bin "${BASE_DIR}/authentic/php-8.1.0-dev/safe/sapi/cli/php"       "authentic/php/safe"
copy_bin "${BASE_DIR}/authentic/php-8.1.0-dev/prev-safe/sapi/cli/php"  "authentic/php/prev-safe"

# vsftpd-2.3.4
copy_bin "${BASE_DIR}/authentic/vsftpd-2.3.4/backdoored/vsftpd" "authentic/vsftpd/backdoored"
copy_bin "${BASE_DIR}/authentic/vsftpd-2.3.4/safe/vsftpd"       "authentic/vsftpd/safe"
copy_bin "${BASE_DIR}/authentic/vsftpd-2.3.4/prev-safe/vsftpd"  "authentic/vsftpd/prev-safe"

echo "All copies completed."
