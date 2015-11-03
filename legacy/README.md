The directory contains an obsolete implementation of the python parser.
This implementation uses an ANTLR grammar and prooved to be:
- complicated
- practically impossible to cover all the cases (notably encodings and back
  slashes)
- fragile
- excessively large

The newer version of the parser does not use ANTLR anymore.
This obsolete code stays here for the reference purposes.
