// ============================================
// MiniLang - Teste Árvore Binária
// Teste de inserção e percurso em árvore binária
// ============================================

print("=== TESTE ÁRVORE BINÁRIA ===")

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
// FUNÇÃO DE INSERÇÃO
// ============================================
func inserir(node: ref TreeNode, valor: int)
    if node == null then
        // Não faz nada (raiz já criada na main)
        return
    end
    if valor < node.valor then
        if node.esquerda == null then
            node.esquerda = ref TreeNode(valor, null, null)
        else
            inserir(node.esquerda, valor)
        end
    else
        if node.direita == null then
            node.direita = ref TreeNode(valor, null, null)
        else
            inserir(node.direita, valor)
        end
    end
end

print("✓ Função inserir definida")

// ============================================
// FUNÇÃO DE PERCURSO EM ORDEM
// ============================================
func percorrer_em_ordem(node: ref TreeNode)
    if node != null then
        percorrer_em_ordem(node.esquerda)
        print("Visitando: " + to_str(node.valor))
        percorrer_em_ordem(node.direita)
    end
end

print("✓ Função percorrer_em_ordem definida")

// ============================================
// EXECUÇÃO DOS TESTES
// ============================================
let raiz: TreeNode = TreeNode(8, null, null)
print("✓ Raiz criada")

inserir(ref raiz, 3)
inserir(ref raiz, 10)
inserir(ref raiz, 1)
inserir(ref raiz, 6)
inserir(ref raiz, 14)
inserir(ref raiz, 4)
inserir(ref raiz, 7)
inserir(ref raiz, 13)

print("")
print("Percorrendo em ordem...")
percorrer_em_ordem(ref raiz)

print("")
print("=== TESTE CONCLUÍDO ===") 