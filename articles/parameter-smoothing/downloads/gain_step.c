/*
 * gain_step.c - jump the gain from 1.0 to 0.5 at t = 1.00025 s (a sine peak), no smoothing.
 *
 * Input : test.pcm   (raw PCM, 48 kHz, 16-bit, 2 ch, interleaved)
 * Output: test_1.pcm
 *
 * gcc -O2 -o gain_step gain_step.c && ./gain_step
 */

#include <stdio.h>
#include <stdint.h>

#define SAMPLE_RATE 48000
#define CHANNELS    2

int main(void)
{
    FILE *in  = fopen("test.pcm", "rb");
    FILE *out = fopen("test_1.pcm", "wb");
    if (!in || !out) { perror("fopen"); return 1; }

    int16_t frame[CHANNELS];
    long n = 0;                                   /* frame index */

    while (fread(frame, sizeof(int16_t), CHANNELS, in) == CHANNELS) {
        float gain = (n < SAMPLE_RATE + 12) ? 1.0f : 0.5f;   /* hard step at a peak (1.00025 s) */

        for (int c = 0; c < CHANNELS; c++)
            frame[c] = (int16_t)(frame[c] * gain);

        fwrite(frame, sizeof(int16_t), CHANNELS, out);
        n++;
    }

    fclose(in);
    fclose(out);
    return 0;
}
