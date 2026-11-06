#!/bin/sh
# Reinstalls the system packages the headless GUI tests need.
# The runtime container is recycled periodically and drops them; the project
# files themselves live on persistent storage, so only apt state is lost.
apt-get update -qq
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    xvfb xauth libegl1 libgl1 libxcb-cursor0 libxcb-xinerama0 libxcb-icccm4 \
    libxcb-image0 libxcb-keysyms1 libxcb-randr0 libxcb-render-util0 \
    libxcb-shape0 libxcb-xkb1 libxkbcommon-x11-0 \
    fonts-noto-core fonts-dejavu-core
fc-cache -f >/dev/null 2>&1
echo "test environment ready: $(command -v xvfb-run)"
