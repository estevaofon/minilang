# MiniLang v2.0

A statically-typed mini programming language with LLVM backend compilation, featuring advanced data structures and algorithms.

## Overview

MiniLang v2.0 is a powerful programming language designed for educational purposes and practical applications. It features static typing, LLVM-based compilation, and supports advanced programming constructs including structs, auto-referencing, dynamic assignments, and complex algorithms.

## 🚀 New Features in v2.0

### **Advanced Data Structures**
- **Structs with Auto-Reference**: Self-referencing structs using `ref` operator
- **Dynamic Field Assignment**: Modify struct fields at runtime
- **Constructors**: Create structs with different data types
- **Nested Structs**: Complex data structures with nested fields

### **Array Enhancements**
- **Static Arrays**: Fixed-size arrays with type safety
- **Dynamic Arrays**: Arrays passed as function parameters
- **Automatic Conversion**: Seamless conversion between static arrays and pointers
- **Binary Search**: Efficient search algorithms for sorted arrays

### **Algorithm Support**
- **Binary Search**: O(log n) search in sorted arrays
- **Linked Lists**: Self-referencing node structures
- **Binary Trees**: Hierarchical data structures
- **Complex Algorithms**: Support for advanced algorithms

## Features

### Core Language Features
- **Static Type System**: Supports `int`, `float`, `string`, `bool`, and array types
- **LLVM Backend**: Compiles to native machine code using LLVM
- **Function Support**: Define and call functions with typed parameters and return values
- **Array Support**: Create and manipulate arrays with type safety
- **Control Flow**: `if-else` statements and `while` loops
- **Type Casting**: Built-in casting functions between numeric types and strings
- **Global and Local Variables**: Support for both global and local variable declarations
- **String Operations**: String concatenation and array-based string manipulation
- **Print Function**: Built-in print functionality for output

### Advanced Features
- **Structs**: User-defined composite data types
- **Auto-Reference**: Self-referencing structs with `ref` operator
- **Dynamic Assignment**: Modify struct fields at runtime
- **Constructors**: Create structs with different data types
- **Binary Search**: Efficient search in sorted arrays
- **Complex Algorithms**: Support for linked lists, trees, and graphs

## Installation

### Prerequisites

- Python 3.13 or higher
- LLVM (the project uses llvmlite for LLVM bindings)
- GCC or compatible C compiler

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

### Compiling and Running Programs

First, compile the source code into an object file using the MiniLang compiler:

```bash
uv run python compiler.py --compile <source_file.ml>
```

Then link the generated object file with the casting functions written in C:

```bash
gcc -o programa.exe output.obj casting_functions.c
```

Run the executable:

```bash
./programa.exe
```

### Running Test Suite

Execute the comprehensive test suite:

```bash
uv run python compiler.py --compile testes_unitarios_automatizados.ml
gcc -o testes.exe output.obj casting_functions.c
./testes.exe
```

## Language Syntax

### Variable Declarations

```minilang
let x: int = 42
let y: float = 3.14
let texto: string = "Hello, World!"
let ativo: bool = true
```

### Arrays

```minilang
let numeros: int[5] = [1, 2, 3, 4, 5]
let matriz: float[3] = [1.1, 2.2, 3.3]
let vazio: int[0] = []
```

### Structs

```minilang
struct Pessoa
    nome: string,
    idade: int,
    ativo: bool
end

// Create struct with constructor
let pessoa: Pessoa = Pessoa("João", 25, true)

// Dynamic field assignment
pessoa.idade = 26
pessoa.nome = "João Silva"
```

### Auto-Referencing Structs

```minilang
struct TreeNode
    valor: int,
    esquerda: ref TreeNode,
    direita: ref TreeNode
end

// Create nodes
let raiz: TreeNode = TreeNode(50, null, null)
let filho_esq: TreeNode = TreeNode(25, null, null)

// Link nodes
raiz.esquerda = ref filho_esq
```

### Functions

```minilang
func add(a: int, b: int) -> int
    return a + b
end

func busca_binaria(arr: int[], tamanho: int, valor: int) -> int
    let inicio: int = 0
    let fim: int = tamanho - 1
    
    while inicio <= fim do
        let meio: int = (inicio + fim) / 2
        
        if arr[meio] == valor then
            return meio
        end
        
        if arr[meio] < valor then
            inicio = meio + 1
        else
            fim = meio - 1
        end
    end
    
    return -1
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

The project includes comprehensive examples demonstrating all features:

### Basic Examples
- `teste_simples.ml` - Basic language features demonstration
- `exemplo.ml` - Comprehensive example with arrays and functions
- `demo_completa.ml` - Full demonstration of language capabilities

### Data Structure Examples
- `pilha_exemplo.ml` - Stack implementation example
- `hashmap_exemplo.ml` - Hash map implementation
- `arvore_exemplo.ml` - Tree data structure example
- `dijkstra_exemplo.ml` - Dijkstra's algorithm implementation

### Advanced Examples
- `arvore_binaria_atualizada.ml` - Binary tree with auto-reference
- `arvore_binaria_construtores.ml` - Binary tree with constructors
- `teste_struct_auto_ref.ml` - Auto-referencing structs
- `teste_solucao_array_statico.ml` - Array static to pointer conversion

### Test Suite
- `testes_unitarios_automatizados.ml` - Comprehensive test suite (87 tests)

### Quick Start Example

Create a file `hello.ml`:

```minilang
print("Hello from MiniLang v2.0!")

// Basic operations
let x: int = 10
let y: int = 20
print("Sum: ")
print(x + y)

// Struct example
struct Produto
    codigo: int,
    nome: string,
    preco: float
end

let produto: Produto = Produto(1, "Laptop", 2500.50)
print("Product: ")
print(produto.nome)
```

Run it:
```bash
uv run python compiler.py --compile hello.ml
gcc -o hello.exe output.obj casting_functions.c
./hello.exe
```

## Project Structure

```
mini-language/
├── compiler.py                          # Main compiler implementation
├── casting_functions.c                  # C functions for type casting
├── pyproject.toml                      # Project configuration
├── uv.lock                            # Dependency lock file
├── README.md                          # This file
├── RESUMO_IMPLEMENTACAO.md            # Implementation summary
├── AUTO_REFERENCIAMENTO_STRUCTS.md    # Auto-reference documentation
├── EXEMPLOS_AUTO_REFERENCIA.md        # Auto-reference examples
├── minilang_examples/                  # Example programs
│   ├── teste_simples.ml
│   ├── exemplo.ml
│   ├── demo_completa.ml
│   ├── arvore_binaria_atualizada.ml
│   ├── arvore_binaria_construtores.ml
│   ├── teste_struct_auto_ref.ml
│   └── ...
└── testes_unitarios_automatizados.ml   # Comprehensive test suite
```

## Language Features in Detail

### Data Types

- **int**: 64-bit integer values
- **float**: Double-precision floating-point values
- **string**: Null-terminated character arrays
- **bool**: Boolean values (true/false)
- **Arrays**: Fixed-size arrays of any type (e.g., `int[5]`, `float[10]`)
- **Structs**: User-defined composite data types
- **ref**: Reference types for auto-referencing

### Operators

- **Arithmetic**: `+`, `-`, `*`, `/`, `%` (modulo)
- **Comparison**: `>`, `<`, `>=`, `<=`, `==`, `!=`
- **Logical**: `&` (and), `|` (or), `!` (not)
- **Assignment**: `=`
- **String Concatenation**: `++`
- **Reference**: `ref` (for creating references)

### Built-in Functions

- `print(expression)` - Output values to console
- `to_str_int(int)` - Convert integer to string
- `to_str_float(float)` - Convert float to string
- `to_int(float)` - Convert float to integer (truncates)
- `to_float(int)` - Convert integer to float

### Advanced Features

#### Structs with Auto-Reference
```minilang
struct Node
    valor: int,
    proximo: ref Node
end

let no1: Node = Node(100, null)
let no2: Node = Node(200, null)
no1.proximo = ref no2
```

#### Binary Search
```minilang
let array: int[7] = [1, 3, 5, 7, 9, 11, 13]
let posicao: int = busca_binaria(array, 7, 7)  // Returns 3
```

#### Dynamic Struct Assignment
```minilang
struct Funcionario
    id: int,
    salario: float,
    ativo: bool
end

let func: Funcionario = Funcionario(1001, 3500.00, true)
func.salario = 3800.00  // Dynamic assignment
func.ativo = false
```

## Compilation Details

The compiler generates LLVM IR code that is then compiled to native machine code. The process includes:

1. **Lexical Analysis**: Breaks source code into tokens
2. **Syntax Analysis**: Builds AST from tokens
3. **Semantic Analysis**: Type checking and validation
4. **Code Generation**: LLVM IR generation with advanced features
5. **Optimization**: LLVM optimization passes
6. **Execution**: Native code execution

### Advanced Compilation Features

- **Automatic Array Conversion**: Static arrays automatically converted to pointers when passed to functions
- **Reference Handling**: Proper handling of `ref` types and auto-referencing
- **Struct Field Access**: Efficient access to struct fields with dynamic assignment
- **Type Safety**: Comprehensive type checking for all language constructs

## Test Results

The comprehensive test suite includes **87 tests** covering:

- ✅ **Basic Types**: int, float, string, bool
- ✅ **Arithmetic Operations**: All mathematical operations
- ✅ **Comparison Operations**: All comparison operators
- ✅ **Logical Operations**: AND, OR, NOT operations
- ✅ **Arrays**: Static and dynamic arrays
- ✅ **String Operations**: Concatenation and manipulation
- ✅ **Type Conversion**: All casting functions
- ✅ **Control Flow**: if-else and while loops
- ✅ **Functions**: Function definition and calls
- ✅ **Structs**: Basic struct operations
- ✅ **Algorithms**: Array manipulation and search
- ✅ **Auto-Reference**: Self-referencing structs
- ✅ **Dynamic Assignment**: Runtime field modification
- ✅ **Constructors**: Struct creation with different types
- ✅ **Binary Search**: Efficient search algorithms
- ✅ **Complex Operations**: Advanced language features

**Result**: 🎉 **ALL 87 TESTS PASSED!**

## Contributing

This is an educational project showcasing advanced compiler design concepts. Feel free to explore the code, run examples, and experiment with the language features.

## License

This project is for educational purposes.

---

**MiniLang v2.0** - A powerful, statically-typed programming language with advanced data structures, algorithms, and LLVM backend compilation. Perfect for learning compiler design concepts and implementing complex programming language features.
