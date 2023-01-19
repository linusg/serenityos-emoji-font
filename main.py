from __future__ import annotations

import logging
import os
import subprocess
import unicodedata
from pathlib import Path

SERENITY_SOURCE_DIR = Path(os.environ["SERENITY_SOURCE_DIR"])
EMOJI_PNG_DIR = SERENITY_SOURCE_DIR / "Base/res/emoji"
BUILD_DIR = Path("build")
EMOJI_SVG_DIR = BUILD_DIR / "emoji"

HTML_TEMPLATE = """\
<!doctype html>
<html>
  <head>
    <title>SerenityOS Emoji Font</title>
    <link href="SerenityOS-Emoji.css" rel="stylesheet">
    <style>
      body {{
        font-family: sans-serif;
      }}
      code {{
        font-size: 1.2em;
      }}
      .emoji-grid {{
        display: flex;
        flex-wrap: wrap;
      }}
      .emoji {{
        font-family: "SerenityOS Emoji";
        font-size: 64px;
        border: 2px solid black;
        margin: 2px;
      }}
    </style>
  </head>
  <body>
    <p>
      <code>SerenityOS-Emoji.ttf</code> currently contains the following {emoji_count} emojis:
    </p>
    <section class="emoji-grid">
      {emojis}
    </section>
  </body>
</html>
"""


logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def convert_images() -> None:
    EMOJI_SVG_DIR.mkdir(parents=True, exist_ok=True)
    png_files = EMOJI_PNG_DIR.glob("*.png")
    svg_files = EMOJI_SVG_DIR.glob("*.svg")
    svg_to_png_file_map = {
        EMOJI_SVG_DIR
        / png_file.name.replace("U+", "").replace(".png", ".svg"): png_file
        for png_file in png_files
        # Skip PUA emojis, they're too large and take forever to process
        # with the naively vectorized images. It's possible to include them
        # in the font though.
        if not any(
            unicodedata.category(chr(int(code_point, 16))) == "Co"
            for code_point in png_file.stem.replace("U+", "").split("_")
        )
    }
    missing_svg_files = sorted(set(svg_to_png_file_map.keys()) - set(svg_files))
    for i, svg_file in enumerate(missing_svg_files):
        png_file = svg_to_png_file_map[svg_file]
        logger.info(f"[{i + 1}/{len(missing_svg_files)}] Converting {png_file.name}")
        subprocess.call(["python3", "pixart2svg.py", str(png_file), str(svg_file)])


def build_font(emoji_svg_paths: list[str]) -> None:
    subprocess.call(
        [
            "nanoemoji",
            "--family",
            "SerenityOS Emoji",
            "--output_file",
            "SerenityOS-Emoji.ttf",
            "--color_format",
            "glyf_colr_1",
            *emoji_svg_paths,
        ]
    )


def build_html_test_file(emoji_svg_paths: list[str]) -> None:
    (BUILD_DIR / "index.html").write_text(
        HTML_TEMPLATE.format(
            emoji_count=len(emoji_svg_paths),
            emojis="\n".join(
                "".join(
                    [
                        "    ",
                        '<span class="emoji">',
                        *(
                            chr(int(code_point, 16))
                            for code_point in Path(file).stem.split("_")
                        ),
                        "</span>",
                    ]
                )
                for file in emoji_svg_paths
            ),
        )
    )


def main() -> None:
    logger.info("Converting PNG images to SVG...")
    convert_images()
    logger.info("Done.")

    emoji_svg_paths = sorted(str(path) for path in EMOJI_SVG_DIR.glob("*.svg"))

    logger.info("Building font file...")
    build_font(emoji_svg_paths)
    logger.info("Done.")

    logger.info("Building HTML test file...")
    build_html_test_file(emoji_svg_paths)
    logger.info("Done.")


if __name__ == "__main__":
    main()
