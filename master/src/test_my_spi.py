from libbcm2835._bcm2835 import *
import sys
import random

print 'start'

if bcm2835_init() != 1:
    print "bcm2835_init failed."
    sys.exit(1)


rounds = 100

MOSI = RPI_GPIO_P1_19
MISO = RPI_GPIO_P1_21
SCLK = RPI_GPIO_P1_23
SSEL = RPI_GPIO_P1_24

bcm2835_gpio_fsel(MOSI, BCM2835_GPIO_FSEL_OUTP)
bcm2835_gpio_fsel(SCLK, BCM2835_GPIO_FSEL_OUTP)
bcm2835_gpio_fsel(SSEL, BCM2835_GPIO_FSEL_OUTP)
bcm2835_gpio_fsel(MISO, BCM2835_GPIO_FSEL_INPT)

# bcm2835_gpio_pud(SCLK, BCM2835_GPIO_PUD_UP)
# bcm2835_gpio_pud(SSEL, BCM2835_GPIO_PUD_UP)
# bcm2835_gpio_pud(MOSI, BCM2835_GPIO_PUD_UP)
bcm2835_gpio_pud(MISO, BCM2835_GPIO_PUD_UP)

bcm2835_gpio_write(SSEL, HIGH)
bcm2835_gpio_write(SCLK, LOW)

print 'init done'

def spi_transfer(data):
    read_data = 0
    bcm2835_gpio_write(SSEL, LOW)
    for i in range(8):
        send_bit = ((data << i) % 255) >> 7
        bcm2835_gpio_write(MOSI, HIGH if send_bit == 1 else LOW)
        bcm2835_gpio_write(SCLK, HIGH)
        read_bit = bcm2835_gpio_lev(MISO)
        bcm2835_gpio_write(SCLK, LOW)
        read_data = (read_data << 1) + read_bit
    bcm2835_gpio_write(SSEL, HIGH)
    return read_data


send_data = random.randint(0, 255)
read_data = spi_transfer(send_data)
print "Sent 0x%02X and received 0x%02X." % (send_data, read_data)
for i in range(rounds):
    delta = random.randint(0, 255)
    expected_data = (send_data + 3) % 0x100
    send_data = (send_data + delta) % 0x100
    read_data = spi_transfer(send_data)
    if read_data != expected_data:
        print "FAILURE! Expected 0x%02X yet received 0x%02X." % (expected_data, read_data) 
    else:
        pass
        # print "SUCCESS!"# Expected and received 0x%02X." % (expected_data,)
    # print "Send 0x%02X." % (send_data,)


bcm2835_close()
