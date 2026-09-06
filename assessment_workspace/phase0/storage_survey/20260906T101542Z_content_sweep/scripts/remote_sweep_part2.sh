#!/usr/bin/env bash
# remote_sweep_part2.sh — du_depth1, tree_depth2, magic classification, sha256 (≤100 MiB), audio ffprobe.
# Emits sections F..K in a single stream.
set -o pipefail

HOSTLABEL=$(hostname)
STAMP=$(date -u +%Y%m%dT%H%M%SZ)

ROOTS=()
for r in /home /data /mnt /srv /opt /var/www; do
  [ -d "$r" ] && ROOTS+=("$r")
done

PRUNE_EXPR=( \
  -path "*/.ssh"     -o \
  -path "*/.aws"     -o \
  -path "*/.config"  -o \
  -path "*/lost+found" \
)
SECRET_NAME_EXPR=( \
  -iname "*.pem" -o -iname "*key*" -o -iname "*secret*" -o \
  -iname "id_rsa*" -o -iname "id_ed25519*" -o -iname "*.pfx" -o -iname "*.p12" \
)

echo "==BEGIN CONTENT_SWEEP_P2 host=$HOSTLABEL ts=$STAMP=="

# ================================================================
# SECTION F: du depth 1 per root (fixed — no --max-depth+-s conflict)
# ================================================================
echo
echo "===F du depth1 per root (human) ==="
for r in "${ROOTS[@]}"; do
  echo "-- $r --"
  du -hx -d 1 "$r" 2>/dev/null | sort -h
done

# ================================================================
# SECTION G: directory tree depth 2 per root
# ================================================================
echo
echo "===G tree depth2 per root ==="
for r in "${ROOTS[@]}"; do
  echo "-- $r --"
  # -maxdepth 2 -type d, show dirs and their child dirs; skip pruned patterns
  find "$r" -xdev -maxdepth 2 \
    \( "${PRUNE_EXPR[@]}" \) -prune -o \
    -type d -print 2>/dev/null | head -200
done

# ================================================================
# SECTION H: magic-byte classification. All non-secret, non-pruned files.
# We use `file --mime-type` to keep output compact and greppable.
# ================================================================
echo
echo "===H magic-byte classification (path\ttype) ==="
for r in "${ROOTS[@]}"; do
  find "$r" -xdev \
    \( "${PRUNE_EXPR[@]}" \) -prune -o \
    -type f \
    ! \( "${SECRET_NAME_EXPR[@]}" \) \
    -print0 2>/dev/null | \
    xargs -0 -r -n 500 file --mime-type --print0 2>/dev/null | \
    tr '\0' '\n'
done

# ================================================================
# SECTION I: mime-type census (aggregated) — high-level headline
# ================================================================
echo
echo "===I mime-type census (count | mime | example_path first-seen) ==="
for r in "${ROOTS[@]}"; do
  find "$r" -xdev \
    \( "${PRUNE_EXPR[@]}" \) -prune -o \
    -type f \
    ! \( "${SECRET_NAME_EXPR[@]}" \) \
    -print0 2>/dev/null | \
    xargs -0 -r -n 500 file --mime-type 2>/dev/null
done | awk -F': ' '{ mime=$NF; # some paths could contain ": "
                     path=""; for (i=1; i<NF; i++) path=path (i>1?": ":"") $i;
                     if (!(mime in ex)) ex[mime]=path;
                     c[mime]++ }
                   END{ for (m in c) print c[m]"\t"m"\t"ex[m] }' | sort -nr | head -60

# ================================================================
# SECTION J: sha256 (≤ 100 MiB), non-secret, non-pruned
# ================================================================
echo
echo "===J sha256 hashes (≤100 MiB) ==="
LIMIT=$((100*1024*1024))
for r in "${ROOTS[@]}"; do
  find "$r" -xdev \
    \( "${PRUNE_EXPR[@]}" \) -prune -o \
    -type f \
    ! \( "${SECRET_NAME_EXPR[@]}" \) \
    -size -${LIMIT}c \
    -print0 2>/dev/null | \
    xargs -0 -r -n 200 sha256sum 2>/dev/null
done

# ================================================================
# SECTION K: audio candidates — any file with magic containing "audio" or "video"
#            → ffprobe -show_streams. We deliberately probe video too, since
#            some containers (mp4, mkv) carry audio streams.
# ================================================================
echo
echo "===K ffprobe on audio/video magic-byte candidates ==="
if ! command -v ffprobe >/dev/null; then
  echo "SKIP: ffprobe not installed on host"
else
  for r in "${ROOTS[@]}"; do
    find "$r" -xdev \
      \( "${PRUNE_EXPR[@]}" \) -prune -o \
      -type f \
      ! \( "${SECRET_NAME_EXPR[@]}" \) \
      -print0 2>/dev/null | \
      xargs -0 -r -n 200 file --mime-type 2>/dev/null | \
      awk -F': ' '{mime=$NF; if(mime ~ /^(audio|video)\//){ path=""; for(i=1;i<NF;i++) path=path (i>1?": ":"") $i; print path"\t"mime }}' | \
      while IFS=$'\t' read -r p mime; do
        echo "--- ffprobe $p ($mime) ---"
        ffprobe -v error -show_entries stream=index,codec_type,codec_name,sample_rate,channels,duration,bit_rate -show_entries format=duration,format_name,size -of default=noprint_wrappers=1 "$p" 2>&1 | sed 's/^/  /'
      done
  done
fi

echo
echo "==END CONTENT_SWEEP_P2 host=$HOSTLABEL ts=$(date -u +%Y%m%dT%H%M%SZ)=="
