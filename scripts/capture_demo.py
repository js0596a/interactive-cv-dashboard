from __future__ import annotations

import argparse
import os
from pathlib import Path
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


def build_gif(frames: list[Path], output_path: Path) -> None:
    images = []
    for i, frame_path in enumerate(frames):
        frame = Image.open(frame_path).convert("RGB")
        frame = frame.resize((1200, 760), Image.Resampling.LANCZOS)
        repeats = 4 if i in (0, len(frames) - 1) else 2
        for _ in range(repeats):
            images.append(frame.copy())

    output_path.parent.mkdir(parents=True, exist_ok=True)
    imageio.mimsave(output_path, images, duration=0.55, loop=0)


def run_capture(port: int, output_path: Path) -> None:
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
        build_gif(frame_paths, output_path)

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
    args = parser.parse_args()

    output = Path(args.output).resolve()
    run_capture(port=args.port, output_path=output)
    print(f"Demo GIF written to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
