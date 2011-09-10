#! /bin/bash
ls -1 *.flac > playlist
mkfifo aufifo
aplay -B 2000000 -t raw -c 2 -f S16_LE -r 44100 aufifo &> /tmp/aplayfifo.log &
mplayer -ao pcm:nowaveheader:file=aufifo -playlist playlist 
