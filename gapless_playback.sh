#! /bin/bash
ls -1 *.flac > playlist
mkfifo aufifo
aplay -t raw -c 2 -f S16_LE -r 44100 aufifo &> /tmp/aplayfifo.log &
gmplayer -ao pcm:nowaveheader:file=aufifo -playlist playlist 
