#!/usr/bin/env python3
"""
Prepares pictures for sd_photo_frame.py. Run this on your computer, not on the Inky Frame.

Each picture is turned the right way up, cropped and resized to 640x400, made a
little more vivid to suit the ePaper's limited colours, and saved as a
non-progressive jpg with a filename the SD card can store safely.

    pip install pillow
    python3 prepare_photos.py my_photos sd_ready

Then copy the contents of the sd_ready folder to the root of the SD card.
Use --pad to keep the whole picture and add white bars instead of cropping,
which suits portrait photos.
"""

import argparse
import re
import sys
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps

SIZE = (640, 400)
INPUT_TYPES = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff", ".gif"}

# Matches the known-good samples in the 640x400 folder: baseline and 4:4:4
JPEG_OPTIONS = {"quality": 90, "subsampling": 0, "progressive": False}


def prepare(source, pad, saturation, contrast):
    with Image.open(source) as original:
        image = ImageOps.exif_transpose(original)

        # Transparent areas become white, the colour of the frame's bars
        if image.mode in ("RGBA", "LA", "PA") or "transparency" in image.info:
            image = image.convert("RGBA")
            image = Image.alpha_composite(Image.new("RGBA", image.size, "white"), image)
        image = image.convert("RGB")

    if pad:
        image = ImageOps.pad(image, SIZE, Image.Resampling.LANCZOS, color="white")
    else:
        image = ImageOps.fit(image, SIZE, Image.Resampling.LANCZOS)

    image = ImageEnhance.Color(image).enhance(saturation)
    return ImageEnhance.Contrast(image).enhance(contrast)


def output_name(source, used):
    # Plain ASCII names only, as accented names can be garbled on the card
    stem = re.sub(r"[^A-Za-z0-9_-]+", "_", source.stem).strip("_") or "photo"
    name = stem
    count = 2
    while name.lower() in used:  # FAT filenames aren't case sensitive
        name = f"{stem}_{count}"
        count += 1
    used.add(name.lower())
    return name + ".jpg"


def find_sources(input_dir, output_dir):
    sources = []
    for path in sorted(input_dir.rglob("*")):
        hidden = any(part.startswith(".") for part in path.relative_to(input_dir).parts)
        if path.is_file() and not hidden and output_dir not in path.parents:
            sources.append(path)
    return sources


def main():
    parser = argparse.ArgumentParser(description="Prepare pictures for the 4.0 inch Inky Frame photo frame.")
    parser.add_argument("input", type=Path, help="folder of pictures, subfolders included")
    parser.add_argument("output", type=Path, help="folder for the prepared pictures")
    parser.add_argument("--pad", action="store_true", help="add white bars instead of cropping")
    parser.add_argument("--saturation", type=float, default=1.3, help="colour boost, 1.0 leaves it unchanged (default: 1.3)")
    parser.add_argument("--contrast", type=float, default=1.1, help="contrast boost, 1.0 leaves it unchanged (default: 1.1)")
    args = parser.parse_args()

    if not args.input.is_dir():
        sys.exit(f"Folder not found: {args.input}")

    input_dir = args.input.resolve()
    output_dir = args.output.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    used = set()
    prepared = 0
    skipped = 0

    for source in find_sources(input_dir, output_dir):
        if source.suffix.lower() not in INPUT_TYPES:
            print(f"Skipped {source.name}: not a supported picture type")
            skipped += 1
            continue
        try:
            image = prepare(source, args.pad, args.saturation, args.contrast)
        except (OSError, ValueError, Image.DecompressionBombError) as e:
            print(f"Skipped {source.name}: {e}")
            skipped += 1
            continue
        name = output_name(source, used)
        image.save(output_dir / name, "JPEG", **JPEG_OPTIONS)
        print(f"{source.name} -> {name}")
        prepared += 1

    print(f"Prepared {prepared}, skipped {skipped}. Copy the files in {output_dir} to the root of the SD card.")
    if prepared == 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
