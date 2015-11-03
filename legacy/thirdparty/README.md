The obsolete version of the python parser uses an ANTLR grammar. The generated
code for the grammar is C and that code in turn requires a C-library.
The directory below stores the required version of the ANTLR C run-time library.
That version of the library is not officially supported anymore and it was tweaked
specifically for the Codimension python parser.
