SRCDIR = src
BINDIR = bin

SRCS = test_speed.c test_clock.c test_spi.c  
BINS = $(SRCS:.c=.out)

CC = gcc
CFLAGS = -lwiringPi -Wall 

# all : $(BINS);

%.out : $(SRCDIR)/%.c
	$(CC) $< -o $(BINDIR)/$@ $(CFLAGS)
