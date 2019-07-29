/*
 * codimension - graphics python two-way code editor and analyzer
 * Copyright (C) 2014 - 2016  Sergey Satskiy <sergey.satskiy@gmail.com>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Utility to print a python code syntax tree
 */


#include <sys/stat.h>

#include <iostream>


/*
 * The python grammar definition conflicts with the standard library
 * declarations on some platforms, particularly on MacOS: python uses
 * #define test 305
 * while the library has
 * bitset<_Size>::test(size_t __pos) const
 * Thus the python headers must be after certain PyCXX library includes which
 * use the standard library.
 */
#include <Python.h>
#include <node.h>
#include <grammar.h>
#include <parsetok.h>
#include <graminit.h>
#include <errcode.h>
#include <token.h>

extern grammar _PyParser_Grammar; // From graminit.c


struct PythonEnvironment
{
  PythonEnvironment()   { Py_Initialize(); }
  ~PythonEnvironment()  { Py_Finalize();   }
};



std::string errorCodeToString( int  error )
{
    switch ( error )
    {
        case E_OK:          return "E_OK";
        case E_EOF:         return "E_EOF";
        case E_INTR:        return "E_INTR";
        case E_TOKEN:       return "E_TOKEN";
        case E_SYNTAX:      return "E_SYNTAX";
        case E_NOMEM:       return "E_NOMEM";
        case E_DONE:        return "E_DONE";
        case E_ERROR:       return "E_ERROR";
        case E_TABSPACE:    return "E_TABSPACE";
        case E_OVERFLOW:    return "E_OVERFLOW";
        case E_TOODEEP:     return "E_TOODEEP";
        case E_DEDENT:      return "E_DEDENT";
        case E_DECODE:      return "E_DECODE";
        case E_EOFS:        return "E_EOFS";
        case E_EOLS:        return "E_EOLS";
        case E_LINECONT:    return "E_LINECONT";
        default:            break;
    }

    char    buf[256];
    sprintf( buf, "Unknown code %d", error );
    return buf;
}


void printError( perrdetail *  error )
{
    if ( error->error == E_OK || error->error == E_DONE )
    {
        std::cout << "No errors found" << std::endl;
        return;
    }

    std::cout << "Error structure" << std::endl
              << "  error: " << errorCodeToString( error->error ) << std::endl
              << "  filename: " << error->filename << std::endl
              << "  lineno: " << error->lineno << std::endl
              << "  offset: " << error->offset << std::endl;
    if ( error->text != NULL )
         std::cout << "  text: " << error->text << std::endl;
    std::cout << "  token: " << error->token << std::endl
              << "  expected: " << error->expected << std::endl;
}


std::string  nodeTypeToString( int  nodeType  )
{
    switch ( nodeType )
    {
        case single_input:      return "single_input";
        case file_input:        return "file_input";
        case eval_input:        return "eval_input";
        case decorator:         return "decorator";
        case decorators:        return "decorators";
        case decorated:         return "decorated";
        case funcdef:           return "funcdef";
        case parameters:        return "parameters";
        case varargslist:       return "varargslist";
        case stmt:              return "stmt";
        case simple_stmt:       return "simple_stmt";
        case small_stmt:        return "small_stmt";
        case expr_stmt:         return "expr_stmt";
        case augassign:         return "augassign";
        case del_stmt:          return "del_stmt";
        case pass_stmt:         return "pass_stmt";
        case flow_stmt:         return "flow_stmt";
        case break_stmt:        return "break_stmt";
        case continue_stmt:     return "continue_stmt";
        case return_stmt:       return "return_stmt";
        case yield_stmt:        return "yield_stmt";
        case raise_stmt:        return "raise_stmt";
        case import_stmt:       return "import_stmt";
        case import_name:       return "import_name";
        case import_from:       return "import_from";
        case import_as_name:    return "import_as_name";
        case dotted_as_name:    return "dotted_as_name";
        case import_as_names:   return "import_as_names";
        case dotted_as_names:   return "dotted_as_names";
        case dotted_name:       return "dotted_name";
        case global_stmt:       return "global_stmt";
        case assert_stmt:       return "assert_stmt";
        case compound_stmt:     return "compound_stmt";
        case if_stmt:           return "if_stmt";
        case while_stmt:        return "while_stmt";
        case for_stmt:          return "for_stmt";
        case try_stmt:          return "try_stmt";
        case with_stmt:         return "with_stmt";
        case with_item:         return "with_item";
        case except_clause:     return "except_clause";
        case suite:             return "suite";
        case test:              return "test";
        case or_test:           return "or_test";
        case and_test:          return "and_test";
        case not_test:          return "not_test";
        case comparison:        return "comparison";
        case comp_op:           return "comp_op";
        case expr:              return "expr";
        case xor_expr:          return "xor_expr";
        case and_expr:          return "and_expr";
        case shift_expr:        return "shift_expr";
        case arith_expr:        return "arith_expr";
        case term:              return "term";
        case factor:            return "factor";
        case power:             return "power";
        case atom:              return "atom";
        case testlist_comp:     return "testlist_comp";
        case lambdef:           return "lambdef";
        case trailer:           return "trailer";
        case subscriptlist:     return "subscriptlist";
        case subscript:         return "subscript";
        case sliceop:           return "sliceop";
        case exprlist:          return "exprlist";
        case testlist:          return "testlist";
        case dictorsetmaker:    return "dictorsetmaker";
        case classdef:          return "classdef";
        case arglist:           return "arglist";
        case argument:          return "argument";
        case comp_iter:         return "comp_iter";
        case comp_for:          return "comp_for";
        case comp_if:           return "comp_if";
        case encoding_decl:     return "encoding_decl";
        case yield_expr:        return "yield_expr";

        #if PY_MAJOR_VERSION == 2
        case fpdef:             return "fpdef";
        case fplist:            return "fplist";
        case print_stmt:        return "print_stmt";
        case exec_stmt:         return "exec_stmt";
        case testlist_safe:     return "testlist_safe";
        case old_test:          return "old_test";
        case old_lambdef:       return "old_lambdef";
        case listmaker:         return "listmaker";
        case list_iter:         return "list_iter";
        case list_for:          return "list_for";
        case list_if:           return "list_if";
        case testlist1:         return "testlist1";
        #else
        case async_funcdef:     return "async_funcdef";
        case typedargslist:     return "typedargslist";
        case tfpdef:            return "tfpdef";
        case vfpdef:            return "vfpdef";
        case testlist_star_expr:return "testlist_star_expr";
        case nonlocal_stmt:     return "nonlocal_stmt";
        case async_stmt:        return "async_stmt";
        case test_nocond:       return "test_nocond";
        case lambdef_nocond:    return "lambdef_nocond";
        case star_expr:         return "star_expr";
        case atom_expr:         return "atom_expr";
        case yield_arg:         return "yield_arg";
        #endif

        case ENDMARKER:         return "ENDMARKER";
        case NAME:              return "NAME";
        case NUMBER:            return "NUMBER";
        case STRING:            return "STRING";
        case NEWLINE:           return "NEWLINE";
        case INDENT:            return "INDENT";
        case DEDENT:            return "DEDENT";
        case LPAR:              return "LPAR";
        case RPAR:              return "RPAR";
        case LSQB:              return "LSQB";
        case RSQB:              return "RSQB";
        case COLON:             return "COLON";
        case COMMA:             return "COMMA";
        case SEMI:              return "SEMI";
        case PLUS:              return "PLUS";
        case MINUS:             return "MINUS";
        case STAR:              return "STAR";
        case SLASH:             return "SLASH";
        case VBAR:              return "VBAR";
        case AMPER:             return "AMPER";
        case LESS:              return "LESS";
        case GREATER:           return "GREATER";
        case EQUAL:             return "EQUAL";
        case DOT:               return "DOT";
        case PERCENT:           return "PERCENT";
        case LBRACE:            return "LBRACE";
        case RBRACE:            return "RBRACE";
        case EQEQUAL:           return "EQEQUAL";
        case NOTEQUAL:          return "NOTEQUAL";
        case LESSEQUAL:         return "LESSEQUAL";
        case GREATEREQUAL:      return "GREATEREQUAL";
        case TILDE:             return "TILDE";
        case CIRCUMFLEX:        return "CIRCUMFLEX";
        case LEFTSHIFT:         return "LEFTSHIFT";
        case RIGHTSHIFT:        return "RIGHTSHIFT";
        case DOUBLESTAR:        return "DOUBLESTAR";
        case PLUSEQUAL:         return "PLUSEQUAL";
        case MINEQUAL:          return "MINEQUAL";
        case STAREQUAL:         return "STAREQUAL";
        case SLASHEQUAL:        return "SLASHEQUAL";
        case PERCENTEQUAL:      return "PERCENTEQUAL";
        case AMPEREQUAL:        return "AMPEREQUAL";
        case VBAREQUAL:         return "VBAREQUAL";
        case CIRCUMFLEXEQUAL:   return "CIRCUMFLEXEQUAL";
        case LEFTSHIFTEQUAL:    return "LEFTSHIFTEQUAL";
        case RIGHTSHIFTEQUAL:   return "RIGHTSHIFTEQUAL";
        case DOUBLESTAREQUAL:   return "DOUBLESTAREQUAL";
        case DOUBLESLASH:       return "DOUBLESLASH";
        case DOUBLESLASHEQUAL:  return "DOUBLESLASHEQUAL";
        case AT:                return "AT";
        case OP:                return "OP";
        case ERRORTOKEN:        return "ERRORTOKEN";
        case N_TOKENS:          return "N_TOKENS";

        #if PY_MAJOR_VERSION == 2
        case BACKQUOTE:         return "BACKQUOTE";
        #else
        case ATEQUAL:           return "ATEQUAL";
        case RARROW:            return "RARROW";
        case ELLIPSIS:          return "ELLIPSIS";
        #if PY_MINOR_VERSION < 7
        // The AWAIT and ASYNC became the proper keywords in 3.7
        case AWAIT:             return "AWAIT";
        case ASYNC:             return "ASYNC";
        #endif
        #endif
        default:                break;
    }

    char    buf[256];
    sprintf( buf, "Unknown type %d", nodeType );
    return buf;
}



void printTree( node *  n, size_t  level )
{
    for ( size_t k = 0; k < level * 2; ++k )
        std::cout << " ";
    std::cout << "Type: " << nodeTypeToString( n->n_type )
              << " line: " << n->n_lineno << " col: " << n->n_col_offset;
    if ( n->n_str != NULL )
         std::cout << " str: " << n->n_str;
    std::cout << std::endl;
    for ( int k = 0; k < n->n_nchildren; ++k )
        printTree( &(n->n_child[ k ]), level + 1 );
}


int getTotalLines( node *  tree )
{
    if ( tree == NULL )
        return -1;

    if ( tree->n_type != file_input )
        tree = &(tree->n_child[ 0 ]);

    for ( int k = 0; k < tree->n_nchildren; ++k )
    {
        node *  child = &(tree->n_child[ k ]);
        if ( child->n_type == ENDMARKER )
            return child->n_lineno;
    }
    return -1;
}


int main( int  argc, char *  argv[] )
{
    if ( argc != 2 && argc != 3 )
    {
        std::cerr << "Usage: " << argv[0] << " <python file name> [loops]" << std::endl;
        return EXIT_FAILURE;
    }

    FILE *              f = fopen( argv[1], "r" );
    if ( f == NULL )
    {
        std::cerr << "Cannot open " << argv[1] << std::endl;
        return EXIT_FAILURE;
    }

    int     loops = 1;
    if ( argc == 3 )
    {
        loops = atoi( argv[2] );
        if ( loops <= 0 )
        {
            std::cerr << "Number of loops must be >= 1" << std::endl;
            return EXIT_FAILURE;
        }
    }


    struct stat     st;
    stat( argv[1], &st );

    char            buffer[st.st_size + 2];
    size_t          itemCount = fread( buffer, st.st_size, 1, f );
    if (itemCount != 1)
    {
        std::cerr << "Unexpected number of read items. Must be 1, received "
                  << itemCount << std::endl;
        return EXIT_FAILURE;
    }

    buffer[ st.st_size ] = '\n';
    buffer[ st.st_size + 1 ] = '\0';
    fclose( f );

    PythonEnvironment   pyEnv;
    perrdetail          error;
    PyCompilerFlags     flags = { 0 };

    for ( int  k = 0; k < loops; ++k )
    {
        node *              n = PyParser_ParseStringFlagsFilename(
                                    buffer,
                                    argv[1],
                                    &_PyParser_Grammar,
                                    file_input, &error, flags.cf_flags );

        if ( n == NULL )
        {
            std::cerr << "Parser error" << std::endl;
            printError( &error );
            return EXIT_FAILURE;
        }

        if ( loops == 1 )
        {
            printTree( n, 0 );
            printError( &error );
            std::cout << "Total number of lines: " << getTotalLines( n ) << std::endl;
        }
        PyNode_Free( n );
    }

    return EXIT_SUCCESS;
}

