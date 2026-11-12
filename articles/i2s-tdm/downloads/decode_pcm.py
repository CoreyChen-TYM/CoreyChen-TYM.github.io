"""Extract one channel from a DSView text export as little-endian PCM."""

import argparse
import re
from pathlib import Path


def convert(mode, source, destination, channel=None):
    source = Path(source)
    destination = Path(destination)
    if source.resolve() == destination.resolve():
        raise ValueError("Input and output paths must differ")
    if mode == "i2s":
        channel = "left" if channel is None else channel.lower()
        if channel not in ("left", "right"):
            raise ValueError("I2S channel must be left or right")
        pattern = re.compile(rf"{channel} channel:\s*([0-9a-fA-F]+)\s*$", re.I)
        width = 3
    elif mode == "tdm":
        channel = 1 if channel is None else int(channel)
        if not 1 <= channel <= 16:
            raise ValueError("TDM channel must be between 1 and 16")
        pattern = re.compile(rf"Channel {channel}\s*:\s*([0-9a-fA-F]+)\s*$")
        width = 4
    else:
        raise ValueError("Mode must be i2s or tdm")
    mask = (1 << (width * 8)) - 1
    count = 0
    with source.open(encoding="utf-8-sig") as src, destination.open("wb") as dst:
        for line in src:
            match = pattern.search(line)
            if match:
                value = int(match[1], 16) & mask
                dst.write(value.to_bytes(width, "little"))
                count += 1
    if not count:
        destination.unlink()
        raise ValueError("No samples matched the requested channel")
    return count, width


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("i2s", "tdm"))
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--channel", help="left/right for I2S, 1-16 for TDM")
    args = parser.parse_args()
    try:
        samples, width = convert(args.mode, args.input, args.output, args.channel)
    except (ValueError, OSError) as error:
        parser.exit(1, f"Error: {error}\n")
    print(f"Wrote {samples:,} samples as {width * 8}-bit little-endian mono PCM.")
    print(f"Duration at 48,000 Hz: {samples / 48000:.6f} seconds.")
