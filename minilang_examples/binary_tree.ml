struct Node
  data: int,
  left: ref Node,
  right: ref Node
end

let visit: int[5] = [0, 0, 0, 0, 0]

// Formato mais sofisticado (múltiplos níveis)
let root: Node = Node(1, null, null)
root.left = Node(2, null, null)
root.right = Node(3, null, null)
root.left.left = Node(4, null, null)
root.left.right = Node(5, null, null)

func pre_order(node: Node, index: int, array: int[]) -> int
  if node != null then
    array[index] = node.data
    print("Visiting node: " + to_str(node.data) + " at index: " + to_str(index))
    let new_index: int = index + 1
    let new_index: int = pre_order(node.left, new_index, array)
    let new_index: int = pre_order(node.right, new_index, array)
    return new_index
  else
    return index
  end
end

pre_order(root, 0, visit)
print("Pre-order traversal:")
print(to_str(visit))
