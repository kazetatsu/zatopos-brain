// SPDX-FileCopyrightText: 2024 ShinagwaKazemaru
// SPDX-License-Identifier: MIT License

#ifndef _ZATOPOS_BRAIN_CONSTS_H
#define _ZATOPOS_BRAIN_CONSTS_H

#define EAR_NUM_MICS 6
#define EAR_WINDOW_LEN 64
#define EAR_SAMPLING_RATE 2000
#define EAR_BUFFER_LEN EAR_NUM_MICS * EAR_WINDOW_LEN
#define EAR_BUFFER_SIZE 2 * EAR_BUFFER_LEN
#define EAR_WINDOW_TIME 64 / 2000

#endif