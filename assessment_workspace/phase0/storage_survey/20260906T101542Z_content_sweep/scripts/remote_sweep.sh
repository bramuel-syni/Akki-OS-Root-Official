#!/usr/bin/env bash
# remote_sweep.sh — content-level file sweep, shape-only metadata output.
# Runs on the remote host. Emits sections to stdout with clear === headers.
# Guardrails:
#   - Skips system dirs (/proc /sys /usr /lib /boot /snap)
#   - Skips secrets (~/.ssh ~/.aws ~/.config, *.pem, *key*, *secret*) EXCEPT for a top-level count/size summary
#   - sha256 gated at ≤ 100 MiB
#   - Does not read, echo, or emit file contents; only names + shape
set -o pipefail

HOSTLABEL=$(hostname)
STAMP=$(date -u +%Y%m%dT%H%M%SZ)

# --- Roots to sweep. Skip system dirs entirely. ---
ROOTS=()
for r in /home /data /mnt /srv /opt /var/www; do
  [ -d "$r" ] && ROOTS+=("$r")
done

# --- Secret-skip predicates ---
# find prune expression parts:
PRUNE_EXPR=( \
  -path "*/.ssh"     -o \
  -path "*/.aws"     -o \
  -path "*/.config"  -o \
  -path "*/lost+found" \
)

# Secret-name predicate (for count/size-only reporting)
SECRET_NAME_EXPR=( \
  -iname "*.pem"     -o \
  -iname "*key*"     -o \
  -iname "*secret*"  -o \
  -iname "id_rsa*"   -o \
  -iname "id_ed25519*" -o \
  -iname "*.pfx"     -o \
  -iname "*.p12" \
)

echo "==BEGIN CONTENT_SWEEP host=$HOSTLABEL ts=$STAMP=="
echo "roots=${ROOTS[*]}"

# ================================================================
# SECTION A: top-level du -sh per root (single depth)
# ================================================================
echo
echo "===A du-sh per root ==="
for r in "${ROOTS[@]}"; do
  # -x = one filesystem; --max-depth=1 for top-of-root
  du -shx --max-depth=1 "$r" 2>/dev/null | sed "s|\t|\t|"
done

# ================================================================
# SECTION B: full enumeration (path\tsize\tmtime\tuid\tgid\tmode)
# One line per FILE. Prune excluded dirs. Secret files are omitted
# here and counted separately in Section C.
# ================================================================
echo
echo "===B enumeration (tab: path SIZE MTIME UID GID MODE) ==="
for r in "${ROOTS[@]}"; do
  find "$r" -xdev \
    \( "${PRUNE_EXPR[@]}" \) -prune -o \
    -type f \
    ! \( "${SECRET_NAME_EXPR[@]}" \) \
    -printf '%p\t%s\t%T@\t%U\t%G\t%m\n' 2>/dev/null
done

# ================================================================
# SECTION C: secret-file summary (count + total size, no hashes, no listings)
# ================================================================
echo
echo "===C secret-file summary (count+total_size only) ==="
for r in "${ROOTS[@]}"; do
  find "$r" -xdev \
    \( -path "*/.ssh" -o -path "*/.aws" -o -path "*/.config" \) -prune -o \
    -type f \
    \( "${SECRET_NAME_EXPR[@]}" \) \
    -printf '%s\n' 2>/dev/null | \
    awk -v ROOT="$r" 'BEGIN{n=0; b=0} {n++; b+=$1} END{printf "%s\tsecret_files=%d\ttotal_bytes=%d\n", ROOT, n, b}'
done
# Also count the pruned trees themselves for visibility
for r in "${ROOTS[@]}"; do
  for p in .ssh .aws .config; do
    if [ -n "$(find "$r" -xdev -type d -name "$p" -print -quit 2>/dev/null)" ]; then
      # If the pruned dir exists somewhere under r, report its total size
      find "$r" -xdev -type d -name "$p" 2>/dev/null | while read d; do
        sz=$(du -sb "$d" 2>/dev/null | awk '{print $1}')
        nf=$(find "$d" -xdev -type f 2>/dev/null | wc -l)
        echo -e "PRUNE_DIR\t$d\tfiles=$nf\tbytes=$sz"
      done
    fi
  done
done

# ================================================================
# SECTION D: owner/group census (one line)
# ================================================================
echo
echo "===D owner/group census ==="
for r in "${ROOTS[@]}"; do
  find "$r" -xdev \
    \( "${PRUNE_EXPR[@]}" \) -prune -o \
    -type f -printf '%U:%G\n' 2>/dev/null
done | sort | uniq -c | sort -nr | head -20

# ================================================================
# SECTION E: mtime distribution — buckets per root
#   <1d, <7d, <30d, <365d, >=365d, min, max
# ================================================================
echo
echo "===E mtime buckets per root ==="
NOW=$(date -u +%s)
for r in "${ROOTS[@]}"; do
  find "$r" -xdev \
    \( "${PRUNE_EXPR[@]}" \) -prune -o \
    -type f -printf '%T@\n' 2>/dev/null | \
    awk -v NOW="$NOW" -v ROOT="$r" '
      BEGIN {b1=b2=b3=b4=b5=0; mn=""; mx=""}
      {
        t=$1+0; age=NOW-t
        if (mn=="" || t<mn) mn=t
        if (mx=="" || t>mx) mx=t
        if (age<86400)         b1++
        else if (age<604800)   b2++
        else if (age<2592000)  b3++
        else if (age<31536000) b4++
        else                   b5++
      }
      END {
        printf "%s\tlt1d=%d\tlt7d=%d\tlt30d=%d\tlt365d=%d\tge365d=%d\tmin_epoch=%s\tmax_epoch=%s\n",
               ROOT, b1, b2, b3, b4, b5, mn, mx
      }'
done

echo
echo "==END CONTENT_SWEEP host=$HOSTLABEL ts=$(date -u +%Y%m%dT%H%M%SZ)=="
