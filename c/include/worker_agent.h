#ifndef _WORKER_AGENT_C
#define _WORKER_AGENT_C

#include "sound.h"

#define USB_MAX_DATA_SIZE 60

struct worker_agent;
typedef struct worker_agent worker_agent_t;

worker_agent_t* worker_agent_malloc();
int worker_agent_init(worker_agent_t *agent, unsigned char bus_no, unsigned char dev_addr);
void worker_agent_delete(worker_agent_t *agent);
unsigned int worker_agent_receive(worker_agent_t *agent);
void worker_agent_copy_sound(worker_agent_t *agent, unsigned short *dst);

#endif