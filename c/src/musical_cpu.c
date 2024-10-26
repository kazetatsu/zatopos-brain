// SPDX-FileCopyrightText: 2024 ShinagwaKazemaru
// SPDX-License-Identifier: MIT License

// #include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#include "musical.h"

static const float q[EAR_NUM_MICS - 1][2] = {
    { 0.5f,  0.86f},
    {-0.5f,  0.86f},
    {-1.0f,  0.0f},
    {-0.5f, -0.86f},
    { 0.5f, -0.86f},
};

struct musical {
    int res_x;
    int res_y;
    float dist_x;
    float dist_y;
    float* freq;
    int freq_len;
};

musical_t* musical_malloc(void) {
    return (musical_t*)calloc(1, sizeof(musical_t));
}

unsigned int musical_init(musical_t* music) {
    // printf("initialized\n");
    return 0;
}

void musical_delete(musical_t* music) {
    if (music->freq != NULL)
        free(music->freq);
    free(music);
    // printf("deleted\n");
}

unsigned int musical_set_frequency(musical_t* music, float* freq, int len) {
    music->freq = freq;
    music->freq_len = len;
    music->freq = (float*)malloc(len * sizeof(float));
    for (int f = 0; f < len; f++)
        music->freq[f] = freq[f];
    return 0;
}

unsigned int musical_set_resolution(musical_t* music, int x, int y) {
    music->res_x = x;
    music->res_y = y;
    // printf("set resolution: x=%d, y=%d\n", music->res_x, music->res_y);
    return 0;
}

unsigned int musical_set_distance(musical_t* music, float x, float y) {
    music->dist_x = x;
    music->dist_y = y;
    // printf("set distance: x=%f, y=%f\n", music->dist_x, music->dist_y);
    return 0;
}

unsigned int musical_search(musical_t* music, float *eig_vecs, float *result) {
    // steering vector
    float v_re[EAR_NUM_MICS];
    float v_im[EAR_NUM_MICS];

    int stride_r_if = music->res_x * music->res_y; // result, index of frequency
    int stride_r_iy = music->res_x;
    int stride_e_if = EAR_NUM_MICS * EAR_NUM_MICS * 2; // eigen vector, index of frequency
    int stride_e_c = EAR_NUM_MICS * 2;

    for (int ix = 0; ix < music->res_x; ix++) {
        for (int iy = 0; iy < music->res_y; iy++) {
            // calculate p: position
            float px = (float)(2 * ix - music->res_x + 1) / 2.0f;
            float py = (float)(2 * iy - music->res_y + 1) / 2.0f;
            px *= music->dist_x / (float)music->res_x;
            py *= music->dist_y / (float)music->res_y;

            for (int i_f = 0; i_f < music->freq_len; i_f++) {
                // calculate v: steering vector
                float coef = music->freq[i_f] * 0.001109 / sqrtf(px * px + py * py + 6.25f);
                float theta = coef * px;
                v_re[0] = cosf(theta);
                v_im[0] = sinf(theta);
                for (unsigned char j = 1; j < EAR_NUM_MICS; j++) {
                    theta = q[j-1][0] * px + q[j-1][1] * py;
                    theta *= coef;
                    v_re[j] = cosf(theta);
                    v_im[j] = sinf(theta);
                }

                // calculate || v^T E ||^2
                float res = 0.0f;
                float u_re, u_im;
                for (unsigned char c = 1; c < EAR_NUM_MICS; c++) {
                    u_re = 0.0f;
                    u_im = 0.0f;
                    for (unsigned char r = 0; r < EAR_NUM_MICS; r++) {
                        int pivot = i_f * stride_e_if + c * stride_e_c + r * 2;
                        u_re += v_re[r] * eig_vecs[pivot    ] - v_im[r] * eig_vecs[pivot + 1];
                        u_im += v_re[r] * eig_vecs[pivot + 1] + v_im[r] * eig_vecs[pivot    ];
                    }
                    res += u_re * u_re + u_im * u_im;
                }

                result[i_f * stride_r_if + iy * stride_r_iy+ ix] = res;
            }
        }
    }

    return 0;
}
