I2S AND TDM IN PRACTICE - LAB
Corey Chen

Open the accompanying article for the complete explanation.

SMALL LAB KIT
  test.wav             48,000 Hz, stereo, signed 16-bit PCM in WAV
  test.mp3             Compressed audio example from the original attachment
  test.pcm             Headerless PCM extracted from the WAV data chunk
  test.txt / test.zip  Text and archive analogy, with English content
  I2S/output.pcm       Extracted left channel, signed 24-bit LE, mono, 48,000 Hz
  TDM/output.pcm       Extracted channel 1, signed 32-bit LE, mono, 48,000 Hz
  i2s.cpp              Portable C++ conversion example from the English article
  decode_pcm.py        Streaming Python converter, standard library only

FULL LAB
Download i2s-tdm-lab-v2.7z from the repository's GitHub Releases page.
Open the file with 7-Zip and extract. The complete archive also includes:
  I2S/raw.dsl
  I2S/txt2pcm/in.txt
  TDM/raw.dsl
  TDM/in.txt
  I2S/decoder-options.png
  I2S/pcm-import-settings.png

PYTHON CONVERSION (run from the extracted lab directory)
  python decode_pcm.py i2s I2S/txt2pcm/in.txt left.pcm
  python decode_pcm.py i2s I2S/txt2pcm/in.txt right.pcm --channel right
  python decode_pcm.py tdm TDM/in.txt channel1.pcm --channel 1

I2S output is 24-bit little-endian mono. TDM output is 32-bit little-endian
mono. In Audacity, import raw PCM using the matching format and 48,000 Hz.
Slots 1 and 2 in DSView's one-based TDM list correspond to slots 0 and 1
in zero-based interface terminology. Slot width is not necessarily the
number of meaningful bits in a sample.

C++ CONVERSION
  g++ -std=c++11 i2s.cpp -o txt2pcm
Run txt2pcm in a directory containing the I2S in.txt export.

WAV RAW-IMPORT EXPERIMENT
Use test.pcm, signed 16-bit LE, two channels, offset zero.
At 48,000 Hz it lasts 4.000021 seconds; at 16,000 Hz it lasts 12.000063.
Opening test.wav normally reads its format metadata automatically.

DATA CHECKS
The Python converter reproduces both supplied output.pcm files byte for
byte when extracting the I2S left channel and TDM channel 1 respectively.
I2S: 2,880,042 samples, 8,640,126 bytes, 60.000875 seconds at 48 kHz.
TDM: 196,444 samples, 785,776 bytes, 4.092583 seconds at 48 kHz.

SCREENSHOTS
English-localized screenshots are reading aids. Configuration tables and
the saved decoder metadata inside raw.dsl are authoritative for values.
The bit-clock cursor readouts in the original screenshots are approximate;
the nominal clocks are 2.304 MHz (I2S) and 24.576 MHz (TDM).

RIGHTS
Original tutorial: https://blog.csdn.net/weixin_40137374/article/details/149279354
Tutorial text: CC BY-SA 4.0. Music is by Khalil Fong; music and third-party
illustration rights remain with their respective owners.
