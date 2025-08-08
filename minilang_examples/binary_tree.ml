struct Node
  data: int,
  left: ref Node,
  right: ref Node
end

let visit: int[5] = [0, 0, 0, 0, 0]

let root: Node = Node(1, null, null)
let left_child: Node = Node(2, null, null)
let right_child: Node = Node(3, null, null)
let left_left: Node = Node(4, null, null)
let left_right: Node = Node(5, null, null)

root.left = left_child
root.right = right_child
left_child.left = left_left
left_child.right = left_right

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
