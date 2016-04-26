from libbcm2835._bcm2835 import *


if bcm2835_init() != 1:
    print 'bcm2835_init() failed!'


bcm2835_gpio_fsel(RPI_GPIO_P1_23, BCM2835_GPIO_FSEL_OUTP);
while True:
    bcm2835_gpio_write(RPI_GPIO_P1_23, HIGH)
    bcm2835_delay(500)
    bcm2835_gpio_write(RPI_GPIO_P1_23, LOW)
    bcm2835_delay(500)


bcm2835_close()
