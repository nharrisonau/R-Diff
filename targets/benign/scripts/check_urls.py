#!/usr/bin/env python3
import argparse
import csv
import subprocess
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

STATUS_OK = "ok"
STATUS_NOT_FOUND = "not_found"
STATUS_ERROR = "error"


def check_url(url: str, timeout: float) -> tuple[str, int | None, str]:
    """Return (status, http_status, note)."""
    if not url:
        return STATUS_ERROR, None, "empty url"

    # Try HEAD first
    try:
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return STATUS_OK, getattr(resp, "status", None), "head"
    except urllib.error.HTTPError as exc:
        code = exc.code
        if code in {404, 410}:
            return STATUS_NOT_FOUND, code, "head"
        # Some servers disallow HEAD
        if code in {405, 501}:
            pass
        else:
            return STATUS_ERROR, code, "head"
    except Exception as exc:
        return STATUS_ERROR, None, f"head: {exc}"

    # Fallback to GET with Range
    try:
        req = urllib.request.Request(url, method="GET")
        req.add_header("Range", "bytes=0-0")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return STATUS_OK, getattr(resp, "status", None), "get-range"
    except urllib.error.HTTPError as exc:
        code = exc.code
        if code in {404, 410}:
            return STATUS_NOT_FOUND, code, "get-range"
        return STATUS_ERROR, code, "get-range"
    except Exception as exc:
        return STATUS_ERROR, None, f"get-range: {exc}"


def load_manifest(path: Path) -> list[dict]:
    with path.open(newline="") as fh:
        reader = csv.DictReader(fh)
        return list(reader)


def write_manifest(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check manifest URLs and optionally filter out missing samples",
    )
    parser.add_argument(
        "--manifest",
        default="targets/benign/manifest.csv",
        help="Path to manifest.csv",
    )
    parser.add_argument(
        "--out-valid",
        default="targets/benign/manifest.valid.csv",
        help="Where to write valid rows",
    )
    parser.add_argument(
        "--out-invalid",
        default="targets/benign/manifest.invalid.csv",
        help="Where to write invalid rows",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=10.0,
        help="Timeout per request (seconds)",
    )
    parser.add_argument(
        "--max-workers",
        type=int,
        default=8,
        help="Parallel workers (default: 8; use 1 for serial logging)",
    )
    parser.add_argument(
        "--log-every",
        type=int,
        default=1,
        help="Print progress every N completed checks",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print a line for each URL as it completes",
    )
    parser.add_argument(
        "--sleep",
        type=float,
        default=0.0,
        help="Sleep between submissions (seconds)",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Replace manifest.csv with valid rows and regenerate pairs",
    )

    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    if not manifest_path.exists():
        print(f"Missing manifest: {manifest_path}")
        return 1

    rows = load_manifest(manifest_path)
    if not rows:
        print("Manifest is empty")
        return 1

    fieldnames = list(rows[0].keys())
    # extend with status columns
    if "url_status" not in fieldnames:
        fieldnames.extend(["url_status", "http_status", "url_note"])

    valid_rows = []
    invalid_rows = []
    total = len(rows)
    completed = 0
    ok_count = 0
    not_found_count = 0
    error_count = 0
    start = time.time()
    print(f"Checking {total} URLs with {args.max_workers} worker(s)...")

    if args.max_workers <= 1:
        for idx, row in enumerate(rows, start=1):
            url = (row.get("url") or "").strip()
            if args.verbose:
                print(f"[{idx}/{total}] checking {url}")
            status, http_status, note = check_url(url, args.timeout)
            row = dict(row)
            row["url_status"] = status
            row["http_status"] = "" if http_status is None else str(http_status)
            row["url_note"] = note

            if status == STATUS_OK:
                valid_rows.append(row)
                ok_count += 1
            else:
                invalid_rows.append(row)
                if status == STATUS_NOT_FOUND:
                    not_found_count += 1
                else:
                    error_count += 1

            completed += 1
            if args.verbose:
                print(f"[{completed}/{total}] {status} {url} ({note})")
            elif args.log_every and completed % args.log_every == 0:
                elapsed = time.time() - start
                rate = completed / elapsed if elapsed > 0 else 0.0
                remaining = total - completed
                eta = remaining / rate if rate > 0 else 0.0
                print(
                    f"[{completed}/{total}] ok={ok_count} not_found={not_found_count} "
                    f"error={error_count} rate={rate:.2f}/s eta={eta/60:.1f}m"
                )

            if args.sleep:
                time.sleep(args.sleep)
    else:
        with ThreadPoolExecutor(max_workers=args.max_workers) as executor:
            future_map = {}
            for idx, row in enumerate(rows):
                url = (row.get("url") or "").strip()
                future = executor.submit(check_url, url, args.timeout)
                future_map[future] = row
                if args.sleep:
                    time.sleep(args.sleep)

            for future in as_completed(future_map):
                row = future_map[future]
                status, http_status, note = future.result()
                row = dict(row)
                row["url_status"] = status
                row["http_status"] = "" if http_status is None else str(http_status)
                row["url_note"] = note

                if status == STATUS_OK:
                    valid_rows.append(row)
                    ok_count += 1
                else:
                    invalid_rows.append(row)
                    if status == STATUS_NOT_FOUND:
                        not_found_count += 1
                    else:
                        error_count += 1

                completed += 1
                if args.verbose:
                    print(
                        f"[{completed}/{total}] {status} {row.get('url', '')} ({row['url_note']})"
                    )
                elif args.log_every and completed % args.log_every == 0:
                    elapsed = time.time() - start
                    rate = completed / elapsed if elapsed > 0 else 0.0
                    remaining = total - completed
                    eta = remaining / rate if rate > 0 else 0.0
                    print(
                        f"[{completed}/{total}] ok={ok_count} not_found={not_found_count} "
                        f"error={error_count} rate={rate:.2f}/s eta={eta/60:.1f}m"
                    )

    write_manifest(Path(args.out_valid), valid_rows, fieldnames)
    write_manifest(Path(args.out_invalid), invalid_rows, fieldnames)

    print(f"Valid rows: {len(valid_rows)}")
    print(f"Invalid rows: {len(invalid_rows)}")

    if args.apply:
        write_manifest(manifest_path, valid_rows, fieldnames)
        # regenerate pairs
        build_pairs = Path("targets/benign/scripts/build_pairs.py")
        if build_pairs.exists():
            subprocess.run(
                [
                    sys.executable,
                    str(build_pairs),
                    "--manifest",
                    str(manifest_path),
                    "--out",
                    "targets/benign/pairs.csv",
                ],
                check=False,
            )
        print("Applied filtered manifest and regenerated pairs.csv")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
