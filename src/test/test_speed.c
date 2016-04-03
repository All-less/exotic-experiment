#include <stdio.h>
#include <wiringPi.h>
#include <time.h>

#define SIZE_OF_ARRAY(array) ( sizeof( array ) / sizeof( array[0] ) ) 
#define OUT_TO_CONSOLE(msg) printf( msg );fflush(stdout);

int output_pins[] = {5, 0, 3, 4};
int input_pins[] = {7, 6, 2, 1};

int main(void) {
    
    int i, val;
    clock_t start, end;

    wiringPiSetup();
    OUT_TO_CONSOLE("wiringPiSetup() done.\n");

    /*
     * Initialize pins
     */
    for (i = 0; i < SIZE_OF_ARRAY(input_pins); i++) {
        pinMode(input_pins[i], INPUT);
        pullUpDnControl(input_pins[i], PUD_UP);
    }
    OUT_TO_CONSOLE("Configuring input pins done.\n");
    for (i = 0; i < SIZE_OF_ARRAY(output_pins); i++)
        pinMode(output_pins[i], OUTPUT);
    OUT_TO_CONSOLE("Configuing output pins done.\n");

    /*
     * Get the initial level
     */
    val = 1 - digitalRead(7);

    /*
     * Start test
     */
    start = clock();

    for (i = 0; i < 10000; i++) {
        digitalWrite(5, val);
        while (digitalRead(7) != val);
        val = 1 - val;
    }

    end = clock();
    printf("It takes %f sec to finish 10000 loops.\n", ((float)(end-start))/CLOCKS_PER_SEC);
    return 0;
}
