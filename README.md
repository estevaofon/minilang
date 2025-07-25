# MiniLang v2.0

A statically-typed mini programming language with LLVM backend compilation.

## Overview

MiniLang is a simple yet powerful programming language designed for educational purposes and small-scale applications. It features static typing, LLVM-based compilation, and supports common programming constructs like functions, arrays, control flow, and type casting.

## Features

- **Static Type System**: Supports `int`, `float`, `string`, and array types
- **LLVM Backend**: Compiles to native machine code using LLVM
- **Function Support**: Define and call functions with typed parameters and return values
- **Array Support**: Create and manipulate arrays with type safety
- **Control Flow**: `if-else` statements and `while` loops
- **Type Casting**: Built-in casting functions between numeric types and strings
- **Global and Local Variables**: Support for both global and local variable declarations
- **String Operations**: String concatenation and array-based string manipulation
- **Print Function**: Built-in print functionality for output

## Installation

### Prerequisites

- Python 3.13 or higher
- LLVM (the project uses llvmlite for LLVM bindings)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd mini-language
```

2. Install dependencies using uv:
```bash
uv sync
```

## Usage

### Running Programs

Use `uv run` to execute MiniLang programs:

```bash
uv run compiler.py <source_file.ml>
```

### Compilation Process

The compiler follows these steps:
1. **Lexical Analysis**: Tokenizes the source code
2. **Parsing**: Builds an Abstract Syntax Tree (AST)
3. **Code Generation**: Generates LLVM IR
4. **Execution**: Compiles and runs the generated code

## Language Syntax

### Variable Declarations

```minilang
let x: int = 42
let y: float = 3.14
let texto: string = "Hello, World!"
```

### Arrays

```minilang
let numeros: int[5] = [1, 2, 3, 4, 5]
let matriz: float[3] = [1.1, 2.2, 3.3]
```

### Functions

```minilang
func add(a: int, b: int) -> int
    return a + b
end

func greet(name: string) -> string
    return "Hello " ++ name
end
```

### Control Flow

```minilang
if x > 10 then
    print("x is greater than 10")
else
    print("x is 10 or less")
end

while i < 10 do
    print(i)
    i = i + 1
end
```

### Type Casting

```minilang
let num: int = 42
let str: string = to_str_int(num)  // Convert int to string
let flt: float = to_float(num)     // Convert int to float
```

### String Operations

```minilang
let str1: string = "Hello"
let str2: string = "World"
let result: string = str1 ++ " " ++ str2  // String concatenation
```

## Examples

The project includes several example programs in the `minilang_examples/` directory:

- `teste_simples.ml` - Basic language features demonstration
- `exemplo.ml` - Comprehensive example with arrays and functions
- `demo_completa.ml` - Full demonstration of language capabilities
- `pilha_exemplo.ml` - Stack implementation example
- `hashmap_exemplo.ml` - Hash map implementation
- `arvore_exemplo.ml` - Tree data structure example
- `dijkstra_exemplo.ml` - Dijkstra's algorithm implementation

### Quick Start Example

Create a file `hello.ml`:

```minilang
print("Hello from MiniLang!")
let x: int = 10
let y: int = 20
print("Sum: ")
print(x + y)
```

Run it:
```bash
uv run compiler.py hello.ml
```

## Project Structure

```
mini-language/
├── compiler.py              # Main compiler implementation
├── casting_functions.c      # C functions for type casting
├── pyproject.toml          # Project configuration
├── uv.lock                 # Dependency lock file
├── minilang_examples/      # Example programs
│   ├── teste_simples.ml
│   ├── exemplo.ml
│   ├── demo_completa.ml
│   └── ...
└── README.md               # This file
```

## Language Features in Detail

### Data Types

- **int**: 64-bit integer values
- **float**: Double-precision floating-point values
- **string**: Null-terminated character arrays
- **Arrays**: Fixed-size arrays of any type (e.g., `int[5]`, `float[10]`)

### Operators

- **Arithmetic**: `+`, `-`, `*`, `/`, `%` (modulo)
- **Comparison**: `>`, `<`, `>=`, `<=`, `==`, `!=`
- **Assignment**: `=`
- **String Concatenation**: `++`

### Built-in Functions

- `print(expression)` - Output values to console
- `to_str_int(int)` - Convert integer to string
- `to_str_float(float)` - Convert float to string
- `to_int(float)` - Convert float to integer (truncates)
- `to_float(int)` - Convert integer to float

## Compilation Details

The compiler generates LLVM IR code that is then compiled to native machine code. The process includes:

1. **Lexical Analysis**: Breaks source code into tokens
2. **Syntax Analysis**: Builds AST from tokens
3. **Semantic Analysis**: Type checking and validation
4. **Code Generation**: LLVM IR generation
5. **Optimization**: LLVM optimization passes
6. **Execution**: Native code execution

## Contributing

This is an educational project. Feel free to explore the code, run examples, and experiment with the language features.

## License

This project is for educational purposes.

---

**Note**: This is MiniLang v2.0, featuring static typing and LLVM backend compilation. The language is designed to be simple yet powerful, making it ideal for learning compiler design concepts and programming language implementation.
