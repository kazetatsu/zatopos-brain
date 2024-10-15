// SPDX-FileCopyrightText: 2024 ShinagwaKazemaru
// SPDX-License-Identifier: MIT License

/**
 * MUSIC algorithm
 */

#ifndef _MUSICAL_H
#define _MUSICAL_H

#include "consts.h"

struct musical;
typedef struct musical musical_t;

musical_t* musical_malloc(void);
unsigned int musical_init(musical_t* music);
void musical_delete(musical_t* music);
unsigned int musical_set_frequency(musical_t* music, float* freq, int len);
unsigned int musical_set_resolution(musical_t* music, int x, int y);
unsigned int musical_set_distance(musical_t* music, float x, float y);
unsigned int musical_search(musical_t* music, float *E, float *result);

#endif