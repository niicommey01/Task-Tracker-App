Building a .deb for Task Tracker
================================

This folder contains a small script to build a Debian package for the app.

Prerequisites
- dpkg-deb (part of Debian packaging tools)
- fakeroot (to build without root)
- python3 and python3-pyqt5 installed on target system

Quick build
-----------
From the repository root:

```bash
chmod +x packaging/build_deb.sh
packaging/build_deb.sh 0.1.0
```

This will produce `task-tracker_0.1.0.deb` in the repository root.

Install the package:

```bash
sudo dpkg -i task-tracker_0.1.0.deb
sudo apt-get install -f
```

Notes
-----
- The script copies `src/` into `/usr/share/task-tracker` inside the package, creates a `/usr/bin/task-tracker` wrapper, installs the icon (if present) to the hicolor icon path, and adds a desktop entry under `/usr/share/applications`.
- Edit dependencies in `packaging/build_deb.sh` (control file) if you need different package names or additional runtime deps.
- Consider adding a GitHub Actions workflow to build and publish `.deb` assets automatically on tags.

If you want, I can add the GitHub Actions workflow too.  
