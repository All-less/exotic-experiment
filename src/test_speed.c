/*
 * The program tests transfering spped between Sword and Rpi.
 * It measures as follows:
 *
 * 1. It write 1 to an port 5.
 * 2. On FPGA, the port 5 is directly linked to port 7.
 * 3. It reads signal from port 7. 
 * 4. If it get 1, then it will write 0 to port 5 and repeat.
 * 5. After 10000 loops, the total time will be calculated.
 *
 */
#include <wiringPi.h>
#include "commons.h"


void func() {
    
    int val, i;

    val = 1 - digitalRead(7);

    for (i = 0; i < 10000; i++) {
        digitalWrite(5, val);
        while (digitalRead(7) != val);
        val = 1 - val;
    }
}


int main(void) {

    initPins();

    printf("It takes %f sec to finish 10000 loops.\n", measureTime(func));

    return 0;
}
