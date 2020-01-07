#!/bin/bash
# Split a flash image into separate files

# sudo flashrom -p ch341a_spi -r router.bin
dd if=router.bin of=boot.bin           bs=1                    count=$((  0x6000))
dd if=router.bin of=hwconfig.bin       bs=1 skip=$((  0x6000)) count=$((  0x2000))
dd if=router.bin of=config_default.bin bs=1 skip=$((  0x8000)) count=$((  0x8000))
dd if=router.bin of=config_current.bin bs=1 skip=$(( 0x10000)) count=$((  0x8000))
dd if=router.bin of=kernel.bin         bs=1 skip=$(( 0x18000)) count=$((0x120000))
dd if=router.bin of=rootfs.bin         bs=1 skip=$((0x138000)) count=$((0x1ef002))
