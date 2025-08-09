struct Node
  data: int,
  left: ref Node,
  right: ref Node
end

// Teste simples para debug
let root: Node = Node(1, null, null)

// Testar apenas to_str com um valor simples
print("Testando to_str com valor simples:")
print(to_str(42))

// Testar to_str com campo de struct
print("Testando to_str com campo de struct:")
print(to_str(root.data))
