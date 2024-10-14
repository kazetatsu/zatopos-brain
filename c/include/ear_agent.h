// SPDX-FileCopyrightText: 2024 ShinagwaKazemaru
// SPDX-License-Identifier: MIT License

#ifndef _WORKER_AGENT_C
#define _WORKER_AGENT_C

#include "consts.h"

#define USB_MAX_DATA_SIZE 60

struct ear_agent;
typedef struct ear_agent ear_agent_t;

ear_agent_t* ear_agent_malloc();
unsigned int ear_agent_init(ear_agent_t *agent, unsigned char bus_no, unsigned char dev_addr);
void ear_agent_delete(ear_agent_t *agent);
unsigned int ear_agent_receive(ear_agent_t *agent, unsigned char* sound_buf, unsigned char num_windows);

#endif