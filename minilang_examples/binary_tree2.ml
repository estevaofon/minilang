// ============================================
// IMPLEMENTAÇÃO DE ÁRVORE BINÁRIA EM MINILANG
// ============================================

// Definir a estrutura do array dinâmico
struct DynamicArray
    elementos: int[100],      // Array interno para armazenar os elementos
    capacidade: int,          // Capacidade máxima atual
    tamanho: int              // Número atual de elementos
end

// Função para criar um novo array dinâmico
func criar_array_dinamico() -> DynamicArray
    let array: int[100] = zeros(100)  // Array fixo de 100 elementos
    return DynamicArray(array, 100, 0)  // Capacidade fixa de 100, tamanho inicial 0
end

// Função para adicionar elemento ao final do array
func adicionar_elemento(arr: ref DynamicArray, elemento: int) -> void
    if arr.tamanho >= arr.capacidade then
        print("ERRO: Array está cheio! Não é possível adicionar mais elementos.")
        return
    end
    
    arr.elementos[arr.tamanho] = elemento
    arr.tamanho = arr.tamanho + 1
    
    //print("Elemento " + to_str(elemento) + " adicionado na posição " + to_str(arr.tamanho - 1))
end

// Função para obter elemento de uma posição
func obter_elemento(arr: ref DynamicArray, posicao: int) -> int
    if posicao < 0 | posicao >= arr.tamanho then
        print("ERRO: Posição inválida: " + to_str(posicao))
        return 0
    end
    
    return arr.elementos[posicao]
end

// Função para imprimir o array
func imprimir_array(arr: ref DynamicArray) -> void
    print("Array Dinâmico:")
    print("  Tamanho: " + to_str(arr.tamanho))
    print("  Capacidade: " + to_str(arr.capacidade))
    
    // Construir a string dos elementos em uma linha
    let elementos_str: string = "["
    
    let i: int = 0
    while i < arr.tamanho do
        if i > 0 then
            elementos_str = elementos_str + ", "
        end
        elementos_str = elementos_str + to_str(arr.elementos[i])
        i = i + 1
    end
    
    elementos_str = elementos_str + "]"
    print("  Elementos: " + elementos_str)
end

// ============================================
// TESTES DO ARRAY DINÂMICO
// ============================================

// Criar array dinâmico como variável local (sem malloc)
let meu_array: DynamicArray = criar_array_dinamico()
// imprimir_array(meu_array)

print("")
print("=== ADICIONANDO ELEMENTOS ===")

// Adicionar elementos
//adicionar_elemento(meu_array, 1000)
//imprimir_array(meu_array)



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

func pre_order(node: ref Node, array: ref DynamicArray) -> void
  if node != null then
    adicionar_elemento(array, node.data)
    pre_order(node.left, array)
    pre_order(node.right, array)
  end
end

pre_order(root, meu_array)
print("Pre-order traversal:")
imprimir_array(meu_array)
