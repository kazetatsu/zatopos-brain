#define NUM_MIC_CHS 6
#define SOUND_DEPTH 64
#define SOUND_BUF_LEN NUM_MIC_CHS * SOUND_DEPTH
#define SOUND_BUF_SIZE 2 * SOUND_BUF_LEN

#define USB_MAX_DATA_SIZE 60

struct receiver;
typedef struct receiver receiver_t;

receiver_t* receiver_malloc();
int receiver_init(receiver_t *receiver, unsigned char bus_no, unsigned char dev_addr);
void receiver_delete(receiver_t *receiver);
unsigned int receiver_receive(receiver_t *receiver);
void receiver_get_data(receiver_t *receiver, unsigned short *buf);
