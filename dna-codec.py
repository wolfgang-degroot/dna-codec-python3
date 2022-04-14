#!/usr/bin/env python3
"""Encode or decode any string or file to a sequence of DNA, and vice versa"""
import sys

__author__ = "Wolfgang de Groot"
__version__ = "1.0.3"
__license__ = "MIT"

# * Encoders

def hex_to_dna(hex: hex) -> str:
	"""Encodes Hexidecimal to DNA"""
	try:
		base10 = int(hex, 16) # ? Base 16 to base 10
	except ValueError:
		sys.exit("Invalid hexidecimal.")
	dna = ""
	while base10 > 0: # ? Base 10 to DNA (base 4)
		offset = base10 % 4
		dna = "ACGT"[offset] + dna
		base10 = base10 // 4
	return dna


def str_to_dna(s: str) -> str:
	"""Encodes a string to DNA"""
	hex = s.encode("utf_8").hex()
	return hex_to_dna(hex)

# * Decoders

def dna_to_hex(dna: str) -> hex:
	"""Decodes DNA to Hexidecimal"""
	nucleotides = ["A", "C", "G", "T"]
	base4 = ""
	for char in dna:
		u = char.upper()
		if u not in nucleotides:
			continue # ? Skip non-DNA characters
		base4 += str(nucleotides.index(u))
	return hex(int(base4, 4)) if base4 != "" else "0"


def dna_to_str(dna: str) -> str:
	"""Decodes DNA back to a string"""
	hex = dna_to_hex(dna)
	try:
		byte = bytes.fromhex(hex[2:])
	except ValueError:
		sys.exit("Incomplete input.")
	return byte.decode("utf_8", "ignore")

# * Function

def help() -> None:
	self = sys.argv[0]
	print("Usage: %s <input> <args>"%self)
	print("\t--encode: -- encode string to DNA [default]")
	print("\t--decode: -- decode DNA to string")
	print("\t--string: -- Use a string as input  [default]")
	print("\t--file: ---- Use a file instead of a string")
	print("\t--hex: ----- The data input is hexidecimal")
	print("\t--strict: -- Do not pad the input if characters are missing")
	print("\t--help: ---- Print this help message")
	print("Example: %s \"Biology is actually my least favorite subject\" --encode --string"%self)
	print("Example: %s input.txt --encode --file"%self)
	print("Example: %s CAGACGCCCGTACGTACGTTAGAC --decode --string"%self)


def main():
	flag = {"decode": False, "string": True, "hex": False, "strict": False}
	if len(sys.argv) == 1:
		# ? No arguments given.
		data = input("Input a string to encode into DNA: > ")
		flag["string"] = True
	elif len(sys.argv) == 2 and sys.argv[1] == "--help":
		sys.exit(help())
	else:
		# ? Arguments given, and the first is not --help
		data = sys.argv[1]
		for arg in sys.argv[2:]:
			sys.exit(help()) if arg == "--help" else None
			flag["decode"]	= True	if arg == "--decode" else flag["decode"]
			flag["decode"]	= False	if arg == "--encode" else flag["decode"]  # *
			flag["string"]	= False	if arg == "--file"	 else flag["string"]
			flag["string"]	= True	if arg == "--string" else flag["string"]  # *
			flag["hex"]		= True	if arg == "--hex"	 else flag["hex"]
			flag["strict"]	= True	if arg == "--strict" else flag["strict"]

	# * Execution
	if flag["string"]:
		payload = data
	else:
		with open(data, "r") as file:
			try:
				payload = file.read().replace("\n", "")
			except UnicodeDecodeError:
				sys.exit("Invalid file encoding. Only UTF-8 is supported.")
	if flag["decode"]:
		# ? Decoding
		cleaned = "".join([i for i in payload if i in "ACGT"])
		# ! Pad strings that are too short if --strict is not used
		cleaned += "A" * (4 - len(cleaned) % 4) if not flag["strict"] else ""
		print(dna_to_hex(cleaned) if flag["hex"] else dna_to_str(cleaned))
	else:
		# ? Encoding
		print(hex_to_dna(payload) if flag["hex"] else str_to_dna(payload))

if __name__ == "__main__":
	sys.exit(main())
