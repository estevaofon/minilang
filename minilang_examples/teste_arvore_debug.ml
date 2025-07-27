// ============================================
// MiniLang - Teste Árvore Binária (Debug)
// Teste com prints detalhados para identificar problemas
// ============================================

print("=== TESTE ÁRVORE BINÁRIA DEBUG ===")

// ============================================
// DEFINIÇÃO DA ESTRUTURA
// ============================================
struct TreeNode
    valor: int,
    esquerda: ref TreeNode,
    direita: ref TreeNode
end

print("✓ Struct TreeNode definido")

// ============================================
// FUNÇÃO DE INSERÇÃO COM DEBUG
// ============================================
func inserir(node: ref TreeNode, valor: int)
    print("DEBUG: inserir chamada com valor: " + to_str(valor))
    
    if node == null then
        print("DEBUG: node é null, retornando")
        return
    end
    
    print("DEBUG: node.valor = " + to_str(node.valor))
    
    if valor < node.valor then
        print("DEBUG: valor < node.valor, indo para esquerda")
        if node.esquerda == null then
            print("DEBUG: criando novo nó esquerdo")
            node.esquerda = ref TreeNode(valor, null, null)
            print("DEBUG: nó esquerdo criado com valor: " + to_str(valor))
        else
            print("DEBUG: recursão para esquerda")
            inserir(node.esquerda, valor)
        end
    else
        print("DEBUG: valor >= node.valor, indo para direita")
        if node.direita == null then
            print("DEBUG: criando novo nó direito")
            node.direita = ref TreeNode(valor, null, null)
            print("DEBUG: nó direito criado com valor: " + to_str(valor))
        else
            print("DEBUG: recursão para direita")
            inserir(node.direita, valor)
        end
    end
    print("DEBUG: inserir finalizada para valor: " + to_str(valor))
end

print("✓ Função inserir definida")

// ============================================
// FUNÇÃO DE PERCURSO COM DEBUG
// ============================================
func percorrer_em_ordem(node: ref TreeNode)
    print("DEBUG: percorrer_em_ordem chamada")
    
    if node != null then
        print("DEBUG: node não é null, valor = " + to_str(node.valor))
        print("DEBUG: indo para esquerda")
        percorrer_em_ordem(node.esquerda)
        print("DEBUG: visitando nó: " + to_str(node.valor))
        print("DEBUG: indo para direita")
        percorrer_em_ordem(node.direita)
    else
        print("DEBUG: node é null")
    end
end

print("✓ Função percorrer_em_ordem definida")

// ============================================
// EXECUÇÃO DOS TESTES
// ============================================
let raiz: TreeNode = TreeNode(8, null, null)
print("✓ Raiz criada com valor: 8")

print("")
print("=== INSERINDO PRIMEIRO NÓ ===")
inserir(ref raiz, 3)
print("✓ Primeiro nó inserido")

print("")
print("=== INSERINDO SEGUNDO NÓ ===")
inserir(ref raiz, 10)
print("✓ Segundo nó inserido")

print("")
print("=== PERCORRENDO ÁRVORE ===")
percorrer_em_ordem(ref raiz)

print("")
print("=== TESTE CONCLUÍDO ===") 