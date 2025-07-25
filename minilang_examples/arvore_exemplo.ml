// MiniLang v2.0 - Exemplo de Árvore Binária e Percursos
// =====================================================

// Função strlen para MiniLang
func len(s: string) -> int
    let i: int = 0
    while s[i] != "\0" do
        i = i + 1
    end
    return i
end

print("=== MiniLang v2.0 - Árvore Binária e Percursos ===")
print("")

// Definição de uma árvore binária simples
// Cada nó contém um valor e índices para filhos esquerdo e direito
// -1 indica que não há filho (nó nulo)

// Estrutura da árvore usando arrays
// Valores dos nós
global tree_values: int[10] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

// Índices dos filhos esquerdos (-1 = sem filho)
global left_children: int[10] = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]

// Índices dos filhos direitos (-1 = sem filho)
global right_children: int[10] = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]

// Próximo índice disponível para inserção
global next_index: int = 0

// Função para criar um novo nó na árvore
func createNode(value: int) -> int
    if next_index >= 10 then
        print("Erro: Árvore cheia!")
        return -1
    else
        let index: int = next_index
        tree_values[index] = value
        left_children[index] = -1
        right_children[index] = -1
        next_index = next_index + 1
        return index
    end
end

// Função para inserir um filho esquerdo
func insertLeft(parent: int, value: int) -> int
    if parent == -1 then
        print("Erro: Pai inválido!")
        return -1
    else
        let child_index: int = createNode(value)
        if child_index != -1 then
            left_children[parent] = child_index
        end
        return child_index
    end
end

// Função para inserir um filho direito
func insertRight(parent: int, value: int) -> int
    if parent == -1 then
        print("Erro: Pai inválido!")
        return -1
    else
        let child_index: int = createNode(value)
        if child_index != -1 then
            right_children[parent] = child_index
        end
        return child_index
    end
end

// Função para verificar se um nó é nulo (folha)
func isNull(node: int) -> int
    if node == -1 then
        return 1
    else
        return 0
    end
end

// Função para obter o valor de um nó
func getValue(node: int) -> int
    if node == -1 then
        return -1
    else
        return tree_values[node]
    end
end

// Função para obter o filho esquerdo
func getLeftChild(node: int) -> int
    if node == -1 then
        return -1
    else
        return left_children[node]
    end
end

// Função para obter o filho direito
func getRightChild(node: int) -> int
    if node == -1 then
        return -1
    else
        return right_children[node]
    end
end

// Percursos da árvore

// Percurso em Pré-ordem: Raiz -> Esquerda -> Direita
func preorderTraversal(node: int) -> void
    if isNull(node) == 0 then
        // Visitar a raiz
        print("  ")
        print(getValue(node))
        
        // Percorrer subárvore esquerda
        let left: int = getLeftChild(node)
        preorderTraversal(left)
        
        // Percorrer subárvore direita
        let right: int = getRightChild(node)
        preorderTraversal(right)
    end
end

// Percurso em In-ordem: Esquerda -> Raiz -> Direita
func inorderTraversal(node: int) -> void
    if isNull(node) == 0 then
        // Percorrer subárvore esquerda
        let left: int = getLeftChild(node)
        inorderTraversal(left)
        
        // Visitar a raiz
        print("  ")
        print(getValue(node))
        
        // Percorrer subárvore direita
        let right: int = getRightChild(node)
        inorderTraversal(right)
    end
end

// Percurso em Pós-ordem: Esquerda -> Direita -> Raiz
func postorderTraversal(node: int) -> void
    if isNull(node) == 0 then
        // Percorrer subárvore esquerda
        let left: int = getLeftChild(node)
        postorderTraversal(left)
        
        // Percorrer subárvore direita
        let right: int = getRightChild(node)
        postorderTraversal(right)
        
        // Visitar a raiz
        print("  ")
        print(getValue(node))
    end
end

// Função para imprimir a estrutura da árvore
func printTreeStructure(node: int, level: int) -> void
    if isNull(node) == 0 then
        // Imprimir indentação
        let i: int = 0
        while i < level do
            print("  ")
            i = i + 1
        end
        
        // Imprimir o nó
        print("|- ")
        print(getValue(node))
        print("")
        
        // Imprimir filhos
        let left: int = getLeftChild(node)
        let right: int = getRightChild(node)
        
        if isNull(left) == 0 then
            printTreeStructure(left, level + 1)
        end
        
        if isNull(right) == 0 then
            printTreeStructure(right, level + 1)
        end
    end
end

// Função para contar o número de nós na árvore
func countNodes(node: int) -> int
    if isNull(node) == 1 then
        return 0
    else
        let left: int = getLeftChild(node)
        let right: int = getRightChild(node)
        let left_count: int = countNodes(left)
        let right_count: int = countNodes(right)
        return 1 + left_count + right_count
    end
end

// Função para calcular a altura da árvore
func treeHeight(node: int) -> int
    if isNull(node) == 1 then
        return -1
    else
        let left: int = getLeftChild(node)
        let right: int = getRightChild(node)
        let left_height: int = treeHeight(left)
        let right_height: int = treeHeight(right)
        
        if left_height > right_height then
            return 1 + left_height
        else
            return 1 + right_height
        end
    end
end

// Demonstração de uso da árvore
print(">> Construindo uma árvore binária:")
print("")

// Criar a raiz
let root: int = createNode(10)
print("Criando raiz com valor: ")
print(getValue(root))
print("")

// Construir a árvore:
//       10
//      /  \
//     5    15
//    / \   / \
//   3   7 12  18
//  /
// 1

// Nível 1: filhos da raiz
let left_child: int = insertLeft(root, 5)
let right_child: int = insertRight(root, 15)

// Nível 2: filhos do nó 5
let left_left: int = insertLeft(left_child, 3)
let left_right: int = insertRight(left_child, 7)

// Nível 2: filhos do nó 15
let right_left: int = insertLeft(right_child, 12)
let right_right: int = insertRight(right_child, 18)

// Nível 3: filho do nó 3
let left_left_left: int = insertLeft(left_left, 1)

print("Árvore construída!")
print("")

print(">> Estrutura da árvore:")
printTreeStructure(root, 0)
print("")

print(">> Estatísticas da árvore:")
let node_count: int = countNodes(root)
print("Número de nós: ")
print(node_count)

let height: int = treeHeight(root)
print("Altura da árvore: ")
print(height)
print("")

print(">> Percursos da árvore:")
print("")

print("1. Percurso em Pré-ordem (Raiz -> Esquerda -> Direita):")
print("   Resultado: ")
preorderTraversal(root)
print("")
print("")

print("2. Percurso em In-ordem (Esquerda -> Raiz -> Direita):")
print("   Resultado: ")
inorderTraversal(root)
print("")
print("")

print("3. Percurso em Pós-ordem (Esquerda -> Direita -> Raiz):")
print("   Resultado: ")
postorderTraversal(root)
print("")
print("")

print(">> Explicação dos percursos:")
print("")
print("Pré-ordem (10, 5, 3, 1, 7, 15, 12, 18):")
print("  - Visita a raiz primeiro, depois os filhos")
print("  - Útil para copiar árvores ou criar prefixos")
print("")
print("In-ordem (1, 3, 5, 7, 10, 12, 15, 18):")
print("  - Visita os nós em ordem crescente (para árvores BST)")
print("  - Útil para ordenação ou busca")
print("")
print("Pós-ordem (1, 3, 7, 5, 12, 18, 15, 10):")
print("  - Visita os filhos antes da raiz")
print("  - Útil para deletar árvores ou calcular expressões")
print("")

print("=== Fim da demonstração de árvore binária ===") 