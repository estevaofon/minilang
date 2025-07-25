// MiniLang v2.0 - Exemplo de Pilha (Stack)
// ========================================

// Função strlen para MiniLang
func len(s: string) -> int
    let i: int = 0
    while s[i] != "\0" do
        i = i + 1
    end
    return i
end

print("=== MiniLang v2.0 - Implementação de Pilha ===")
print("")

// Definição de uma pilha simples (stack) para inteiros
// Capacidade máxima da pilha
global STACK_SIZE: int = 10

// Array para armazenar os elementos da pilha
global stack: int[10] = zeros(10)

// Índice do topo da pilha (-1 significa pilha vazia)
global top: int = -1

// Função para verificar se a pilha está vazia
func isEmpty() -> int
    if top == -1 then
        return 1
    else
        return 0
    end
end

// Função para verificar se a pilha está cheia
func isFull() -> int
    if top == STACK_SIZE - 1 then
        return 1
    else
        return 0
    end
end

// Função para adicionar elemento no topo da pilha (push)
func push(value: int) -> int
    if isFull() == 1 then
        print("Erro: Pilha cheia!")
        return 0
    else
        top = top + 1
        stack[top] = value
        return 1
    end
end

// Função para remover e retornar elemento do topo da pilha (pop)
func pop() -> int
    if isEmpty() == 1 then
        print("Erro: Pilha vazia!")
        return -1
    else
        let value: int = stack[top]
        top = top - 1
        return value
    end
end

// Função para ver o elemento do topo sem remover (peek)
func peek() -> int
    if isEmpty() == 1 then
        print("Erro: Pilha vazia!")
        return -1
    else
        return stack[top]
    end
end

// Função para imprimir todos os elementos da pilha
func printStack() -> void
    print("Estado da pilha:")
    if isEmpty() == 1 then
        print("  [Pilha vazia]")
    else
        print("  Topo -> ")
        let i: int = top
        while i >= 0 do
            print("  ")
            print(stack[i])
            if i > 0 then
                print("  |")
            end
            i = i - 1
        end
        print("  Base")
    end
    print("")
end

// Função para obter o tamanho atual da pilha
func size() -> int
    return top + 1
end

// Demonstração de uso da pilha
print(">> Demonstração de operações de pilha:")
print("")

print("1. Verificando se a pilha está vazia:")
if isEmpty() == 1 then
    print("   Pilha está vazia")
else
    print("   Pilha não está vazia")
end
print("")

print("2. Adicionando elementos (push):")
print("   Push 10")
push(10)
printStack()

print("   Push 20")
push(20)
printStack()

print("   Push 30")
push(30)
printStack()

print("   Push 40")
push(40)
printStack()

print("3. Verificando o topo da pilha (peek):")
let top_value: int = peek()
print("   Elemento no topo: ")
print(top_value)
print("")

print("4. Verificando o tamanho da pilha:")
let stack_size: int = size()
print("   Tamanho atual: ")
print(stack_size)
print("")

print("5. Removendo elementos (pop):")
print("   Pop: ")
let popped1: int = pop()
print(popped1)
printStack()

print("   Pop: ")
let popped2: int = pop()
print(popped2)
printStack()

print("6. Adicionando mais elementos:")
print("   Push 50")
push(50)
printStack()

print("   Push 60")
push(60)
printStack()

print("   Push 70")
push(70)
printStack()

print("7. Verificando se a pilha está cheia:")
if isFull() == 1 then
    print("   Pilha está cheia")
else
    print("   Pilha não está cheia")
end
print("")

print("8. Removendo todos os elementos:")
while isEmpty() == 0 do
    print("   Pop: ")
    let popped: int = pop()
    print(popped)
    printStack()
end

print("9. Tentando remover de pilha vazia:")
let invalid_pop: int = pop()
print("   Resultado: ")
print(invalid_pop)
print("")

print("10. Verificando estado final:")
if isEmpty() == 1 then
    print("   Pilha está vazia")
else
    print("   Pilha não está vazia")
end
print("")

print("=== Fim da demonstração de pilha ===") 