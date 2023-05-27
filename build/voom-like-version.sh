#!/usr/bin/env bash

set -e

[ -n "$DEBUG" ] && set -x

voom_version() {
  MACHINE="$(uname -s)"

  case "${MACHINE}" in
      Linux)
        target=$(readlink -f "$1")
        echo $(date -u --date="$(git log -1 --pretty=%ci -- "$target")" "+%Y%m%d_%H%M%S")-g$(git log -1 --pretty=%h -- "$target")$(test -z "$(git status --short -- "$target")" || echo _DIRTY)
        ;;
      Darwin)
        target="$1"
        last_commit_timestamp=$(git log -1 --pretty="%cd" --date="unix" -- "$target")
        echo $(date -r "${last_commit_timestamp}" -u "+%Y%m%d_%H%M%S")-g$(git log -1 --pretty=%h -- "$target")$(test -z "$(git status --short -- "$target")" || echo _DIRTY)
        ;;
      *) echo "could not detect your system flavor from '${MACHINE}' (uname -s)."; exit 1 ;;
  esac

}


usage() {
    echo >&2 "usage: $0 <PATH> [PATH...] # Optionally, set REPO_ROOT_VOOM instead of supplying <PATH>."
    exit 1
}


if [ -z "$*" ]; then
    if [ "$REPO_ROOT_VOOM" ]; then
        voom_version
    else
        usage
    fi
else
    if [ "$REPO_ROOT_VOOM" ]; then
        usage
    else
        voom_version "$@"
    fi
fi
