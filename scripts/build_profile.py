#!/usr/bin/env python3
"""Build the GitHub profile's self-contained terminal SVG assets.

Usage: python scripts/build_profile.py path/to/ascii-portrait.png
Requires Pillow. The source portrait is used only as an embedded visual asset.
"""
from __future__ import annotations

import argparse
import base64
import html
import io
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
BLUE, GREEN, ORANGE, PURPLE = "#79c0ff", "#7ee787", "#ffa657", "#d2a8ff"
TEXT, MUTED, BORDER, BG = "#e6edf3", "#8b949e", "#30363d", "#0d1117"


def text(x, y, value, size=16, color=TEXT, weight=400):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" '
            f'font-weight="{weight}">{html.escape(value)}</text>')


def line(x1, y1, x2, y2, color=BORDER):
    return f'<path d="M{x1} {y1}H{x2}" stroke="{color}"/>' if y1 == y2 else (
        f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{color}"/>')


def shell(width, height, label):
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" '
        'aria-labelledby="title desc">',
        '<title id="title">Toufik Bentaleb — Control Systems Engineer</title>',
        '<desc id="desc">Terminal profile with an ASCII-style portrait. Senior Control Systems '
        'Engineer, PhD, working on predictive control, state estimation, robotics, embedded systems '
        'and DZARYON.</desc>',
        '<defs><clipPath id="window"><rect x="1" y="1" width="' + str(width-2) + '" height="' + str(height-2) + '" rx="18"/></clipPath></defs>',
        f'<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="18" fill="{BG}" stroke="{BORDER}" stroke-width="2"/>',
        f'<path d="M1 18Q1 1 18 1H{width-18}Q{width-1} 1 {width-1} 18V52H1Z" fill="#161b22"/>',
        '<circle cx="28" cy="27" r="6" fill="#ff5f57"/>',
        '<circle cx="49" cy="27" r="6" fill="#febc2e"/>',
        '<circle cx="70" cy="27" r="6" fill="#28c840"/>',
        '<g font-family="DejaVu Sans Mono, Consolas, monospace">',
        text(102, 32, label, 13, MUTED),
    ]


def portrait_uri(path):
    # Web asset encoding only: preserve the generated artwork and its composition.
    image = Image.open(path).convert("RGB")
    image.thumbnail((540, 720), Image.Resampling.LANCZOS)
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=88, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buffer.getvalue()).decode("ascii")


def desktop(uri):
    s = shell(1040, 648, "bentaleb-toufik / README.md")
    s += [text(32, 91, "$ ./profile --engineer", 16, GREEN)]
    s += [f'<image x="27" y="115" width="326" height="435" preserveAspectRatio="xMidYMid meet" xlink:href="{uri}"/>']
    s += [text(70, 578, "MODEL. CONTROL. BUILD.", 14, MUTED)]
    s += [line(380, 84, 380, 585)]
    x = 412
    s += [text(x, 99, "toufik@control-lab", 17, GREEN),
          text(x, 145, "Toufik Bentaleb", 30, TEXT, 700),
          text(x, 174, "Senior Control Systems Engineer | PhD", 16, BLUE),
          line(x, 193, 1006, 193)]
    rows = [
        ("Degree", "PhD, Control Systems · Siena, 2015"),
        ("Experience", "15+ years · Research & engineering"),
        ("Domains", "Robotics · Automotive · Industrial"),
        ("Control", "MPC · Optimal · Adaptive · LPV"),
        ("Estimation", "Kalman · EKF/UKF · System ID"),
        ("Learning", "ML diagnostics · Neural control"),
        ("Code", "MATLAB/Simulink · C/C++ · Python"),
        ("Tools", "ROS 2 · MuJoCo · CasADi · YALMIP"),
        ("Embedded", "STM32 · STM8 · CAN/LIN"),
        ("Languages", "Arabic · French · English"),
    ]
    for i, (key, value) in enumerate(rows):
        y = 223 + 28*i
        s += [text(x, y, key + ":", 15, ORANGE), text(x+122, y, value, 15)]
    s += [line(x, 508, 1006, 508),
          text(x, 539, "Building", 15, PURPLE),
          text(x+122, 539, "DZARYON · AI & Intelligent Systems", 15),
          text(x, 568, "Web", 15, PURPLE),
          text(x+122, 568, "dzrobotics.org", 15, BLUE),
          line(32, 600, 1008, 600),
          text(32, 629, "$ from models to controllers that run on real systems", 15, GREEN),
          '<rect x="532" y="615" width="9" height="18" fill="#7ee787"/>',
          '</g></svg>']
    return "\n".join(s) + "\n"


def mobile(uri):
    s = shell(600, 1180, "bentaleb-toufik / README.md")
    s += [text(28, 89, "$ ./profile --engineer", 19, GREEN),
          f'<image x="150" y="109" width="300" height="400" preserveAspectRatio="xMidYMid meet" xlink:href="{uri}"/>',
          text(28, 554, "Toufik Bentaleb", 34, TEXT, 700),
          text(28, 588, "Senior Control Systems Engineer", 21, BLUE),
          text(28, 618, "PhD · 15+ years of experience", 19, MUTED),
          line(28, 643, 572, 643)]
    rows = [
        ("Control", "MPC · Optimal · Adaptive · LPV"),
        ("Estimation", "Kalman · EKF/UKF · System ID"),
        ("Learning", "ML diagnostics · Neural control"),
        ("Code", "MATLAB/Simulink · C/C++ · Python"),
        ("Tools", "ROS 2 · MuJoCo · CasADi · YALMIP"),
        ("Embedded", "STM32 · STM8 · CAN/LIN"),
        ("Languages", "Arabic · French · English"),
    ]
    for i, (key, value) in enumerate(rows):
        y = 680 + i*49
        s += [text(28, y, key, 16, ORANGE), text(28, y+24, value, 20)]
    s += [line(28, 1020, 572, 1020), text(28, 1054, "Building DZARYON", 22, PURPLE),
          text(28, 1088, "AI & Intelligent Systems", 20),
          text(28, 1122, "dzrobotics.org", 20, BLUE),
          text(28, 1160, "$ model · simulate · implement · validate", 17, GREEN),
          '</g></svg>']
    return "\n".join(s) + "\n"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("portrait", type=Path)
    args = parser.parse_args()
    ASSETS.mkdir(parents=True, exist_ok=True)
    uri = portrait_uri(args.portrait)
    (ASSETS / "profile-terminal.svg").write_text(desktop(uri), encoding="utf-8")
    (ASSETS / "profile-mobile.svg").write_text(mobile(uri), encoding="utf-8")
    for asset in ASSETS.glob("*.svg"):
        print(f"{asset.name}: {asset.stat().st_size:,} bytes")
