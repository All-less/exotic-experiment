from libbcm2835._bcm2835 import *
import sys
import random


rounds = 100


if bcm2835_init() != 1:
    print "bcm2835_init failed."
    sys.exit(1)
if bcm2835_spi_begin() != 1:
    print "bcm2835_spi_begin failed."
    sys.exit(1)


bcm2835_spi_setBitOrder(BCM2835_SPI_BIT_ORDER_MSBFIRST)
bcm2835_spi_setDataMode(BCM2835_SPI_MODE0)
bcm2835_spi_setClockDivider(BCM2835_SPI_CLOCK_DIVIDER_32)
bcm2835_spi_chipSelect(BCM2835_SPI_CS0)
bcm2835_spi_setChipSelectPolarity(BCM2835_SPI_CS0, LOW)


send_data = 0x23
read_data = bcm2835_spi_transfer(send_data)
for i in range(rounds):
    delta = random.randint(0, 255)
    expected_data = (send_data + 4) % 0x100
    send_data = (send_data + delta) % 0x100
    read_data = bcm2835_spi_transfer(send_data)
    if read_data != expected_data:
        print "FAILURE! Expected 0x%02X yet received 0x%02X." % (expected_data, read_data) 
        # break
    else:
        print "SUCCESS!"


bcm2835_spi_end()
bcm2835_close()
