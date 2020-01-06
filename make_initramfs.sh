#!/bin/bash
# mksquashfs /mnt/ramdisk/router $1 -b 131072 -comp lzma
./append_checksum.py $1 $1.bin
./make_header.py $1.bin $1.web r6cr 0x00000000 0x138000
./check_update.py $1.web
