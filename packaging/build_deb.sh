#!/usr/bin/env bash
set -euo pipefail

# packaging/build_deb.sh
# Build a .deb package for Task Tracker
# Usage:
#   ./packaging/build_deb.sh [version]
# Example:
#   ./packaging/build_deb.sh 0.1.0

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PKG_NAME=task-tracker
VERSION=${1:-0.1.0}
# Produce filename without architecture suffix (e.g. task-tracker_0.1.0.deb)
OUTFILE="${PKG_NAME}_${VERSION}.deb"

BUILD_DIR="${REPO_ROOT}/packaging/build_${PKG_NAME}_${VERSION}"

echo "Building ${OUTFILE} in ${BUILD_DIR}"

rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR/DEBIAN"

# Create control file
cat > "$BUILD_DIR/DEBIAN/control" <<EOF
Package: ${PKG_NAME}
Version: ${VERSION}
Section: utils
Priority: optional
Architecture: ${ARCH}
Depends: python3, python3-pyqt5
Maintainer: Your Name <you@example.com>
Description: A small task tracker app built with PyQt5
 A simple to-do application.
EOF

chmod 644 "$BUILD_DIR/DEBIAN/control"

# Copy application files to /usr/share/<pkg>
mkdir -p "$BUILD_DIR/usr/share/$PKG_NAME"
cp -r "$REPO_ROOT/src/"* "$BUILD_DIR/usr/share/$PKG_NAME/"

# Create wrapper in /usr/bin
mkdir -p "$BUILD_DIR/usr/bin"
cat > "$BUILD_DIR/usr/bin/$PKG_NAME" <<'EOF'
#!/bin/sh
exec python3 /usr/share/task-tracker/task-tracker_app.py "$@"
EOF
chmod 0755 "$BUILD_DIR/usr/bin/$PKG_NAME"

# Install icon (if present)
ICON_SRC="$REPO_ROOT/resources/th-1828655096.png"
if [ -f "$ICON_SRC" ]; then
  mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"
  cp "$ICON_SRC" "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/${PKG_NAME}.png"
fi

# Desktop entry
mkdir -p "$BUILD_DIR/usr/share/applications"
cat > "$BUILD_DIR/usr/share/applications/$PKG_NAME.desktop" <<EOF
[Desktop Entry]
Name=Task Tracker
Comment=A beautiful little to-do app
Exec=/usr/bin/$PKG_NAME
Icon=$PKG_NAME
Terminal=false
Type=Application
Categories=Utility;Productivity;
EOF

chmod 644 "$BUILD_DIR/usr/share/applications/$PKG_NAME.desktop"

echo "Building deb package (fakeroot)..."
if ! command -v fakeroot >/dev/null 2>&1; then
  echo "fakeroot not found; please install it (sudo apt install fakeroot)" >&2
  exit 1
fi

pushd "$REPO_ROOT/packaging" >/dev/null
fakeroot dpkg-deb --build "build_${PKG_NAME}_${VERSION}" "$REPO_ROOT/$OUTFILE"
popd >/dev/null

echo "Built: $OUTFILE"
echo "You can install it with: sudo dpkg -i $OUTFILE && sudo apt-get install -f"
