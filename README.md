# Exotic Experiment
Course project for *Embedded System*.

## Note

1. 树莓派端的输入（相对于树莓派而言）接口需要接上拉电阻，在[wiringPi](http://wiringpi.com/)中可通过`gpio mode 7 up`实现。

2. Linux下下载bit文件至FPGA开发板工具下载地址为https://reference.digilentinc.com/digilent_adept_2#software_downloads

3. 下载工具命令包括

	```
	djtgcfg
	dadutil
	dsumecfg
	```

4. libbcm2835安装说明

libbcm2835是树莓派GPIO操作库的python封装，其安装中需注意生成so并添加链接目录。

```bash
# do this in <root of bcm2835>/src
$ gcc -shared -o libbcm2835.so -fPIC bcm2835.c
$ cp libbcm2835.so /usr/local/lib

LD_LIBRARY_PATH=/usr/local/lib
export LD_LIBRARY_PATH
sudo ldconfig
```