raspivid -t 0 -w 960 -h 540 -fps 25 -b 500000 -vf -hf -o - | ffmpeg -i - -vcodec copy -an -r 25 -f flv -metadata streamName=test tcp://10.214.128.116:6666
