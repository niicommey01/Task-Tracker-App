#!/usr/bin/env bash
set -euo pipefail

# Simple installer for Task Tracker
# Usage:
#   ./install.sh            -> installs for the current user under ~/.local
#   ./install.sh --system   -> installs system-wide under /usr/local (requires sudo)
#   ./install.sh --prefix /custom/prefix

show_help() {
  cat <<EOF
Usage: $0 [--system] [--prefix DIR]

Installs Task Tracker as a desktop application.

Options:
  --system       Install system-wide under /usr/local (requires sudo)
  --prefix DIR   Install under DIR (overrides --system). Default: ~/.local
  -h, --help     Show this help message
EOF
}

PREFIX="$HOME/.local"
SYSTEM=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --system)
      SYSTEM=true
      PREFIX="/usr/local"
      shift
      ;;
    --prefix)
      PREFIX="$2"
      shift 2
      ;;
    -h|--help)
      show_help
      exit 0
      ;;
    *)
      echo "Unknown arg: $1"
      show_help
      exit 1
      ;;
  esac
done

if $SYSTEM; then
  SUDO=sudo
else
  SUDO=
fi

command -v python3 >/dev/null 2>&1 || { echo "python3 is required but not found" >&2; exit 1; }

APPNAME="task-tracker"
APPDIR="$PREFIX/share/$APPNAME"
BINDIR="$PREFIX/bin"
ICONDIR="$PREFIX/share/icons/hicolor/256x256/apps"
DESKTOPDIR="$PREFIX/share/applications"

echo "Installing Task Tracker to $PREFIX"

${SUDO} mkdir -p "$APPDIR" "$BINDIR" "$ICONDIR" "$DESKTOPDIR"

echo "Copying application files..."
${SUDO} cp -r "$(pwd)/src/"* "$APPDIR/"

if [ -f "$(pwd)/resources/th-1828655096.png" ]; then
  echo "Installing icon..."
  ${SUDO} cp "$(pwd)/resources/th-1828655096.png" "$ICONDIR/$APPNAME.png"
fi

echo "Creating wrapper in $BINDIR/$APPNAME"
${SUDO} tee "$BINDIR/$APPNAME" >/dev/null <<EOF
#!/bin/sh
exec python3 "$APPDIR/task-tracker_app.py" "\$@"
EOF

${SUDO} chmod +x "$BINDIR/$APPNAME"

echo "Installing desktop entry to $DESKTOPDIR/$APPNAME.desktop"
${SUDO} tee "$DESKTOPDIR/$APPNAME.desktop" >/dev/null <<EOF
[Desktop Entry]
Name=Task Tracker
Comment=A beautiful little to-do app
Exec=$BINDIR/$APPNAME
Icon=$APPNAME
Terminal=false
Type=Application
Categories=Utility;Productivity;
EOF

echo
echo "Installation complete."
echo "If you installed system-wide you may need to run 'sudo update-desktop-database' and/or restart your session to see the app in menus."
