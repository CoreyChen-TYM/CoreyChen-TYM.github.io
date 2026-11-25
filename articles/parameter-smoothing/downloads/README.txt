WHY VOLUME KNOBS DON'T CLICK - LAB FILES
Corey Chen

Open the accompanying article for the complete explanation.

  test.pcm       2 s, 1 kHz sine, 48,000 Hz, stereo, signed 16-bit LE, headerless
  gain_step.c    Naive gain change: 1.0 -> 0.5 in one sample, no smoothing
  gain.dsp       FAUST's volume example (GRAME)
  sine_1k_5s.wav 5 s, 1 kHz sine, 48,000 Hz, stereo, 16-bit WAV, for the Faust IDE
  gain_faust.c   C code generated from gain.dsp: faust -lang c gain.dsp
  gain_smooth.c  gain_step.c plus FAUST's one-pole smoother

Build and run (Linux):
  gcc -O2 -o gain_step   gain_step.c   && ./gain_step     # writes test_1.pcm
  gcc -O2 -o gain_smooth gain_smooth.c && ./gain_smooth   # writes test_2.pcm

Listen to the results in Audacity:
  File -> Import -> Raw Data
  Signed 16-bit PCM, little-endian, 2 channels, 48000 Hz
