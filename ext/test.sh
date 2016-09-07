#!/bin/bash

cd src
gcc -shared -o libbcm2835.so -fPIC bcm2835.c
cp libbcm2835.so /usr/local/lib
LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib
export LD_LIBRARY_PATH
ldconfig
