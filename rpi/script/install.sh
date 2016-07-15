#!/bin/bash

# check for root privilege
if [ "$(whoami)" != "root" ]; then
	echo "Error! Root privilege required for this script."
	exit 1
fi

# install third-party packages
cd ../third-party

# install digilent adept tool for downloading bit file
dpkg -i "$(ls | grep digilent | grep deb)"

# install bcm2835 library for operating GPIO
BCM2835="$(ls | grep bcm2835- | sed 's/.tar.gz//')"
tar zxf $BCM2835.tar.gz
cd $BCM2835
./configure
make
make check
make install
cd src
# add shared lib
gcc -shared -o libbcm2835.so -fPIC bcm2835.c
cp libbcm2835.so /usr/local/lib
LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib
export LD_LIBRARY_PATH
ldconfig
cd ../..
rm -rf $BCM2835
# install python binding
cd py-libbcm2835
python setup.py install
cd ..


