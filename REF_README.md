# MiniLang: When to use the `ref` keyword

This guide explains concisely when and how to use `ref` in MiniLang, with practical examples and common pitfalls.

## What is `ref`?

- Type modifier: `ref T` declares a reference to a value of type `T`. It can be used in struct fields, function parameters, variables, and return types.
- Reference operator: `ref expr` produces a reference (address) to an existing value to assign into a `ref T` destination.
- `null`: reference literal that represents the absence of a value; can be stored in values of type `ref T`.

## Use `ref` for these cases

- Self-referencing or cross-referencing struct fields
```minilang
struct Node
    value: int,
    next: ref Node
end

let n1: Node = Node(100, null)
let n2: Node = Node(200, null)
n1.next = ref n2  // use the ref operator when assigning to a ref field
```

- Function parameters when you need to mutate a struct argument
```minilang
func append(node: ref Node, value: int)
    if node.next == null then
        node.next = ref Node(value, null)
    else
        append(node.next, value)
    end
end
```
Without `ref` on the parameter, mutations inside the function will not affect the caller’s value.

- Passing and mutating container-like structs (e.g., dynamic arrays modeled as a struct)
```minilang
struct DynamicArray
    elements: int[100],
    capacity: int,
    size: int
end

func push(arr: ref DynamicArray, x: int) -> void
    if arr.size >= arr.capacity then
        // grow or reject; capacity is fixed in this simple example
    end
    arr.elements[arr.size] = x
    arr.size = arr.size + 1
end
```

- Variables that store references to structs and may be `null` or reassigned
```minilang
let cur: ref Node = null
if cur == null then
    cur = ref n1
end
```

- Return types when you want to return an existing reference
```minilang
func find(head: ref Node, value: int) -> ref Node
    let cur: ref Node = head
    while cur != null do
        if cur.value == value then
            return cur
        end
        cur = cur.next
    end
    return null
end
```

## Avoid `ref` in these cases

- Primitive types used read-only: `int`, `float`, `bool`, `string` do not need `ref` as parameters if you don’t intend to mutate an owning struct.
- Static arrays passed for reading: the compiler already handles the pointer conversion for calls; use `ref` only when your “array” is a struct you will mutate (like `DynamicArray`).
- Fields that should embed values by copy: if the field must store the value itself, not a reference, don’t use `ref`.

## Essential usage patterns

- Assigning to `ref` fields/variables requires the `ref` operator on the right-hand side
```minilang
root.left = ref childLeft   // correct
// root.left = childLeft    // incorrect
```

- Comparing to `null`
```minilang
if node.next == null then
    // ...
end
```

- Reading a `ref` field does not require the operator
```minilang
let nextNode: ref Node = node.next
```

- Mutating via `ref` parameter
```minilang
struct Counter
    value: int
end

func inc(c: ref Counter)
    c.value = c.value + 1
end
```

## Common mistakes and fixes

- Forgetting the `ref` operator when assigning a `ref` destination
```minilang
node.next = ref other
```

- Declaring a parameter without `ref` but expecting call-site mutation
```minilang
// wrong: mutations won’t escape the function
func set_value(n: Node, v: int)
    n.value = v
end

// correct
func set_value(n: ref Node, v: int)
    n.value = v
end
```

- Overusing `ref` for simple data where it brings no benefit: it adds complexity without need.

## Repository examples

- `minilang_examples/linked_list.ml` and `minilang_examples/stack.ml`: linked lists with `ref` fields and parameters.
- `minilang_examples/binary_tree2.ml` and `minilang_examples/binary_tree3.ml`: binary trees with `ref` children.
- `minilang_examples/dynamic_array.ml`: mutating a container via a `ref` parameter.
- `minilang_examples/hashmap_string_keys.ml`: local `ref` variables and `null` checks.

## Quick reference

- Types: `field: ref T`, `param: ref T`, `let v: ref T = null`, `func f(...) -> ref T`
- Operator: `ref expr` when assigning to a `ref` destination

If in doubt, browse `minilang_examples/` and `testes_unitarios_automatizados.ml` for working patterns.
