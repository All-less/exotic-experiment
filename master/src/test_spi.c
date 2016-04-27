#include <stdio.h>
#include "commons.h"


int fail;

void func(void) {
    
    uint8_t send_data, read_data, expected_data;
    uint64_t i;

    send_data = 0x06;
    read_data = bcm2835_spi_transfer(send_data);

    for (i = 0; i < 1000000; i++) {
        expected_data = send_data + 3;
        send_data += 1;
        read_data = bcm2835_spi_transfer(send_data);
        if (read_data != expected_data) {
            /*
            printf("FAILURE! Expected 0x%02X yet received 0x%02X.\n", expected_data, read_data); 
            */
            fail += 1; 
        } else {
            /*
            printf("SUCCESS");
            */
        }
    }
}


int main(void) {

    initPins();
    initSpi();
    
    printf("Sending 1,000,000 byte takes %f sec.\n", measureTime(func));
    printf("Fails %d times.\n", fail);    
    closeSpi();
    return 0;
}