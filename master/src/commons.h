#include <stdio.h>
#include <wiringPi.h>
#include <time.h>
#include <string.h>
#include <stdlib.h>
#include <errno.h>
#include <bcm2835.h>


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


/*
 * Measure time spent in executing 'func'.
 * Return time in unit 'second'.
 */
float measureTime(void (*func)(void)){

    clock_t start, end;
    start = clock();
    func();
    end = clock();
    
    return (float)(end-start)/CLOCKS_PER_SEC;
}


/*
 * Initialize and setup spi registers.
 * It should be called with closeSpi().
 */
void initSpi(void) {
    if (!bcm2835_init()) {
      printf("bcm2835_init failed. Are you running as root??\n");
    }

    if (!bcm2835_spi_begin()) {
      printf("bcm2835_spi_begin failedg. Are you running as root??\n");
    }

    bcm2835_spi_setBitOrder(BCM2835_SPI_BIT_ORDER_MSBFIRST);
    bcm2835_spi_setDataMode(BCM2835_SPI_MODE0);
    bcm2835_spi_setClockDivider(BCM2835_SPI_CLOCK_DIVIDER_64);
    bcm2835_spi_chipSelect(BCM2835_SPI_CS0);
    bcm2835_spi_setChipSelectPolarity(BCM2835_SPI_CS0, LOW);
}


/*
 * End spi setup.
 * It should be called with initSpi().
 */
void closeSpi(void) {
    bcm2835_spi_end();
    bcm2835_close();
}


/*
 * Get error message from errno.h.
 */
char *getError(void) {
    return strerror(errno);
}
