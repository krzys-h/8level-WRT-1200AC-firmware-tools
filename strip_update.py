#!/usr/bin/python3
import sys
import struct

# Strips trailing zero bytes at the end of a single update file (e.g. if coming from a flash dump)

source = sys.argv[1]
target = sys.argv[2]

with open(source, "rb") as f:
	HEADER_FMT = '>4sLLL'
	HEADER_SIZE = struct.calcsize(HEADER_FMT)
	header = f.read(HEADER_SIZE)
	sig, ram_address, flash_address, data_len = struct.unpack(HEADER_FMT, header)
	print("Stripping to length: %d (0x%08x)" % (data_len, data_len))
	data = f.read(data_len)
	with open(target, "wb") as f2:
		f2.write(header)
		f2.write(data)
	trailing_data = f.read()
	print("Removed %d (0x%08x) bytes" % (len(trailing_data), len(trailing_data)))
	warn = False
	for byte in trailing_data:
		if byte != 0x00 and byte != 0xff:
			warn = True
	if warn:
		print("WARNING! Trailing data contains not empty bytes!!")
