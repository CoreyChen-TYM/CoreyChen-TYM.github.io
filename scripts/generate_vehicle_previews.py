"""Generate small WebP hover previews while retaining original vehicle photos.

Run from any directory: python scripts/generate_vehicle_previews.py
Requires Pillow: python -m pip install Pillow
"""
from html.parser import HTMLParser
from pathlib import Path
import re

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / 'index.html'
PREVIEWS = ROOT / 'images/vehicles/previews'


class VehicleLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paths = set()

    def handle_starttag(self, tag, attrs):
        href = dict(attrs).get('href', '')
        if tag == 'a' and href.startswith('images/vehicles/'):
            self.paths.add(href)


def main():
    source = INDEX.read_text(encoding='utf-8')
    links = VehicleLinks()
    links.feed(source)
    PREVIEWS.mkdir(parents=True, exist_ok=True)
    originals = total = 0
    for name in sorted(links.paths):
        original = ROOT / name
        target = PREVIEWS / (original.stem + '.webp')
        with Image.open(original) as image:
            image = ImageOps.exif_transpose(image).convert('RGB')
            image.thumbnail((720, 520), Image.Resampling.LANCZOS)
            image.save(target, 'WEBP', quality=76, method=6)
        originals += original.stat().st_size
        total += target.stat().st_size
        preview = target.relative_to(ROOT).as_posix()
        pattern = r'<a\b[^>]*\bhref="' + re.escape(name) + r'"[^>]*>'

        def attach(match):
            tag = re.sub(r'\sdata-preview-src="[^"]*"', '', match.group())
            return tag[:-1] + f' data-preview-src="{preview}">'

        source = re.sub(pattern, attach, source)
        print(f'{original.name}: {original.stat().st_size / 1024:.1f} -> '
              f'{target.stat().st_size / 1024:.1f} KiB')
    INDEX.write_text(source, encoding='utf-8')
    print(f'{len(links.paths)} previews: {originals / 1024:.0f} -> '
          f'{total / 1024:.0f} KiB ({(1 - total / originals) * 100:.1f}% smaller)')


if __name__ == '__main__':
    main()
