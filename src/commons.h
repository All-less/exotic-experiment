#include <stdio.h>
#include <wiringPi.h>
#include <time.h>
#include <string.h>
#include <stdlib.h>
#include <errno.h>
#include <wiringPiSPI.h>


#define SIZE_OF_ARRAY(array) ( sizeof( array ) / sizeof( array[0] ) ) 
#define OUT_TO_CONSOLE(msg) printf( msg );fflush(stdout);


int output_pins[] = {5, 0, 3, 4};
int input_pins[] = {7, 6, 2, 1};


/*
 * Initialize wiringPi setup and pin modes.
 */
void initPins(void) {

    int i;

    wiringPiSetup();
    OUT_TO_CONSOLE("Setting up wiringPi done.\n");

    for (i = 0; i < SIZE_OF_ARRAY(input_pins); i++) {
        pinMode(input_pins[i], INPUT);
        pullUpDnControl(input_pins[i], PUD_UP);
    }
    OUT_TO_CONSOLE("Configuring input pins done.\n");
    
    for (i = 0; i < SIZE_OF_ARRAY(output_pins); i++)
        pinMode(output_pins[i], OUTPUT);
    OUT_TO_CONSOLE("Configuing output pins done.\n");
}


float measureTime(void (*func)(void)){

    clock_t start, end;
    start = clock();
    func();
    end = clock();
    
    return (float)(end-start)/CLOCKS_PER_SEC;
}


/*
 * Attempt to initialize SPI port. It will halt the program
 * if the initialization fails.
 *
 * The parameter 'freq' has unit MHz. 
 */
void initSpi(int freq) {

    if (wiringPiSPISetup(0, freq * 100000) < 0) {
        printf("SPI Setup failed: %s\n", strerror (errno));
        exit(0);
    }
}


char *getError(void) {
    return strerror(errno);
}
