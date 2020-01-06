#!/bin/sh

# Create files that can be uploaded over TFTP
# TODO: check rootfs RAM location

./strip_update.py kernel.bin kernel.web
./check_update.py kernel.web
./make_header.py rootfs.bin rootfs.web r6cr 0x00000000 0x138000
./check_update.py rootfs.web

