// SPDX-FileCopyrightText: 2024 ShinagwaKazemaru
// SPDX-License-Identifier: MIT License

#ifndef _EAR_DRIVER_C
#define _EAR_DRIVER_C

#include "consts.h"

#define USB_MAX_DATA_SIZE 64

struct ear_driver;
typedef struct ear_driver ear_driver_t;

ear_driver_t* ear_driver_malloc();
unsigned int ear_driver_init(ear_driver_t *driver, unsigned char bus_no, unsigned char dev_addr);
void ear_driver_delete(ear_driver_t *driver);
unsigned int ear_driver_receive(ear_driver_t *driver, unsigned char* sound_buf, unsigned char num_windows);

#endif