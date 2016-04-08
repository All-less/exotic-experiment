/*
 *
 */
#include <stdio.h>
#include <wiringPi.h>
#include "commons.h"


int main(void) {

    int i;
    unsigned int start, end, total;
    
    initPins();

    for (i = 0, total = 0; i < 100; i++) {
        start = millis();
        delay(100);
        end = millis();
        total += end - start;
    }
    printf("Delaying 100ms causes %ums delay.\n", total/100);

    for (i = 0, total = 0; i < 100; i++) {
        start = micros();
        delayMicroseconds(100);
        end = micros();
        total += end - start;
    }
    printf("Delaying 100us causes %uus delay.\n", total/100);
    return 0;
}
