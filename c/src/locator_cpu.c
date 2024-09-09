#include <stdlib.h>

#include "locator.h"

struct locator {
    int rx;
    int ry;
    float lx;
    float ly;
};

locator_t* locator_malloc(void) {
    return (locator_t*)malloc(sizeof(locator_t));
}

unsigned int locator_init(locator_t* locator) {
    return 0;
}

void locator_delete(locator_t* locator) {
    free(locator);
}

unsigned int locator_set_frequency(locator_t* locator, float* freq, int len) {
    return 0;
}

unsigned int locator_set_resolution(locator_t* locator, int x, int y) {
    locator->rx = x;
    locator->ry = y;
    return 0;
}

unsigned int locator_set_distance(locator_t* locator, float x, float y) {
    locator->lx = x;
    locator->ly = y;
    return 0;
}

unsigned int locator_locate(locator_t* locator, float ***E_re, float ***E_im, float **result) {
    for (int ix = 0; ix < locator->rx; ix++) {
        for (int iy = 0; iy < locator->ry; iy++) {
            result[ix][iy] = 0.0f;
        }
    }
    return 0;
}
