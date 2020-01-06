#!/usr/bin/python3
import sys
import struct

source = sys.argv[1]
target = sys.argv[2]
sig = sys.argv[3]
ram_address = int(sys.argv[4], 16)
flash_address = int(sys.argv[5], 16)
assert len(sig.encode()) == 4

data = open(source, "rb").read()

with open(target, "wb") as f:
	f.write(struct.pack('4s', sig.encode()))
	f.write(struct.pack('>l', ram_address))
	f.write(struct.pack('>l', flash_address))
	f.write(struct.pack('>l', len(data)))
	f.write(data)
