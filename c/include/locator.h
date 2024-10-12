// SPDX-FileCopyrightText: 2024 ShinagwaKazemaru
// SPDX-License-Identifier: MIT License

/**
 * MUSIC algorithm
 */

#ifndef _LOCATE_H
#define _LOCATE_H

#include "consts.h"

struct locator;
typedef struct locator locator_t;

locator_t* locator_malloc(void);
unsigned int locator_init(locator_t* locator);
void locator_delete(locator_t* locator);
unsigned int locator_set_frequency(locator_t* locator, float* freq, int len);
unsigned int locator_set_resolution(locator_t* locator, int x, int y);
unsigned int locator_set_distance(locator_t* locator, float x, float y);
unsigned int locator_locate(locator_t* locator, float *E, float *result);

#endif