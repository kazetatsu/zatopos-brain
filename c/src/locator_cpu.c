// #include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#include "sound.h"
#include "locator.h"

static const float q[NUM_MIC_CHS - 1][2] = {
    { 0.5f,  0.86f},
    {-0.5f,  0.86f},
    {-1.0f,  0.0f},
    {-0.5f, -0.86f},
    { 0.5f, -0.86f},
};

struct locator {
    int res_x;
    int res_y;
    float dist_x;
    float dist_y;
    float* freq;
    int freq_len;
};

locator_t* locator_malloc(void) {
    return (locator_t*)calloc(1, sizeof(locator_t));
}

unsigned int locator_init(locator_t* locator) {
    // printf("initialized\n");
    return 0;
}

void locator_delete(locator_t* locator) {
    if (locator->freq != NULL)
        free(locator->freq);
    free(locator);
    // printf("deleted\n");
}

unsigned int locator_set_frequency(locator_t* locator, float* freq, int len) {
    locator->freq = freq;
    locator->freq_len = len;
    locator->freq = (float*)malloc(len * sizeof(float));
    for (int f = 0; f < len; f++)
        locator->freq[f] = freq[f];
    // printf("set freq: len=%d\n", locator->freq_len);
    return 0;
}

unsigned int locator_set_resolution(locator_t* locator, int x, int y) {
    locator->res_x = x;
    locator->res_y = y;
    // printf("set resolution: x=%d, y=%d\n", locator->res_x, locator->res_y);
    return 0;
}

unsigned int locator_set_distance(locator_t* locator, float x, float y) {
    locator->dist_x = x;
    locator->dist_y = y;
    // printf("set distance: x=%f, y=%f\n", locator->dist_x, locator->dist_y);
    return 0;
}

unsigned int locator_locate(locator_t* locator, float *E, float *result) {
    // steering vector
    float v_re[NUM_MIC_CHS];
    float v_im[NUM_MIC_CHS];

    int stride_f = NUM_MIC_CHS * NUM_MIC_CHS * 2;
    int stride_c = NUM_MIC_CHS * 2;

    for (int ix = 0; ix < locator->res_x; ix++) {
        for (int iy = 0; iy < locator->res_y; iy++) {
            // calculate p: position
            float px = (float)ix - (float)locator->res_x / 2.0f;
            float py = (float)iy - (float)locator->res_y / 2.0f;
            float coef = sqrtf(locator->res_x * locator->res_x + locator->res_y * locator->res_y) / 2.0f;
            px /= coef;
            py /= coef;
            px *= locator->dist_x;
            py *= locator->dist_y;

            for (int i = 0; i < locator->freq_len; i++) {
                // calculate v: steering vector
                coef = locator->freq[i] * 0.001109 / sqrtf(px * px + py * py + 6.25f);
                float theta = coef * px;
                v_re[0] = cosf(theta);
                v_im[0] = sinf(theta);
                for (unsigned char j = 1; j < NUM_MIC_CHS; j++) {
                    theta = q[j-1][0] * px + q[j-1][1] * py;
                    theta *= coef;
                    v_re[j] = cosf(theta);
                    v_im[j] = sinf(theta);
                }

                // calculate || v^T E ||^2
                float res = 0.0f;
                float u_re, u_im;
                for (unsigned char c = 1; c < NUM_MIC_CHS; c++) {
                    u_re = 0.0f;
                    u_im = 0.0f;
                    for (unsigned char r = 0; r < NUM_MIC_CHS; r++) {
                        int pibot = i * stride_f + c * stride_c + r * 2;
                        u_re += v_re[r] * E[pibot    ] - v_im[r] * E[pibot + 1];
                        u_im += v_re[r] * E[pibot + 1] + v_im[r] * E[pibot    ];
                    }
                    res += u_re * u_re + u_im * u_im;
                }

                // calculate average
                result[ix * locator->res_y + iy] += res;
            }
        }
    }

    return 0;
}
