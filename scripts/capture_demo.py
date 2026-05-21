from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
from urllib.request import urlopen

import imageio.v2 as imageio
from PIL import Image
from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parent.parent


def wait_for_server(url: str, timeout: float = 30.0) -> None:
    start = time.time()
    while time.time() - start < timeout:
        try:
            with urlopen(url, timeout=2):
                return
        except Exception:
            time.sleep(0.35)
    raise TimeoutError(f"Server did not start in time: {url}")


def build_gif(
    frames: list[Path],
    output_path: Path,
    frame_duration: float,
    hold_start: int,
    hold_middle: int,
    hold_end: int,
) -> None:
    images = []
    for i, frame_path in enumerate(frames):
        frame = Image.open(frame_path).convert("RGB")
        frame = frame.resize((1200, 760), Image.Resampling.LANCZOS)
        if i == 0:
            repeats = hold_start
        elif i == len(frames) - 1:
            repeats = hold_end
        else:
            repeats = hold_middle
        for _ in range(repeats):
            images.append(frame.copy())

    output_path.parent.mkdir(parents=True, exist_ok=True)
    imageio.mimsave(output_path, images, duration=frame_duration, loop=0)


def export_screenshots(frames: list[Path], screenshots_dir: Path) -> None:
    screenshots_dir.mkdir(parents=True, exist_ok=True)
    for frame_path in frames:
        target = screenshots_dir / frame_path.name
        shutil.copy2(frame_path, target)


def run_capture(
    port: int,
    output_path: Path,
    frame_duration: float,
    hold_start: int,
    hold_middle: int,
    hold_end: int,
    screenshots_dir: Path | None,
) -> None:
    url = f"http://127.0.0.1:{port}"
    env = os.environ.copy()

    server = subprocess.Popen(
        [
            sys.executable,
            "-c",
            f"from app import app; app.run(debug=False, port={port})",
        ],
        cwd=str(ROOT),
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    frames_dir = ROOT / ".demo_frames"
    frames_dir.mkdir(exist_ok=True)
    for old in frames_dir.glob("*.png"):
        old.unlink()

    try:
        wait_for_server(url)

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1440, "height": 930})
            page.goto(url, wait_until="networkidle")
            page.wait_for_timeout(2200)
            page.screenshot(path=str(frames_dir / "01-overview.png"))

            page.locator("label", has_text="Experience").first.click()
            page.wait_for_timeout(1300)
            page.mouse.wheel(0, 380)
            page.wait_for_timeout(700)
            page.screenshot(path=str(frames_dir / "02-experience-awards.png"))

            page.locator("label", has_text="Projects").first.click()
            page.wait_for_timeout(1100)
            page.fill("#project-search", "FoodBridge")
            page.wait_for_timeout(900)
            page.screenshot(path=str(frames_dir / "03-projects-foodbridge.png"))

            page.locator("label", has_text="Skills").first.click()
            page.wait_for_timeout(1100)
            page.screenshot(path=str(frames_dir / "04-skills.png"))

            browser.close()

        frame_paths = [
            frames_dir / "01-overview.png",
            frames_dir / "02-experience-awards.png",
            frames_dir / "03-projects-foodbridge.png",
            frames_dir / "04-skills.png",
        ]
        build_gif(
            frame_paths,
            output_path,
            frame_duration=frame_duration,
            hold_start=hold_start,
            hold_middle=hold_middle,
            hold_end=hold_end,
        )
        if screenshots_dir is not None:
            export_screenshots(frame_paths, screenshots_dir)

    finally:
        server.terminate()
        try:
            server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server.kill()


def main() -> int:
    parser = argparse.ArgumentParser(description="Capture CV dashboard demo GIF.")
    parser.add_argument("--port", type=int, default=8070)
    parser.add_argument(
        "--output",
        default=str(ROOT / "docs" / "cv-dashboard-demo.gif"),
        help="Output GIF path",
    )
    parser.add_argument(
        "--duration",
        type=float,
        default=1.05,
        help="Seconds per GIF frame (higher is slower).",
    )
    parser.add_argument("--hold-start", type=int, default=7, help="Repeats for first frame.")
    parser.add_argument("--hold-middle", type=int, default=5, help="Repeats for middle frames.")
    parser.add_argument("--hold-end", type=int, default=10, help="Repeats for final frame.")
    parser.add_argument(
        "--screenshots-dir",
        default=str(ROOT / "docs" / "screenshots"),
        help="Directory to export PNG screenshots.",
    )
    parser.add_argument(
        "--skip-screenshots",
        action="store_true",
        help="Disable screenshot export.",
    )
    args = parser.parse_args()

    output = Path(args.output).resolve()
    shots_dir = None if args.skip_screenshots else Path(args.screenshots_dir).resolve()
    run_capture(
        port=args.port,
        output_path=output,
        frame_duration=args.duration,
        hold_start=args.hold_start,
        hold_middle=args.hold_middle,
        hold_end=args.hold_end,
        screenshots_dir=shots_dir,
    )
    print(f"Demo GIF written to {output}")
    if shots_dir is not None:
        print(f"Screenshots exported to {shots_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
