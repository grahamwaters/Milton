#!/bin/bash
# This script creates the directory structure and files for the cyberpunk_hud_toolkit project.

# Root directory (package)
ROOT_DIR="cyberpunk_hud_toolkit"

# Create the root directory
mkdir -p "$ROOT_DIR"

# Create the README.md file
touch "$ROOT_DIR/README.md"

# ------------------------
# Create core directory structure and files
CORE_DIR="$ROOT_DIR/core"
mkdir -p "$CORE_DIR"
touch "$CORE_DIR/__init__.py"
touch "$CORE_DIR/engine.py"
touch "$CORE_DIR/scene.py"
touch "$CORE_DIR/effect.py"
touch "$CORE_DIR/transition.py"
touch "$CORE_DIR/utils.py"

# Create the hud subpackage inside core
HUD_DIR="$CORE_DIR/hud"
mkdir -p "$HUD_DIR"
touch "$HUD_DIR/__init__.py"
touch "$HUD_DIR/circular.py"
touch "$HUD_DIR/radar.py"
touch "$HUD_DIR/panel.py"
touch "$HUD_DIR/text.py"
touch "$HUD_DIR/shapes.py"
touch "$HUD_DIR/particles.py"

# ------------------------
# Create assets directory structure
ASSETS_DIR="$ROOT_DIR/assets"
mkdir -p "$ASSETS_DIR/fonts"
mkdir -p "$ASSETS_DIR/images"
mkdir -p "$ASSETS_DIR/sounds"

# ------------------------
# Create examples directory and files
EXAMPLES_DIR="$ROOT_DIR/examples"
mkdir -p "$EXAMPLES_DIR"
touch "$EXAMPLES_DIR/demo_dashboard.py"
touch "$EXAMPLES_DIR/demo_fireworks.py"
touch "$EXAMPLES_DIR/demo_matrix.py"
touch "$EXAMPLES_DIR/demo_hud_elements.py"
touch "$EXAMPLES_DIR/demo_glitch_transition.py"
touch "$EXAMPLES_DIR/demo_console.py"
touch "$EXAMPLES_DIR/demo_filesearch.py"

echo "Project structure for 'cyberpunk_hud_toolkit' created successfully."
