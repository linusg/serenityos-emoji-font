# SerenityOS Emoji Font

The [SerenityOS pixel art emojis](https://emoji.serenityos.net/) embedded in a TrueType font.

![banner](banner.png)

## Installation & Usage

A nightly build of the font is done automatically via GitHub Actions, you can download it from [here](https://nightly.link/linusg/serenityos-emoji-font/workflows/build/main/SerenityOS-Emoji.ttf.zip).

The font can be installed as a system wide font for emojis, used on a website, and more. The former will depend a lot on your operating system and desktop environment, an example for the latter can be found in the HTML file included in the archive mentioned above.

Please make sure to include a copy of the [`LICENSE`](LICENSE) file when distributing the font!

## Building locally

Uses [`pixart2svg`](https://gist.github.com/m13253/66284bc244deeff0f0f8863c206421c7) for vectorization of the emoji PNG images and [`nanoemoji`](https://github.com/googlefonts/nanoemoji) to build the font. SVGs are cached, so subsequent runs of the build script will be much faster.

- Clone SerenityOS and export the path of your local checkout:

  ```shell
  export SERENITY_SOURCE_DIR='...'
  ```

- Install dependencies:

  ```console
  pip install --user -r requirements.txt
  ```

- Download and patch `pixart2svg`:

  ```shell
  wget https://gist.githubusercontent.com/m13253/66284bc244deeff0f0f8863c206421c7/raw/f9454958dc0a33cea787cc6fbd7e8e34ba6eb23b/pixart2svg.py
  for file in patches/*.patch; do
    patch -p0 < "$file"
  done
  ```

- Build `SerenityOS-Emoji.ttf`:

  ```console
  python main.py
  ```

The output files (TTF, `index.html` listing all included emojis) will be in `build/`.

## TODO

This is an initial proof of concept that could be refined in multiple ways:

- Replace `pixart2svg` with something that is more flexible and doesn't need to be patched locally (it's GPL-licensed)
- Find a better approach for vectorization - the current solution of using adjacent SVG rects should in theory yield perfect results but has visible gaps between segments in reality, depending on the renderer and zoom level

## Credit

This wouldn't be possible without all the awesome people creating & refining these emojis for the SerenityOS project! ❤
