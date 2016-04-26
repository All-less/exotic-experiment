SRCDIR = src
BINDIR = bin

SRCS = test_speed.c test_clock.c test_spi.c  
BINS = $(SRCS:.c=)

CC = gcc
CFLAGS = -lwiringPi -Wall -lbcm2835 

# all : $(BINS);

% : $(SRCDIR)/%.c
	$(CC) $< -o $(BINDIR)/$@ $(CFLAGS)
