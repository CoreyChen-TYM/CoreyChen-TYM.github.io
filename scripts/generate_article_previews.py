"""Build article WebP display images and hover thumbnails, keeping full PNGs.

Run: python scripts/generate_article_previews.py (requires Pillow).
"""
from pathlib import Path
import re
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
ARTICLES = ROOT / 'articles'


def webp(source, target, bounds):
    target.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(source) as image:
        image = ImageOps.exif_transpose(image)
        image = image.convert('RGBA' if 'A' in image.getbands() else 'RGB')
        image.thumbnail(bounds, Image.Resampling.LANCZOS)
        image.save(target, 'WEBP', quality=90, method=6)


def main():
    before = after = 0
    replacements = {}
    for folder in sorted(ARTICLES.iterdir()):
        images = folder / 'images'
        if not images.is_dir():
            continue
        for original in sorted(images.glob('*.png')):
            if original.stat().st_size < 32 * 1024:
                continue
            optimized = images / 'optimized' / (original.stem + '.webp')
            webp(original, optimized, (1600, 1600))
            if optimized.stat().st_size >= original.stat().st_size:
                optimized.unlink()
                continue
            replacements[original] = optimized
            before += original.stat().st_size
            after += optimized.stat().st_size
            print(f'{folder.name}/{original.name}: '
                  f'{original.stat().st_size / 1024:.0f} -> '
                  f'{optimized.stat().st_size / 1024:.0f} KiB')
        for page in folder.glob('*.html'):
            text = page.read_text(encoding='utf-8')

            def replace_image(match):
                tag = match.group()
                src = re.search(r'\bsrc="([^"]+)"', tag)
                if not src:
                    return tag
                relative = src[1]
                if relative.startswith('images/optimized/'):
                    relative = 'images/' + Path(relative).stem + '.png'
                original = folder / relative
                if original not in replacements:
                    return tag
                target = replacements[original].relative_to(folder).as_posix()
                return tag[:src.start(1)] + target + tag[src.end(1):]

            text = re.sub(r'<img\b[^>]*>', replace_image, text)
            page.write_text(text, encoding='utf-8')

    # Hover previews have a separate resolution budget from article figures.
    home = ROOT / 'index.html'
    text = home.read_text(encoding='utf-8')

    def replace_hover(match):
        relative = match[1]
        if not relative.startswith('articles/'):
            return match.group()
        original = ROOT / relative
        if original.suffix == '.webp' and original.parent.name == 'previews':
            original = original.parent.parent / (original.stem + '.png')
        if original.suffix != '.png':
            return match.group()
        target = original.parent / 'previews' / (original.stem + '.webp')
        webp(original, target, (720, 520))
        return 'data-preview-src="' + target.relative_to(ROOT).as_posix() + '"'

    text = re.sub(r'data-preview-src="([^"]+)"', replace_hover, text)
    home.write_text(text, encoding='utf-8')
    print(f'Article display images: {before / 1024 / 1024:.2f} -> '
          f'{after / 1024 / 1024:.2f} MiB '
          f'({(1 - after / before) * 100:.1f}% smaller). Full PNG links retained.')


if __name__ == '__main__':
    main()
