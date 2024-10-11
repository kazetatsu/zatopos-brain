// #include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <libusb.h>

#include "ear_agent.h"

struct ear_agent{
    libusb_context *ctx;
    libusb_device *device;
    libusb_device_handle *handle;
    unsigned short *sound_buf;
};

ear_agent_t *ear_agent_malloc(void) {
    return calloc(1, sizeof(ear_agent_t));
}

unsigned int ear_agent_init(ear_agent_t *agent, unsigned char bus_no, unsigned char dev_addr) {
    libusb_context *ctx;
    libusb_device **list;
    struct libusb_device_descriptor desc;

    libusb_device *device;
    libusb_device_handle *handle;

    libusb_init(&ctx);

    int list_len = libusb_get_device_list(ctx, &list);

    for (unsigned char i = 0; i < list_len; i++) {
        device = list[i];
        unsigned char bus  = libusb_get_bus_number(device);
        unsigned char addr = libusb_get_device_address(device);

        if (bus == bus_no && addr == dev_addr) {
            int ret = libusb_open(device, &handle);  // Internally, this function decrement the reference counter of agent->device when success

            if (ret == 0) {
                agent->ctx = ctx;
                agent->device = device;
                agent->handle = handle;
                agent->sound_buf = (unsigned short*)malloc(SOUND_BUF_SIZE);
                libusb_free_device_list(list, 1);
            } else {
                libusb_free_device_list(list, 1);
                libusb_exit(ctx);
            }
            return (unsigned int)(-ret);
        }
    }

    libusb_free_device_list(list, 1);
    libusb_exit(ctx);
    return (unsigned int)(-LIBUSB_ERROR_NO_DEVICE);
}

void ear_agent_delete(ear_agent_t *agent) {
    if (agent->sound_buf != NULL) {
        free(agent->sound_buf);
    }

    if (agent->ctx != NULL) {
        libusb_close(agent->handle); // Internally, this function decrement the reference counter of agent->device
        libusb_exit(agent->ctx);
    }

    free(agent);
}

unsigned int ear_agent_receive(ear_agent_t *agent) {
    unsigned int ret = 0;

    int ret_intf = libusb_claim_interface(agent->handle, 0);
    if (ret_intf != 0) {
        ret |= (unsigned int)(-1 * ret_intf);
        return ret;
    }

    int actual_length;

    // Send commad to ask worker to send sound buffer
    unsigned char cmd[] = {0x01};
    int ret_cmd = libusb_bulk_transfer(agent->handle, LIBUSB_ENDPOINT_OUT | 1, cmd, 1, &actual_length, 1000);
    if (ret_cmd != 0) {
        libusb_release_interface(agent->handle, 0);

        ret |= 0x01 << 24;
        ret |= (unsigned int)(-1 * ret_cmd) << 16;
        ret |= actual_length;
        return ret;
    }

    // Receive sound buffer
    unsigned char *buf = (unsigned char*)agent->sound_buf;
    unsigned short offset = 0;
    do {
        unsigned int data_size = SOUND_BUF_SIZE - offset;
        if (data_size > USB_MAX_DATA_SIZE) {
            data_size = USB_MAX_DATA_SIZE;
        }

        int ret_data = libusb_bulk_transfer(
            agent->handle,
            LIBUSB_ENDPOINT_IN | 1,
            buf,
            data_size,
            &actual_length,
            2000
        );

        if (ret_data != 0) {
            libusb_release_interface(agent->handle, 0);

            ret |= 0x03 << 24;
            ret |= (unsigned int)(-1 * ret_data) << 16;
            ret |= offset + actual_length;
            return ret;
        }

        // uint16_t *dat = (uint16_t*)buf;
        // if (dat[0] & 0xf000) {
        // }

        buf += data_size;
        offset += data_size;
    } while (offset < SOUND_BUF_SIZE);

    libusb_release_interface(agent->handle, 0);

    return 0;
}

unsigned int ear_agent_copy_sound(ear_agent_t *agent, unsigned short *dst) {
    memcpy(dst, agent->sound_buf, SOUND_BUF_SIZE);
    return 0;
}
