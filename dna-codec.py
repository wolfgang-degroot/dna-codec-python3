#!/usr/bin/env python3
"""Encode or decode any string or UTF-8 encoded file to a sequence of DNA, and vice versa"""
import sys

__author__ = "Wolfgang de Groot"
__version__ = "1.2.1"
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


def str_to_dna(s: str, codec: str = "utf_8") -> str:
	"""Encodes a string to DNA"""
	hex = s.encode(codec).hex()
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


def dna_to_str(dna: str, codec: str = "utf_8") -> str:
	"""Decodes DNA back to a string"""
	hex = dna_to_hex(dna)
	try:
		byte = bytes.fromhex(hex[2:])
	except ValueError:
		sys.exit("Incomplete input.")
	return byte.decode(codec, "ignore")

# * Function

def clean(input: str, strict: bool = False) -> str:
	"""Cleans the input string for DNA decoding"""
	output = ""
	for char in input:
		if char in "ACGT":
			output += char
		elif strict:
			output += "A"
	output += "A" * (4 - len(output) % 4)
	print(output)
	return output

def help() -> None:
	self = sys.argv[0]
	print("Usage: %s <input> <args>"%self)
	print("\t--encode --------- encode string to DNA [default]")
	print("\t--decode --------- decode DNA to string")
	print("\t--codec:<codec> -- Set which standard encoder to use")
	print("\t--string --------- Use a string as input  [default]")
	print("\t--file ----------- Use a file instead of a string")
	print("\t--strict --------- Pad invalid characters when decoding rather than skipping")
	print("\t--help ----------- Print this help message")
	print("Example: %s \"Biology is actually my least favorite subject\" --encode --string"%self)
	print("Example: %s input.txt --encode --file"%self)
	print("Example: %s CAGACGCCCGTACGTACGTTAGAC --decode --string"%self)

def flags(default: bool = False) -> tuple:
	"""Returns a tuple of flags"""
	flag = {"decode": False, "string": True, "strict": False, "codec": "utf_8"}
	if default:
		return flag
	for arg in sys.argv[1:]:
		sys.exit(help()) if arg == "--help" else None
		flag["decode"]	= True	if arg == "--decode" else flag["decode"]
		flag["decode"]	= False	if arg == "--encode" else flag["decode"]  # *
		flag["string"]	= False	if arg == "--file"	 else flag["string"]
		flag["string"]	= True	if arg == "--string" else flag["string"]  # *
		flag["strict"]	= True	if arg == "--strict" else flag["strict"]
		if arg[:8] == "--codec:":
			import codecs
			codec = arg[8:]
			try:
				codecs.lookup(codec)
			except LookupError:
				sys.exit("Unknown codec \"%s\"."%codec)
			else:
				flag["codec"] = codec
	return flag


def main():
	if len(sys.argv) == 1:
		# ? No arguments given.
		data = input("Input a UTF-8 string to encode into DNA: > ")
		flag = flags(default=True)
	else:
		data = sys.argv[1]
		flag = flags()

	if flag["string"]:
		if flag["decode"]:
			print(dna_to_str(clean(data, flag["strict"]), flag["codec"]))
		else:
			print(str_to_dna(data, flag["codec"]))
	else:
		with open(data, "r") as file:
			try:
				data = file.read()
			except UnicodeDecodeError:
				sys.exit("Invalid file encoding. Only UTF-8 is supported.")
		if flag["decode"]:
			print(dna_to_str(clean(data, flag["strict"]), flag["codec"]))
		else:
			print(str_to_dna(data, flag["codec"]))

if __name__ == "__main__":
	sys.exit(main())
