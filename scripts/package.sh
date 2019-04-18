#!/usr/bin/env bash

set -eu


BASEDIR=$(dirname $0)/..
TARGETDIR=${TARGETDIR:-${HOME}/packages}
PKGNAME=bush-rabbit


if [ ! -d "${TARGETDIR}" ]; then
    mkdir -p "$TARGETDIR"
fi

tar --transform "s/^./${PKGNAME}/" -czf "${TARGETDIR}/${PKGNAME}.tgz" -C "$BASEDIR" --exclude .git --exclude venv .

echo "tarball has bee created at: ${TARGETDIR}/${PKGNAME}.tgz"
