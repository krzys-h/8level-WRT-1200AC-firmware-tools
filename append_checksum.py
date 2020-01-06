#!/usr/bin/python3
import sys
import struct

source = sys.argv[1]
target = sys.argv[2]

with open(source, "rb") as f:
	data = f.read()
	chk = 0
	for i in range(0, len(data), 2):
		a = struct.unpack('>H', data[i:i+2])[0]
		chk = (chk + a) % 65536
	with open(target, "wb") as f2:
		f2.write(data)
		f2.write(struct.pack('>H', (0x10000 - chk) % 0x10000))
