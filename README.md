# Useful resources
* https://oldwiki.archive.openwrt.org/doc/techref/bootloader/realtek
* https://gist.github.com/vitali2y/79ca747be49f146971b5a7fa89a0a637
* https://github.com/jameshilliard/WECB-VZ-GPL/blob/master/rtl819x/bootcode/boot/init/rtk.h
* https://github.com/jameshilliard/WECB-VZ-GPL/blob/master/rtl819x/bootcode/boot/init/eth_tftpd.c

# Chipset
The device is using an RTL8197DN chipset, using a big-endian MIPS instruction set. According to my research, the actual MIPS core inside seems to be Lexra (to be verified).

# Bootloader
Pressing WPS and RESET at the same time during boot enters bootloader mode. The bootloader provides a simple command interface via UART, as well as allows for uploading updates via TFTP (see *./upload_update.sh*). The bootloader is entered automatically if booting fails (also serving as recovery mode).

When an update is uploaded via TFTP, it gets loaded into RAM at address 0x80500000. If the file is a proper update file, flashing begins automatically, otherwise the file just stays in RAM and can e.g. be flashed manually using the FLW command.

Confirmed working commands:
* ? - displays help
* FLW 80500000 10000 8000 - write 0x8000 bytes from 0x80500000 in RAM to 0x10000 in flash
* DB 80500000 128 - hexdump 128 bytes from RAM at 0x80500000
* IPCONFIG - displays IP address of the device for TFTP upload (192.168.1.6)

# UART
The device exposes an UART header with bootloader messages and linux shell. 38400 baud

Username: root
Password: whatever is configured as the admin password for the web panel (default: admin)

# Update file format
Everything big endian. See *./check_update.py* for a script that parses the update files, and *./make_header.py* for a script that appends an update header to a raw binary file

The update file is made out of the following blocks concatenated together:

| offset | size | description |
| ------ | ---- | ----------- |
| 0      | 4    | File type - see https://github.com/jameshilliard/WECB-VZ-GPL/blob/master/rtl819x/bootcode/boot/init/rtk.h for valid types. The device we have only seems to use "cr6c" for kernel and "r6cr" for rootfs (and possibly "boot" for bootloader?) |
| 4      | 4    | Load address in RAM (used only for kernel image it seems?) |
| 8      | 4    | Address in FLASH memory |
| 12     | 4    | Length of the data |
| 16     | *    | Data |

The data is checksummed - the 16-bit big endian sum of all bytes must be 0x0000 (unless you are flashing web files partition, which this device does not have - in that case the checksum is 8-bit). This is usually achieved by appending two bytes at the end.

# Flash memory layout
When the bootloader tries to load first looks at ~4 hardcoded addresses first, then proceeds to search the whole flash for a signature, which seems to indicate that the flash layout may be different on different devices. The data has an identical checksum check to the update files above.

See *./split_img.sh*

| start address | end address | header | description |
| ------------- | ----------- | ------ | ----------- |
| 0x00000000 | 0x00006000 | -          | Bootloader code |
| 0x00006000 | 0x00008000 | H601 (?)   | Hardware config (MAC address etc.) |
| 0x00008000 | 0x00010000 | COMPDS (?) | Default config |
| 0x00010000 | 0x00018000 | COMPCS (?) | Current config |
| 0x00018000 | 0x00138000 | Update header for cr6c | Linux kernel, prefixed with a header identical to the update header format |
| 0x00138000 | 0x00327002 | squashfs filesystem header, starting with hsqs | Root filesystem. The last two bytes are added for the checksum. |
| 0x00327002 | 0x00400000 | -          | 0xFF 0xFF 0xFF 0xFF ... |
