# English edition notes

Source article: https://blog.csdn.net/weixin_40137374/article/details/149279354
Originally published July 13, 2025; original revision July 31, 2025.
Author: Corey Chen. English edition prepared November 12, 2026.

## Images

All 23 inline source images are represented, indexed in source order as
`images/00.png` through `images/22.png` (00 is the zoom-tool icon).
The original source-image URL list is recorded in `image-sources.json`.
Unmodified source images: 00, 01, 07, 08, 14, 16, 19.
English-localized images: 02, 03, 04, 05, 06, 09, 10, 11, 12, 13, 15,
17, 18, 20, 21, 22.

Localized raster assets were made with the built-in ImageGen tool, using
the original image as the edit target. They are translated illustrations,
not newly acquired measurements. Preserve the raw captures as the source
of truth. CSS removes the generated white letterboxing from narrow traces
in the article; it does not alter the saved images.

### Localization prompt set

Common instructions: `Use case: text-localization. Translate this exact
technical screenshot into English. Change text only. Preserve every
technical value, graph, arrow, waveform, layout, and color. Do not invent
samples or UI controls. Output only the localized figure.`

Per-figure text/constraints added to that instruction:

| Figure | English replacements and protected values |
| --- | --- |
| 02 | Replace the red sample-count annotation with `48 samples`; retain the red box and 0.0010, 0.0015, 0.0020 axis labels. |
| 03 | `Mute`, `Solo`, `Effects`, `L`, `R`, `Channel 1`, `Channel 2`; preserve both waveforms and numeric scales. |
| 04 | `Import Raw Data: test.wav`, `Encoding`, `Byte order`, `Channels`, `Start offset`, `Amount to import`, `Sample rate`, `Signed 16-bit PCM`, `Default endianness`, `2 Channels (Stereo)`, `0 bytes`, `100%`, `16000 Hz`, `Detect`, `Import`, `Cancel`. |
| 05 | Same as 04, but preserve `48000 Hz`. |
| 06 | `Anti-aliasing filter`, `Analog filter`, `Digital processing`, `Reconstruction filter`, `Analog input`, `Filtered analog input`, `Digitized input`, `Digital output`, `Sample-and-hold output`, `Analog output`; retain ADC, DAC, both red DAI arrows and the six waveform sketches. |
| 09 | `Decoder options`, `Decode start position`, `Decode end position`, `OK`, `Cancel`; retain probes 0/1/2, left-low, rising-edge, right-shifted by one, left-aligned, msb-first, word size 24. |
| 10 | Translate toolbar and panels to File, Options, Start, Instant, Trigger, Decode, Measure, Search, Display, File, Help, Logic Analyzer, Protocol, Protocol list, Matches, Search. Red callouts: Protocol decoder, Decode progress, Decoder settings, Decoded results. Preserve DSView v1.2.0, 100 MHz, 100%, decoded hex values and traces. |
| 11 | Red annotations `Left channel`, `Right channel`; retain slot0/slot1, SCK, WS, SD out and decoded values. |
| 12 | Width, Period, Frequency, Duty cycle; preserve +10.41 us, +20.84 us, 47.98 KHz, 49.95%. |
| 13 | Width, Period, Frequency, Duty cycle; preserve +210 ns, +430 ns, 2.33 MHz, 48.84%. |
| 15 | Protocol list, Search, Matches; preserve 5760085, the save icon, red arrow, indices 0-6 and all sample hex values. |
| 17 | Import Raw Data: output.pcm; Signed 24-bit PCM, Default endianness, 1 Channel (Mono), 0 bytes, 100%, 48000 Hz; English labels and Detect/Import/Cancel buttons. |
| 18 | Mute, Solo, Effects, L, R; preserve output title, 60-second time axis and waveform. |
| 20 | Width, Period, Frequency, Duty cycle; preserve +10.42 us, +20.83 us, 48.01 KHz, 50.02%, red box, numbered slots and signal labels. |
| 21 | Decoder options, Translate parameter names, Decode start/end position, OK, Cancel; preserve SCK 0, SYNC 1, SD 2, channel size 32, channels 16, falling-edge, rising-edge, bit shift 0. |
| 22 | Width, Period, Frequency, Duty cycle; preserve +20 ns, +40 ns, 25.00 MHz, 50.00%, Channel 1: 2fd50000 and the original traces. |

## Technical clarifications from the Chinese edition

- Use 44.1 kHz rather than 44 kHz. Higher sample rate is not automatically
  better audible quality; sample rate determines bandwidth with filtering.
- Distinguish WAV container metadata from sample payload, and MP3 lossy
  decoding from ZIP decompression. Raw-importing a WAV at offset zero
  includes the header; supply clean `test.pcm` as well.
- Distinguish a DAC from a power amplifier; some devices integrate both.
- A full-duplex example has four signal lines; basic unidirectional I2S
  uses three. Extra MCLK/ground signals are outside that drawing.
- Channel/slot vocabulary is explained as a workplace convention; slot
  width is not necessarily valid audio bit depth.
- I2S time-multiplexes stereo, but is not unconditionally equivalent to
  any chip's TDM2 mode. Keep the one-bit standard I2S delay explicit.
- Correct nominal clocks to 2.304 MHz and 24.576 MHz, keeping the original
  cursor readouts 2.33 MHz and 25 MHz labeled as coarse measurements from
  a 100 MHz logic-analyzer capture.
- Sixteen slots apply per data line. The 32-channel diagram uses two lines
  per direction. Explain DSView's one-based TDM channel numbering.
- C++ output now truncates correctly, tests streams correctly, and writes
  explicit little-endian bytes. The original C++ is retained in the full
  lab as `I2S/txt2pcm/i2s-original.cpp`.

## Verification

### Editorial review after the first draft

- Corrected the invented literal book title and removed the unsupported
  claim that the book was originally Chinese. The verified title is
  *Digital Signal Processing: A Practical Guide for Engineers and
  Scientists*, by Steven W. Smith. Primary sources:
  https://www.dspguide.com/editions.htm and
  https://shop.elsevier.com/books/digital-signal-processing-a-practical-guide-for-engineers-and-scientists/smith/978-0-7506-7444-7
- Removed the edition-dependent page 38 reference rather than implying
  the Chinese edition's pagination applied to the English book.
- Reworked the literal tongdao/shengdao discussion into channel count and
  channel layout; it no longer implies decoding changes channel meaning.
- Removed leftover reader-facing translation commentary from captions
  and the code introduction. Source/provenance notes remain in this file.
- Rechecked both decoder configurations against the captures, WAV metadata,
  nominal-clock arithmetic, PCM sample counts, and the full TDM export.
  TDM channels 3-16 have zero nonzero samples throughout the supplied export.
- The portable C++ example has been reviewed but not compiled in this
  environment. Byte-for-byte converter validation applies to the Python
  implementation, not a claim that the C++ example was executed.

Both DSView decoder configurations were read from the actual `.dsl` ZIP
metadata. Python reconstruction from the original exported text matches
both provided `output.pcm` files byte for byte (SHA-256 comparison).
I2S left channel: 2,880,042 24-bit samples, 60.000875 seconds at 48 kHz.
TDM channel 1: 196,444 32-bit words, 4.092583333 seconds at 48 kHz.
WAV: 48 kHz, stereo, 16-bit PCM, 192,001 frames; 768,004 payload bytes.

The full lab is hosted as one archive in the existing repository's GitHub
Release `i2s-tdm-lab-v1`; large binary attachments are not stored in Git.
Release: https://github.com/CoreyChen-TYM/CoreyChen-TYM.github.io/releases/tag/i2s-tdm-lab-v1
Asset: `i2s-tdm-lab.7z`, 228,196,737 bytes.
SHA-256: `c5c465d1bc38ee4c7318ca1822fe7968d387585469a116c9000e42a4fb66f4ec`.
GitHub's returned asset digest matched the local archive. The archive and
the small ZIP kit both include the updated single-file download instructions.
Opening the article does not automatically download the full lab.

Article presentation uses CSS crops to remove screenshot whitespace and
redundant controls while retaining the relevant signals and annotations.
Original image files remain intact and open when their figures are clicked.
The raw-import comparison and export screenshots are paired; decoder settings
sit beside their parameter tables on wider screens and stack on mobile.
Desktop and 390-pixel mobile layouts were checked in the browser, with no
horizontal page overflow observed.


## Author-directed faithful retranslation

The author requested preservation of the original voice, analogies, rhetorical
questions, simplifications, technical claims, and even errors. The article body
was retranslated against the saved CSDN source accordingly. Earlier editorial
corrections and added technical explanations in this document are historical
audit notes, not the policy for the published prose. The original C++ example
is restored verbatim. The previously identified English book title is retained.
Chinese channel terminology is explained with romanization so that its original
workplace distinction survives in English. The 22 figures, display crops, and
attachment links are retained; added instructional prose and corrections are
removed. Figure captions now follow the original discussion.

Figure 07: remaining Chinese annotations translated into English and lower-right website URL removed at the author’s request. Hex value 0x91261400 retained.

Lab naming update: full archive i2s-tdm-lab-v2.7z now extracts to i2s-tdm-lab/; small kit renamed i2s-tdm-lab-kit.zip. Updated article and bundled READMEs. SHA-256: a4961b4b990320a564b98a8521f7fe587f35567a2d24dbba2454aad7969af922
