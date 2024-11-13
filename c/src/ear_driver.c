// SPDX-FileCopyrightText: 2024 ShinagwaKazemaru
// SPDX-License-Identifier: MIT License

// #include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <libusb.h>

#include "ear_driver.h"

struct ear_driver{
    libusb_context *ctx;
    libusb_device *device;
    libusb_device_handle *handle;
};

ear_driver_t *ear_driver_malloc(void) {
    return calloc(1, sizeof(ear_driver_t));
}

unsigned int ear_driver_init(ear_driver_t *driver, unsigned char bus_no, unsigned char dev_addr) {
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
            int ret = libusb_open(device, &handle);  // Internally, this function decrement the reference counter of driver->device when success

            if (ret == 0) {
                driver->ctx = ctx;
                driver->device = device;
                driver->handle = handle;
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

void ear_driver_delete(ear_driver_t *driver) {
    if (driver->ctx != NULL) {
        libusb_close(driver->handle); // Internally, this function decrement the reference counter of driver->device
        libusb_exit(driver->ctx);
    }

    free(driver);
}

unsigned int ear_driver_receive(ear_driver_t *driver, unsigned char* sound_buf, unsigned char num_windows) {
    unsigned int ret = 0;
    int actual_length;
    unsigned short offset;
    unsigned char cmd[2] = {0x01, num_windows};
    unsigned char stat;
    unsigned char *buf = sound_buf;

    int ret_intf = libusb_claim_interface(driver->handle, 0);
    if (ret_intf != 0) {
        ret |= (unsigned int)(-1 * ret_intf);
        return ret;
    }

    // Send commad to ask worker to send sound buffer
    int ret_cmd = libusb_bulk_transfer(driver->handle, LIBUSB_ENDPOINT_OUT | 1, cmd, 2, &actual_length, 1000);
    if (ret_cmd != 0) {
        libusb_release_interface(driver->handle, 0);

        ret |= 0x01 << 28;
        ret |= (unsigned int)(-1 * ret_cmd) << 20;
        ret |= actual_length;
        return ret;
    }

    for(unsigned int i = 0; i < num_windows; i++) {
        // Receive sound
        offset = 0;
        do {
            int ret_data = libusb_bulk_transfer(
                driver->handle,
                LIBUSB_ENDPOINT_IN | 1,
                buf,
                USB_MAX_DATA_SIZE,
                &actual_length,
                2000
            );

            if (ret_data != 0) {
                libusb_release_interface(driver->handle, 0);

                ret |= 0x02 << 28;
                ret |= (unsigned int)(-1 * ret_data) << 20;
                ret |= i << 12;
                ret |= offset + actual_length;
                return ret;
            }

            buf += USB_MAX_DATA_SIZE;
            offset += USB_MAX_DATA_SIZE;
        } while (offset < EAR_WINDOW_BUF_SIZE);
    }

    libusb_release_interface(driver->handle, 0);

    return 0;
}
