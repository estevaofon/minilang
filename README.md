# Nox

A statically-typed programming language with LLVM backend compilation, featuring advanced data structures and algorithms.

<p align="center">
  <img width="300" height="300" alt="ChatGPT Image 15 de ago  de 2025, 22_43_56" src="https://github.com/user-attachments/assets/b923dd36-f4b7-4b83-972b-7ddd3547f2fe" />
</p>


## Overview

Nox is a powerful programming language designed for educational purposes and practical applications. It features static typing, LLVM-based compilation, and supports advanced programming constructs including structs, auto-referencing, dynamic assignments, and complex algorithms.

## 🚀 Key Features

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
- **Type Casting**: Universal `to_str` function for converting integers, floats, and arrays to string representations
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
cd nox
```

2. Install dependencies using uv:
```bash
uv sync
```

## Usage

### Compiling and Running Programs

First, compile the source code into an object file using the Nox compiler:

```bash
uv run python compiler.py --compile <source_file.nx>
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
uv run python compiler.py --compile testes_unitarios_automatizados.nx
gcc -o testes.exe output.obj casting_functions.c
./testes.exe
```



## Language Syntax

### Variable Declarations

```nox
let x: int = 42
let y: float = 3.14
let texto: string = "Hello, World!"
let ativo: bool = true
```

### Arrays

```nox
let numeros: int[5] = [1, 2, 3, 4, 5]
let matriz: float[3] = [1.1, 2.2, 3.3]
let vazio: int[0] = []

// Get array size using length function
let tamanho: int = length(numeros)  // Returns 5
```

### Structs

```nox
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

```nox
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

```nox
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

```nox
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

Nox provides powerful type conversion functions centered around the universal `to_str` function:

```nox
// Converting integers to string
let num: int = 42
let str_from_int: string = to_str(num)  // "42"

// Converting floats to string
let valor: float = 3.14159
let str_from_float: string = to_str(valor)  // "3.141590"

// Converting arrays to string representation
let numeros: int[5] = [1, 2, 3, 4, 5]
let str_from_array: string = to_str(numeros)  // "[1, 2, 3, 4, 5]"

let floats: float[3] = [1.1, 2.2, 3.3]
let str_from_float_array: string = to_str(floats)  // "[1.100000, 2.200000, 3.300000]"

// Other numeric conversions
let int_from_float: int = to_int(valor)     // 3 (truncates)
let float_from_int: float = to_float(num)   // 42.000000
```

### String Operations

```nox
let str1: string = "Hello"
let str2: string = "World"
let result: string = str1 + " " + str2  // String concatenation
```

### Test Suite
- `testes_unitarios_automatizados.nx` - Comprehensive test suite (87 tests)

### Quick Start Example

Create a file `hello.nx`:

```nox
print("Hello from Nox!")

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
uv run python compiler.py --compile hello.nx
gcc -o hello.exe output.obj casting_functions.c
./hello.exe
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

### Quick guide: When to use `ref`

- Use `ref` in struct fields to model self-references or cross-struct references
- Use `ref` in function parameters when you need to mutate a struct passed by the caller
- Use `ref` variables/return types when storing or returning pointers (and possibly `null`)
- See `REF_README.md` for a focused guide with examples

Example:

```nox
struct Node
    value: int,
    next: ref Node
end

func append(node: ref Node, value: int)
    if node.next == null then
        node.next = ref Node(value, null)
    else
        append(node.next, value)
    end
end
```

### Built-in Functions

- `print(expression)` - Output values to console
- `to_str(value)` - Universal conversion function that converts integers, floats, and arrays to string representation
- `to_int(float)` - Convert float to integer (truncates)
- `to_float(int)` - Convert integer to float
- `strlen(string)` - Get the length of a string
- `length(array)` - Get the size of an array (for arrays with defined size)

### Advanced Features

#### Structs with Auto-Reference
```nox
struct Node
    valor: int,
    proximo: ref Node
end

let no1: Node = Node(100, null)
let no2: Node = Node(200, null)
no1.proximo = ref no2
```

#### Binary Search
```nox
let array: int[7] = [1, 3, 5, 7, 9, 11, 13]
let posicao: int = busca_binaria(array, 7, 7)  // Returns 3
```

#### Dynamic Struct Assignment
```nox
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


## Contributing

This is an educational project showcasing advanced compiler design concepts. Feel free to explore the code, run examples, and experiment with the language features.

## License

This project is for educational purposes.

---

**Nox** - A powerful, statically-typed programming language with advanced data structures, algorithms, and LLVM backend compilation. Perfect for learning compiler design concepts and implementing complex programming language features.
