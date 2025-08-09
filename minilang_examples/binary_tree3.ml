struct LLNode
    valor: int,
    proximo: ref LLNode
end

func append(node: ref LLNode, valor: int)
    if node.proximo == null then
        node.proximo = ref LLNode(valor, null)
    else
        append(node.proximo, valor)
    end
end

let linked_list: LLNode = LLNode(-1, null)


func print_list(node: ref LLNode)
    // ignora o primeiro elemento
    node = ref node.proximo
    while node != null do
        print(to_str(node.valor))
        node = ref node.proximo
    end
end


struct Node
  data: int,
  left: ref Node,
  right: ref Node
end

// Formato mais sofisticado (múltiplos níveis)
let root: Node = Node(1, null, null)
root.left = Node(2, null, null)
root.right = Node(3, null, null)
root.left.left = Node(4, null, null)
root.left.right = Node(5, null, null)

// Desenho da arvore binaria em ASCII
//     1
//    / \
//   2   3
//  / \ 
// 4   5 

func pre_order(node: ref Node, array: ref LLNode) -> void
  if node != null then
    append(array, node.data)
    pre_order(node.left, array)
    pre_order(node.right, array)
  end
end

pre_order(root, linked_list)
print("Pre-order traversal:")
print_list(linked_list)