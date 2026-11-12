# From Imaginary Numbers to FFT: migration notes

## Scope

The overview and Parts 1–3 are translated from the author’s four CSDN pages.
Parts 4–5 remain planned entries, as in the original overview. No unwritten
chapters or additional technical conclusions have been invented.

The author requested faithful translation, including voice, examples,
simplifications, technical claims, and errors. No technical corrections are
silently applied. Chinese publishing-platform navigation, keyword summaries,
recommendations, and generated copyright boilerplate are excluded.

## Pages and dates

- Overview: 149780297; CSDN currently displays 2025-09-07.
- Part 1: 149810506; CSDN displays 2025-08-07.
- Part 2: 151228492; homepage listing displays 2025-09-06. Its article header
  currently shows a recommendation timestamp instead of its original date.
- Part 3: 151264661; CSDN displays 2025-09-08.

Journal dates retain month precision. The page-level timestamps and author
bylines are omitted to match the existing I2S/TDM article.

## Equations and illustrations

76 expressions are typeset as static KaTeX HTML plus accessible MathML. The
original TeX remains in each equation’s MathML annotation. Formulas work
without JavaScript and without an external CDN. KaTeX 0.16.22 CSS and fonts
are bundled under vendor/katex, along with its license. Its JavaScript bundle
was used to render the expressions during preparation.

image-sources.json maps all 95 original math-image and illustration entries
(including repeated entries) to their migrated representation. No formula or
illustration position was dropped. Mathematical screenshots are transcribed
into equations; Chinese prose in quoted screenshots becomes translated
blockquote text. All external image URLs are retained in that source map.

The impulse plot, six-panel impulse decomposition, convolution example, and
system block diagram are recreated as code-native SVG. The convolution
example keeps x={2,1,1}, h={4,2,1}, and y={8,8,8,3,1}. The decomposition figure
preserves the original sample positions and relative stem-height pattern;
its unlabeled vertical scale is illustrative, as in the original.

The original Latin excerpt and the three projection plots are retained.
The Latin excerpt is primary-source material, not untranslated Chinese.

## Raster localization: built-in ImageGen

Four images were localized using the built-in image tool, not the CLI:

1. rotating-vector.png: replace only red y-axis, x-axis, and t-axis Chinese
   labels with “y axis”, “x axis”, and “t axis”; preserve the helix and axes.
2. spectrum-48k.png: translate Frequency Analysis, Cursor, Peak, Grid,
   Algorithm, Spectrum, Size, Export, Window, Hann window, Axis, Linear
   frequency, Replot, Close, and “Spectrum imported at 48K”. Preserve the
   spectrum, 1024 setting, ticks, numeric values, and original layout.
3. spectrum-24k.png: the same label translation, with “Spectrum imported at
   24K”; preserve its distinct frequency axis and the spectrum.
4. sample-rate-comparison.png: translate both track panels’ Mute, Solo,
   Effects, L, R labels; retain the top 48K / bottom 24K comparison. A follow-up
   fixes a remaining right-balance Chinese character in the upper panel.

Generated screenshots are illustrations; the source screenshots remain in
ignored working files for review. The migration does not modify the supplied
audio files or existing I2S/TDM downloads.

## Layout and interactions

Existing Roboto, black links, uppercase section headings, compact measure,
paired figures, and click-to-enlarge viewer are reused. All four pages link
to the overview and each published part. Parts 1–3 have previous/next links.
The third part links to the existing I2S/TDM article and matching lab download.
The Journal includes all four entries, with image previews on title hover.

## Validation

All 76 formulas rendered successfully with strict KaTeX parsing. All local
links, navigation targets, images, scripts, stylesheets, and font paths resolve.
The 95 source image entries are mapped; the published pages contain 12
figures and 76 mathematical expressions. No Chinese text or remote runtime
assets remain in the four HTML pages. English raster labels were inspected.
The overview, Parts 1–3, Journal entries, and image viewer were reviewed in
the browser. At a 390-pixel viewport, the three articles have no horizontal
page overflow. Clicking an enlarged image closes it and restores focus.

Replaced the unavailable 23bei calculator link with Calxy’s convolution calculator. Browser verification using x={2,1,1}, h={4,2,1} produced {8,8,8,3,1}, with per-output product steps.
