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


func peek(node: ref Node) -> int
    while node != null do
        if node.proximo == null then
            return node.valor
        end
        node = node.proximo
    end
end


func pop_front(head: ref Node) -> int
    if head == null then
        return -1
    end
    let valor: int = head.valor

    if head.proximo == null then
        // lista tinha 1 elemento: devolve o valor
        // e você decide fora daqui como sinalizar "lista vazia"
        return valor
    end

    // copia dados do próximo para o atual e pula o próximo
    head.valor = head.proximo.valor
    head.proximo = head.proximo.proximo
    return valor
end
    

let no1: Node = Node(10, null)

func print_list(node: ref Node)
    while node != null do
        print(to_str(node.valor))
        node = node.proximo
    end
end

func stack_push(valor: int)
    append(no1, valor)
end

func stack_pop() -> int
    let i:int = pop(no1)
    return i
end

stack_push(20)
stack_push(30)
stack_push(40)
print_list(no1)
print("apos pop")
stack_pop()
print_list(no1)
let topo: int = peek(no1)
print("Topo da pilha "+to_str(topo))
stack_pop()
let topo: int = peek(no1)
print("Topo da pilha "+to_str(topo))
