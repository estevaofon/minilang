struct Node
  data: int,
  left: ref Node,
  right: ref Node
end

// Teste simples para debug
let root: Node = Node(1, null, null)
print("Root criado")

root.left = Node(2, null, null)
print("Root.left criado")

root.right = Node(3, null, null)
print("Root.right criado")

root.left.left = Node(4, null, null)
print("Root.left.left criado")

root.left.right = Node(5, null, null)
print("Root.left.right criado")

// Testar acesso direto aos campos
print("=== Testando acesso direto ===")
print("Root.data = " + to_str(root.data))
print("Root.left.data = " + to_str(root.left.data))
print("Root.right.data = " + to_str(root.right.data))
print("Root.left.left.data = " + to_str(root.left.left.data))
print("Root.left.right.data = " + to_str(root.left.right.data))
