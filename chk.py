#!/usr/bin/python
import struct
import sys

# Calculate a checksum of a range of the file

start = int(sys.argv[2], 16)
end = int(sys.argv[3], 16)

s = 0
with open(sys.argv[1], "rb") as f:
	f.read(start)
	loc = start
	while loc < end:
		b = f.read(2)
		if not b:
			break
		a = struct.unpack('>H', b)[0]
		s = (s + a) % 65536
		loc += 2
print(hex(s))
