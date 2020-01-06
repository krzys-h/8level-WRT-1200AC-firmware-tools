#!/usr/bin/python3
import sys
import struct

with open(sys.argv[1], "rb") as f:
	while True:
		HEADER_FMT = '>4sLLL'
		HEADER_SIZE = struct.calcsize(HEADER_FMT)
		header = f.read(HEADER_SIZE)
		if not header:
			break
		sig, ram_address, flash_address, data_len = struct.unpack(HEADER_FMT, header)
		print("File of type %s, in ram at 0x%08x, in flash at 0x%08x" % (sig.decode(), ram_address, flash_address))
		print("Data length: %d (0x%08x)" % (data_len, data_len))
		data = f.read(data_len)
		if sig.decode() != "w6cg":
			chk = 0
			for i in range(0, len(data), 2):
				a = struct.unpack('>H', data[i:i+2])[0]
				chk = (chk + a) % 65536
			print("Checksum: 0x%04x (%s)" % (chk, "ok" if chk == 0 else "FAIL!"))
		else:
			chk = 0
			for i in range(0, len(data)):
				a = data[i]
				chk = (chk + a) % 256
			print("Checksum: 0x%02x (%s)" % (chk, "ok" if chk == 0 else "FAIL!"))
