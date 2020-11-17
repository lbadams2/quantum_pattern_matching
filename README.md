# Quantum Pattern Matching

All code (including tests) is located in the `/src` directory.

## Install the Following Packages
`pip install numpy`
`pip install qiskit`

## Running the main program
```
python pattern_match.py <INPUT_STRING> <PATTERN>
```
To change the following settings, modify the options in `run_match()` at the bottom of pattern_match.py.
Make sure that the alphabet contains all letters in input string.
* `oracles` = `'many'` | `'single'`
* `diffuser`= `'gates'`| `'matrix'`
* `alphabet` = `('a', 'b', 'c' ... )` <- Enter your custom alphabet

## Running the tests
```
python test.py [ \* | <NUMBER OF CHARS IN PATTERN> | exact | exact \* ]
```
* `\*` runs wildcard tests
* `exact` runs tests using the latin alphabet for exact matches
