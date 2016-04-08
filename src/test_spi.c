#include <stdio.h>
#include <wiringPiSPI.h>
#include "commons.h"


void func(void) {
    
    int i;
    unsigned char data = 0;

    for (i = 0; i < 10000; i++) {
        wiringPiSPIDataRW(0, &data, 1);
    }
}


int main(void) {
    
    int i;
    unsigned char data;

    initPins();

    initSpi(1);
    
    data = 10;
    for (i = 0; i < 100; i++) {
        if (wiringPiSPIDataRW(0, &data, 1) == -1) {
            printf("SPI error occurs: %s\n", getError());
        } else {
            printf("Received data %u\n", data);
        }
    }
    
    return 0;
}
