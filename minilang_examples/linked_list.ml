struct Node
    valor: int,
    proximo: ref Node
end

func append(node: ref Node, valor: int)
    if node.proximo == null then
        node.proximo = ref Node(valor, null)
    else
        append(node.proximo, valor)
    end
end


func pop(node: ref Node) -> int
    if node == null | node.proximo == null then
        return -1
    end
    while node.proximo.proximo != null do
        node = node.proximo
    end
    let valor: int = node.proximo.valor
    node.proximo = null
    return valor
end
    

let no1: Node = Node(10, null)
append(no1, 20)
append(no1, 30)
append(no1, 40)
append(no1, 50)
append(no1, 60)
append(no1, 70)
append(no1, 80)
append(no1, 90)
append(no1, 100)

func print_list(node: ref Node)
    while node != null do
        print(to_str(node.valor))
        node = node.proximo
    end
end

let v: int = pop(no1)
pop(no1)
print_list(no1)
print("Valor retornado "+to_str(v))
