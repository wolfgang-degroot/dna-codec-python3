#	Wolfgang's DNA Codec
##	Cultivate your data!

### Usage
```bash
dna-codec.py <input> <args>
```
| Flag				| Description			| Default	|
| -----------------	| ---------------------	| ---------	|
| --encode			| *Encode*				| **Yes**	|
| --decode			| *Decode*				| No		|
| --codec:`<codec>`	| Which	encoder to use?	| `utf_8`	|
| --string			| **Input a *string***	| **Yes**	|
| --file			| Input a *file*		| No		|
| --strict			| Don't skip bad data	| No		|
| --help			| Display some help		| No		|

### Examples
Encode a string:
`dna-codec.py "Hello, world!" --encode`

Decode a string:
`dna-codec.py CCCACGGACGCCAGAACACTCGACCGTCCGCC --decode`

Decode a file:
`dna-codec.py dna.txt --decode --file`

Encode a file and store the output:
`dna-codec.py data.txt --encode --file > output.txt`

----------------

```CGAGCTGCAGAACCCTCGTTCGTACGCGCGCTCGACCGTGCGCTAGAACGCACGCCAGAACACTCTAGCGTTCGTTCTCA```