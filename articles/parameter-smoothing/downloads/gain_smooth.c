/*
 * gain_smooth.c - the same experiment as gain_step.c, but with the
 * one-pole smoother taken from FAUST's si.smoo (see gain_faust.c).
 *
 * Input : test.pcm   (raw PCM, 48 kHz, 16-bit, 2 ch, interleaved)
 * Output: test_2.pcm
 *
 * gcc -O2 -o gain_smooth gain_smooth.c && ./gain_smooth
 */

#include <stdio.h>
#include <stdint.h>

#define SAMPLE_RATE 48000
#define CHANNELS    2

int main(void)
{
    FILE *in  = fopen("test.pcm", "rb");
    FILE *out = fopen("test_2.pcm", "wb");
    if (!in || !out) { perror("fopen"); return 1; }

    const float s = 1.0f - 44.1f / SAMPLE_RATE;   /* pole, same as FAUST's fConst1 */
    float g = 1.0f;                                /* smoothed gain, FAUST's fRec0 */

    int16_t frame[CHANNELS];
    long n = 0;

    while (fread(frame, sizeof(int16_t), CHANNELS, in) == CHANNELS) {
        float target = (n < SAMPLE_RATE + 12) ? 1.0f : 0.5f;   /* same hard step */

        g = (1.0f - s) * target + s * g;          /* the one line that smooths */

        for (int c = 0; c < CHANNELS; c++)
            frame[c] = (int16_t)(frame[c] * g);

        fwrite(frame, sizeof(int16_t), CHANNELS, out);
        n++;
    }

    fclose(in);
    fclose(out);
    return 0;
}
